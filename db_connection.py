# db_connection.py
import os
from pathlib import Path
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# 1. Tự động load file .env nằm cùng thư mục dự án
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

# 2. Đọc biến môi trường (với giá trị mặc định fallback an toàn)
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', '')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'xmen_wrapped')

safe_password = quote_plus(DB_PASS)

ENGINE_OPTIONS = {
    "pool_recycle": 1800,
    "pool_pre_ping": True,
    "pool_size": 10,
    "max_overflow": 20
}

_engines = {}
def get_engine(db_name=None):
    """
    Tạo hoặc tái sử dụng engine kết nối.
    - Nếu truyền db_name: Kết nối đích danh database đó.
    - Nếu db_name='': Kết nối tới MySQL Server không gắn liền với database nào (dùng để tạo DB mới).
    - Nếu không truyền gì: Kết nối tới DB mặc định trong .env.
    """
    target_db = DB_NAME if db_name is None else db_name
    
    if target_db not in _engines:
        db_path = f"/{target_db}" if target_db else ""
        url = f"mysql+mysqlconnector://{DB_USER}:{safe_password}@{DB_HOST}:{DB_PORT}{db_path}?charset=utf8mb4"
        _engines[target_db] = create_engine(url, **ENGINE_OPTIONS)
        
    return _engines[target_db]

def test_connection():
    try:
        # Thử kết nối không cần chỉ định database trước
        engine = get_engine(db_name='')
        with engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION(), NOW();")).fetchone()
            print(f"[+] Kết nối MySQL thành công! Phiên bản: {result[0]} | Giờ server: {result[1]}")
            return True
    except Exception as e:
        print(f"[!] Lỗi kết nối MySQL: {e}")
        return False

if __name__ == '__main__':
    test_connection()
