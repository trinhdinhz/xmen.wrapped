# /Users/anhnt/Documents/pythoncode/warp/init_quiz_db.py
import sys
from pathlib import Path
from sqlalchemy import text

CURRENT_DIR = Path(__file__).resolve().parent
SHARED_CONFIG_PATH = CURRENT_DIR.parent / 'shared_config'
if not SHARED_CONFIG_PATH.exists():
    SHARED_CONFIG_PATH = Path.home() / 'Documents/pythoncode/shared_config'
if str(SHARED_CONFIG_PATH) not in sys.path:
    sys.path.append(str(SHARED_CONFIG_PATH))

from db_connection import get_engine  # type: ignore

# 1. BẢNG KẾT QUẢ TEST & WRAPPED
CREATE_QUIZ_RECORDS_TABLE = """
CREATE TABLE IF NOT EXISTS xmen_quiz_records (
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
    INDEX idx_session (session_id),
    INDEX idx_status (status),
    INDEX idx_archetype (archetype_code),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

# 2. BẢNG TRACKS LƯU DANH SÁCH BÀI HÁT
CREATE_TRACKS_TABLE = """
CREATE TABLE IF NOT EXISTS tracks (
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

# 3. DỮ LIỆU SEED MẪU CHO TRACKS (TỰ ĐỘNG BỎ QUA NẾU ĐÃ CÓ)
SEED_TRACKS_SQL = """
INSERT INTO tracks (id, title, artist, artist_portrait_url, cover_url, cut_url, full_url)
VALUES 
(1, 'Thủ Đô Cypher', 'RPT MCK, Orijinn, Wxrdie', 
 'https://res.cloudinary.com/kjby7u78/image/upload/v1790025881/staytonighta.jpg', 
 'https://res.cloudinary.com/kjby7u78/image/upload/v1790027331/discoveryb.jpg', 
 '/audio/track_1_cut.mp3', '/audio/track_1_full.mp3'),
(2, 'Chìm Sâu', 'RPT MCK (feat. Trung Trần)', 
 'https://res.cloudinary.com/kjby7u78/image/upload/v1790026521/discoverya.jpg', 
 'https://res.cloudinary.com/kjby7u78/image/upload/v1790027332/monsterb.jpg', 
 '/audio/track_2_cut.mp3', '/audio/track_2_full.mp3'),
(3, 'Tại Vì Sao', 'RPT MCK', 
 'https://res.cloudinary.com/kjby7u78/image/upload/v1790027332/staytonightb.jpg', 
 'https://res.cloudinary.com/kjby7u78/image/upload/v1790027331/discoveryb.jpg', 
 '/audio/track_3_cut.mp3', '/audio/track_3_full.mp3')
ON DUPLICATE KEY UPDATE title=VALUES(title);
"""

def init_all_database():
    engine = get_engine('sandbox')
    with engine.begin() as conn:
        # Tạo bảng kết quả bài test
        conn.execute(text(CREATE_QUIZ_RECORDS_TABLE))
        print("[+] Đã khởi tạo bảng `xmen_quiz_records`!")

        # Tạo bảng bài hát tracks
        conn.execute(text(CREATE_TRACKS_TABLE))
        print("[+] Đã khởi tạo bảng `tracks`!")

        # Nạp dữ liệu bài hát
        conn.execute(text(SEED_TRACKS_SQL))
        print("[+] Đã nạp dữ liệu danh sách bài hát vào bảng `tracks`!")

if __name__ == '__main__':
    init_all_database()
