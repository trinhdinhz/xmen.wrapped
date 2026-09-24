import os
import sys
from pathlib import Path
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text

# 1. Tự động tìm file .env (quét từ thư mục hiện tại lên các thư mục cha)
CURRENT_FILE = Path(__file__).resolve()
CURRENT_DIR = CURRENT_FILE.parent

def find_and_load_env():
    # Quét ngược lên 4 cấp thư mục cha để tìm .env
    search_dirs = [CURRENT_DIR, CURRENT_DIR.parent, CURRENT_DIR.parent.parent, Path.cwd()]
    for directory in search_dirs:
        env_file = directory / '.env'
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, val = line.split('=', 1)
                        os.environ[key.strip()] = val.strip().strip("'\"")
            return env_file
    return None

loaded_env_path = find_and_load_env()

# 2. Đọc biến môi trường
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', '')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = os.getenv('DB_PORT', '3306')

DB_NAME_SANDBOX = os.getenv('DB_NAME_SANDBOX', 'personal_finance_sandbox')
DB_NAME_REAL = os.getenv('DB_NAME_REAL', 'personal_finance')
DB_NAME_ML = os.getenv('DB_NAME_ML', 'machinelearning_sandbox')

safe_password = quote_plus(DB_PASS)

ENGINE_OPTIONS = {
    "pool_recycle": 1800,
    "pool_pre_ping": True,
    "pool_size": 10,
    "max_overflow": 20
}

def _create_db_engine(db_name):
    url = f"mysql+mysqlconnector://{DB_USER}:{safe_password}@{DB_HOST}:{DB_PORT}/{db_name}?charset=utf8mb4"
    return create_engine(url, **ENGINE_OPTIONS)

_engines = {}

def get_engine(env='real'):
    """
    - get_engine('real') / 'prod': Database chính personal_finance
    - get_engine('sandbox'): Database personal_finance_sandbox
    - get_engine('ml_sandbox') / 'ml': Database machinelearning_sandbox
    """
    env_str = str(env).lower()
    if env_str in ['real', 'prod', 'production', 'main']:
        db_name = DB_NAME_REAL
    elif env_str in ['ml_sandbox', 'ml', 'machinelearning']:
        db_name = DB_NAME_ML
    else:
        db_name = DB_NAME_SANDBOX

    if db_name not in _engines:
        _engines[db_name] = _create_db_engine(db_name)
        
    return _engines[db_name]

def test_connection(env='real'):
    engine = get_engine(env)
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT DATABASE(), NOW();")).fetchone()
            print(f"[+] Đã load .env từ: {loaded_env_path}")
            print(f"[+] Kết nối OK tới DB: `{result[0]}` | Server Time: {result[1]}")
            return True
    except Exception as e:
        print(f"[!] Lỗi kết nối tới `{env}`: {e}")
        return False

if __name__ == '__main__':
    test_connection('real')