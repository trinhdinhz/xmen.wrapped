# X-Men Wrapped Engine

A personalized data storytelling and archetype profiling system built on an asynchronous backend architecture integrated with LLMs and CDN-optimized multimedia storage.

---

### 1. Key Engineering Highlights

* **Behavioral Archetype & Scoring Engine (`quiz_scoring.py`, `quiz_metadata.py`):**  
  Multi-dimensional behavioral response analysis and weighted scoring algorithms for user persona clustering, powering hyper-personalized digital content campaigns.
* **Asynchronous Background Task & Concurrency Throttling (`main.py`):**  
  Decoupled HTTP request ingestion from LLM generation workloads via a multi-threaded producer-consumer pattern. Enforces strict concurrency limits (`MAX_CONCURRENT_LLM = 10`) with thread locking to regulate resource ceilings and prevent database connection pool exhaustion.
* **LLM Integration & Dynamic Content (`gemini_quiz_engine.py`, `gemini_client.py`):**  
  Standardized wrapper integrating the Google GenAI SDK, leveraging structured prompt engineering to generate deterministic, real-time JSON payloads.
* **Connection Pooling & Data Governance (`db_connection.py`, `init_quiz_db.py`):**  
  Centralized connection lifecycle management powered by SQLAlchemy Engine Pooling, optimizing query throughput and isolating MySQL workloads.
* **Media Delivery Pipeline & Data Visualization (`*.html`):**  
  Synchronized audio-visual metadata delivered via Cloudinary CDN, backed by an in-memory deck shuffle algorithm ensuring balanced, low-latency client-side content delivery.

---

### 2. Tech Stack

* **Backend Framework:** Python 3.10+, FastAPI, Uvicorn, Pydantic v2
* **Database & Drivers:** MySQL, SQLAlchemy 2.0 (Connection Pooling), PyMySQL, mysql-connector-python
* **AI & LLM Services:** Google GenAI SDK (`google-genai`)
* **Storage & CDN:** Cloudinary CDN
* **Networking & Tunneling:** ngrok (Public Ingress Tunneling), HTTPX, Requests

---

### 3. Repository Structure

```text
├── db_connection.py        # MySQL connection pooling & SQLAlchemy session management
├── gemini_client.py        # Google GenAI SDK client wrapper & configuration
├── gemini_quiz_engine.py   # Dynamic prompt generation & structured output parser
├── quiz_scoring.py         # Multi-axis scoring algorithm & persona clustering
├── quiz_metadata.py        # Quiz schemas, scoring rubrics & archetype definitions
├── init_quiz_db.py         # Data Definition Script (DDL) for database initialization
├── main.py                 # FastAPI entry point, background workers & REST endpoints
├── requirements.txt        # Project dependencies
└── *.html                  # Wrapped Story visualization interface
```

---

### 4. Quickstart & Deployment

#### a. Environment Setup & Dependencies:

```bash
pip install -r requirements.txt
```

#### b. Environment Variables (.env):

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=wrapped_db
GEMINI_API_KEY=your_gemini_api_key
```

#### c. Initialize Database Schema:

```bash
python init_quiz_db.py
```

#### d. Launch API Server:

```bash
# Terminal 1: Start API Server
uvicorn main:app --reload

# Terminal 2: Expose Public Ingress Tunnel
ngrok http 8000
```
