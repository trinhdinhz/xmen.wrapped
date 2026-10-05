# init_quiz_db.py
from sqlalchemy import text
from db_connection import get_engine

# 0. SCHEMA DEFINITION
CREATE_SCHEMA = """
CREATE SCHEMA IF NOT EXISTS xmen_wrapped DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
"""

# 1. TEST RESULTS & WRAPPED RECORDS TABLE
CREATE_QUIZ_RECORDS_TABLE = """
CREATE TABLE IF NOT EXISTS xmen_wrapped.xmen_quiz_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL UNIQUE,
    user_age INT NOT NULL,
    hair_stress_age INT NOT NULL,
    delta_age INT NOT NULL,
    grooming_iq INT NOT NULL,
    archetype_code VARCHAR(50) NOT NULL,
    archetype_title VARCHAR(100) NOT NULL,
    scalp_profile VARCHAR(50) NOT NULL,
    exposure_level VARCHAR(20) NOT NULL,
    root_solving_pct DECIMAL(5, 2) NOT NULL,
    fragrance_masking_pct DECIMAL(5, 2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    raw_answers JSON NOT NULL,
    scoring_data JSON NOT NULL,
    llm_payload JSON NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_archetype (archetype_code),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

# 2. AUDIO TRACKS REPOSITORY TABLE
CREATE_TRACKS_TABLE = """
CREATE TABLE IF NOT EXISTS xmen_wrapped.tracks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    artist VARCHAR(100) NOT NULL,
    artist_portrait_url VARCHAR(500) NOT NULL,
    cover_url VARCHAR(500) NOT NULL,
    cut_url VARCHAR(500) NOT NULL,
    full_url VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

# 3. SEED DATA FOR TRACKS
SEED_TRACKS_SQL = """
INSERT INTO xmen_wrapped.tracks (id, title, artist, artist_portrait_url, cover_url, cut_url, full_url)
VALUES 
(1, 'Crawl Outta Love', 'ILLENIUM feat. Annika Wells', 
 'https://res.cloudinary.com/kjby7u78/image/upload/v1790027592/crawlouttalovea.jpg', 
 'https://res.cloudinary.com/kjby7u78/image/upload/v1790027331/crawlouttaloveb.jpg', 
 'https://res.cloudinary.com/kjby7u78/video/upload/v1790017614/crawlouttalovecut.mp3',
 'https://res.cloudinary.com/kjby7u78/video/upload/v1790017615/crawlouttalovefull.mp3'),
(2, 'Crash', 'Jason Ross & Lin Was Here', 
 'https://res.cloudinary.com/kjby7u78/image/upload/v1790110647/crasha.jpg', 
 'https://res.cloudinary.com/kjby7u78/image/upload/v1790110648/crashb.jpg', 
 'https://res.cloudinary.com/kjby7u78/video/upload/v1790110643/crashcut.mp3',
 'https://res.cloudinary.com/kjby7u78/video/upload/v1790110643/crashfull.mp3'),
(3, 'Lost With You', 'Far Out feat. Ruby Chase', 
 'https://res.cloudinary.com/kjby7u78/image/upload/v1790110066/lostwithyoua.jpg', 
 'https://res.cloudinary.com/kjby7u78/image/upload/v1790110020/lostwithyoub.jpg', 
 'https://res.cloudinary.com/kjby7u78/video/upload/v1790110008/lostwithyoucut.mp3', 
 'https://res.cloudinary.com/kjby7u78/video/upload/v1790110009/lostwithyoufull.mp3')
ON DUPLICATE KEY UPDATE 
    title = VALUES(title),
    artist = VALUES(artist),
    artist_portrait_url = VALUES(artist_portrait_url),
    cover_url = VALUES(cover_url),
    cut_url = VALUES(cut_url),
    full_url = VALUES(full_url);
"""

def init_all_database():
    # Step 1: Establish a server-level connection (without targeting a specific DB) to ensure schema existence
    server_engine = get_engine(db_name='')
    with server_engine.begin() as conn:
        conn.execute(text(CREATE_SCHEMA))
        print("[+] Schema `xmen_wrapped` verified/initialized successfully!")

    # Step 2: Connect directly to `xmen_wrapped` to initialize tables and populate seed data
    app_engine = get_engine('xmen_wrapped')
    with app_engine.begin() as conn:
        # Initialize quiz records table
        conn.execute(text(CREATE_QUIZ_RECORDS_TABLE))
        print("[+] Table `xmen_quiz_records` initialized successfully!")

        # Initialize audio tracks repository table
        conn.execute(text(CREATE_TRACKS_TABLE))
        print("[+] Table `tracks` initialized successfully!")

        # Populate initial seed data
        conn.execute(text(SEED_TRACKS_SQL))
        print("[+] Seed data populated into `tracks` successfully!")

if __name__ == '__main__':
    init_all_database()
