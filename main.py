import sys
import json
import uuid
import random
import threading
import time
from pathlib import Path
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import text

# 0. Centralized Deck Shuffle dealer for track selection
track_deck_lock = threading.Lock()
server_track_deck = []

def assign_unique_track(track_list):
    """Draw a track from the centralized deck. Reshuffle automatically when depleted."""
    global server_track_deck
    with track_deck_lock:
        if not server_track_deck or any(idx >= len(track_list) for idx in server_track_deck):
            server_track_deck = list(range(len(track_list)))
            random.shuffle(server_track_deck)
        chosen_idx = server_track_deck.pop()
        return track_list[chosen_idx]

# 1. System path resolution configuration
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from db_connection import get_engine
from quiz_metadata import QUIZ_QUESTIONS_MAP, ARCHETYPES_INFO
from quiz_scoring import calculate_quiz_results
from gemini_quiz_engine import generate_deep_wrapped_payload

# 2. FastAPI application initialization
app = FastAPI(
    title="X-Men Wrapped API (Marketing Edition)",
    description="Backend API calculating resilience metrics and generating Spotify Wrapped style stories",
    version="1.5.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Pydantic Request Schemas
class QuizSubmission(BaseModel):
    session_id: str = Field(..., description="Unique quiz session identifier issued at initialization")
    track_id: Optional[int] = Field(None, description="Pre-assigned audio track ID from initialization")
    user_name: str = Field(default="Chiến thần Deadline", max_length=50)
    user_age: int = Field(..., ge=1, le=250)
    answers: Dict[str, str] = Field(..., description="Mapping of question IDs to selected option keys (Q1 -> Q7)")

# ==============================================================================
# BACKGROUND TASK QUEUE WORKER
# ==============================================================================
MAX_CONCURRENT_LLM = 10
active_llm_threads = 0
active_threads_lock = threading.Lock()

def process_single_quiz_job(session_id: str, scoring_result: Dict[str, Any], track_id: Optional[int]):
    """Isolated worker thread invoking LLM engine and persisting results to MySQL."""
    global active_llm_threads
    engine = get_engine('xmen_wrapped')
    try:
        # Retrieve associated audio track metadata
        assigned_track = None
        if track_id:
            with engine.connect() as conn:
                q_track = text("SELECT id, title, artist, artist_portrait_url, cover_url, cut_url, full_url FROM tracks WHERE id = :t_id LIMIT 1")
                row_t = conn.execute(q_track, {"t_id": track_id}).mappings().fetchone()
                if row_t:
                    assigned_track = dict(row_t)

        # Execute Gemini LLM Generation Engine
        llm_payload = generate_deep_wrapped_payload(scoring_result)
        if assigned_track:
            llm_payload["assigned_track"] = assigned_track

        # Commit completed payload and update status to MySQL
        update_sql = """
            UPDATE xmen_quiz_records
            SET llm_payload = :llm_payload, status = 'COMPLETED'
            WHERE session_id = :session_id
        """
        with engine.begin() as conn:
            conn.execute(text(update_sql), {
                "llm_payload": json.dumps(llm_payload, ensure_ascii=False),
                "session_id": session_id
            })
    except Exception as ex:
        print(f"[!] Worker exception at session {session_id}: {ex}")
        with engine.begin() as conn:
            conn.execute(text("UPDATE xmen_quiz_records SET status = 'FAILED' WHERE session_id = :s_id"), {"s_id": session_id})
    finally:
        with active_threads_lock:
            active_llm_threads -= 1

def queue_worker_loop():
    """Background poll loop scanning PENDING records and throttling up to 10 concurrent requests."""
    global active_llm_threads
    engine = get_engine('xmen_wrapped')
    while True:
        try:
            with active_threads_lock:
                available_slots = MAX_CONCURRENT_LLM - active_llm_threads

            if available_slots > 0:
                with engine.connect() as conn:
                    select_sql = text("""
                        SELECT session_id, scoring_data
                        FROM xmen_quiz_records
                        WHERE status = 'PENDING'
                        ORDER BY id ASC
                        LIMIT :limit_slots
                    """)
                    pending_records = conn.execute(select_sql, {"limit_slots": available_slots}).mappings().fetchall()

                for row in pending_records:
                    sid = row["session_id"]
                    scoring_data = json.loads(row["scoring_data"]) if isinstance(row["scoring_data"], str) else row["scoring_data"]
                    t_id = scoring_data.get("track_id")

                    with engine.begin() as conn:
                        conn.execute(text("UPDATE xmen_quiz_records SET status = 'PROCESSING' WHERE session_id = :sid"), {"sid": sid})

                    with active_threads_lock:
                        active_llm_threads += 1

                    t = threading.Thread(target=process_single_quiz_job, args=(sid, scoring_data, t_id), daemon=True)
                    t.start()

        except Exception as e:
            print(f"[!] Worker queue dispatch error: {e}")

        time.sleep(0.5)

# Initialize background daemon thread on server startup
threading.Thread(target=queue_worker_loop, daemon=True).start()

# ==============================================================================
# HTTP ROUTE ENDPOINTS
# ==============================================================================
@app.get("/")
def root():
    quiz_file = CURRENT_DIR / "quiz.html"
    return FileResponse(quiz_file if quiz_file.exists() else CURRENT_DIR / "index.html")

@app.get("/quiz.html")
def serve_quiz():
    quiz_file = CURRENT_DIR / "quiz.html"
    if quiz_file.exists():
        return FileResponse(quiz_file)
    raise HTTPException(status_code=404, detail="File quiz.html not found.")

@app.get("/index.html")
def serve_index():
    quiz_file = CURRENT_DIR / "quiz.html"
    return FileResponse(quiz_file if quiz_file.exists() else CURRENT_DIR / "index.html")

@app.get("/index2.html")
def get_wrapped_page():
    index2_file = CURRENT_DIR / "index2.html"
    if index2_file.exists():
        return FileResponse(index2_file)
    raise HTTPException(status_code=404, detail="File index2.html not found.")

@app.get("/test_discount.html")
def serve_test_discount():
    """Serve promotional 50% discount voucher page."""
    discount_file = CURRENT_DIR / "test_discount.html"
    if discount_file.exists():
        return FileResponse(discount_file)
    raise HTTPException(status_code=404, detail="File test_discount.html not found.")

@app.get("/api/quiz/init-session")
def init_quiz_session():
    engine = get_engine('xmen_wrapped')
    try:
        with engine.connect() as conn:
            query = text("""
                SELECT id, title, artist, artist_portrait_url, cover_url, cut_url, full_url
                FROM tracks ORDER BY id ASC
            """)
            all_tracks = [dict(r) for r in conn.execute(query).mappings().fetchall()]

        if not all_tracks:
            raise HTTPException(status_code=404, detail="No track records found in database.")

        assigned_track = assign_unique_track(all_tracks)
        session_id = f"xmen_{uuid.uuid4().hex[:10]}"
        return {"session_id": session_id, "track": assigned_track}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Session initialization failed: {e}")

@app.get("/api/tracks")
def get_tracks():
    engine = get_engine('xmen_wrapped')
    try:
        with engine.connect() as conn:
            rows = conn.execute(text("SELECT id, title, artist, artist_portrait_url, cover_url, cut_url, full_url FROM tracks")).mappings().fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying tracks repository: {e}")

@app.get("/api/quiz/questions")
def get_questions():
    formatted = []
    for q_id, q_data in QUIZ_QUESTIONS_MAP.items():
        opts = [{"key": k, "label": v.get("label", "")} for k, v in q_data["options"].items()]
        formatted.append({
            "id": q_id,
            "dimension": q_data.get("dimension"),
            "title": q_data.get("title"),
            "question": q_data.get("question"),
            "options": opts
        })
    return {"questions": formatted}

@app.post("/api/quiz/submit")
def submit_quiz(payload: QuizSubmission):
    try:
        engine = get_engine('xmen_wrapped')

        # 1. Compute deterministic quantitative scoring metrics
        scoring_result = calculate_quiz_results(payload.user_age, payload.answers)
        scoring_result["user_name"] = payload.user_name
        scoring_result["track_id"] = payload.track_id
        scoring_result["is_troll_age"] = bool(payload.user_age < 12 or payload.user_age > 85)

        dims = scoring_result.get("dimensions", {})
        arch = scoring_result.get("archetype", {})

        # Default llm_payload to '{}' to ensure strict compatibility with NOT NULL database constraints
        insert_sql = """
        INSERT INTO xmen_quiz_records (
            session_id, user_age, hair_stress_age, delta_age, grooming_iq,
            archetype_code, archetype_title, scalp_profile, exposure_level,
            root_solving_pct, fragrance_masking_pct, status,
            raw_answers, scoring_data, llm_payload
        ) VALUES (
            :session_id, :user_age, :hair_stress_age, :delta_age, :grooming_iq,
            :archetype_code, :archetype_title, :scalp_profile, :exposure_level,
            :root_solving_pct, :fragrance_masking_pct, 'PENDING',
            :raw_answers, :scoring_data, '{}'
        );
        """
        with engine.begin() as conn:
            conn.execute(
                text(insert_sql),
                {
                    "session_id": payload.session_id,
                    "user_age": scoring_result["user_age"],
                    "hair_stress_age": scoring_result["hair_stress_age"],
                    "delta_age": scoring_result["delta_age"],
                    "grooming_iq": scoring_result["grooming_iq"],
                    "archetype_code": arch.get("code", "routine_man"),
                    "archetype_title": arch.get("title", "THE ROUTINE MAN"),
                    "scalp_profile": dims.get("current_condition", {}).get("scalp_profile", "Clean & Balanced"),
                    "exposure_level": dims.get("root_exposure", {}).get("level", "Moderate"),
                    "root_solving_pct": dims.get("grooming_behavior", {}).get("root_problem_solving_pct", 50.0),
                    "fragrance_masking_pct": dims.get("grooming_behavior", {}).get("fragrance_masking_pct", 50.0),
                    "raw_answers": json.dumps(scoring_result["raw_answers"]),
                    "scoring_data": json.dumps(scoring_result, ensure_ascii=False)
                }
            )

        return {
            "session_id": payload.session_id,
            "status": "PENDING",
            "message": "Submission received successfully; background analytics pipeline initiated."
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Submission processing error: {str(e)}")

@app.get("/api/quiz/result/{session_id}")
def get_quiz_result(session_id: str):
    """Frontend polling endpoint to fetch computed diagnostics and AI-generated narrative payload."""
    query_sql = """
    SELECT session_id, user_age, hair_stress_age, delta_age, grooming_iq,
           archetype_code, archetype_title, scalp_profile, exposure_level,
           root_solving_pct, fragrance_masking_pct, status, scoring_data, llm_payload, created_at
    FROM xmen_quiz_records
    WHERE session_id = :session_id
    LIMIT 1;
    """
    engine = get_engine('xmen_wrapped')
    with engine.connect() as conn:
        row = conn.execute(text(query_sql), {"session_id": session_id}).mappings().fetchone()
        
    if not row:
        raise HTTPException(status_code=404, detail="No diagnostic record found for this session.")

    scoring_obj = json.loads(row["scoring_data"]) if isinstance(row["scoring_data"], str) else (row["scoring_data"] or {})
    wrapped_obj = json.loads(row["llm_payload"]) if (row["llm_payload"] and isinstance(row["llm_payload"], str)) else {}
    assigned_track = wrapped_obj.get("assigned_track", None)
    
    return {
        "session_id": row["session_id"],
        "status": row["status"],
        "user_name": scoring_obj.get("user_name", "Bro"),
        "user_age": row["user_age"],
        "hair_stress_age": row["hair_stress_age"],
        "delta_age": row["delta_age"],
        "grooming_iq": row["grooming_iq"],
        "archetype": {
            "code": row["archetype_code"],
            "title": row["archetype_title"],
        },
        "scalp_profile": row["scalp_profile"],
        "exposure_level": row["exposure_level"],
        "root_solving_pct": float(row["root_solving_pct"] if row["root_solving_pct"] is not None else 50.0),
        "fragrance_masking_pct": float(row["fragrance_masking_pct"] if row["fragrance_masking_pct"] is not None else 50.0),
        "scoring": scoring_obj,
        "wrapped": wrapped_obj,
        "assigned_track": assigned_track,
        "created_at": str(row["created_at"])
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
