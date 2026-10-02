# xmen.wrapped

Nền tảng tương tác tổng kết hành vi & AI Quiz Engine được xây dựng trên nền tảng **FastAPI**, **Gemini AI** và **MySQL/Cloudinary**, hoàn thành trọn gói (End-to-End) trong 3 ngày (20/09/2026 – 24/09/2026).

---

## Tính năng cốt lõi (Key Highlights)
* **AI Quiz Generation & Scoring:** Tích hợp Google Gemini Engine tự động sinh câu hỏi và chấm điểm hành vi theo thời gian thực (`gemini_quiz_engine.py`, `quiz_scoring.py`).
* **High-Performance Backend:** Xây dựng trên nền FastAPI + Uvicorn, xử lý luồng dữ liệu async tối ưu băng thông.
* **Media & Database Pipeline:** Tích hợp SQLAlchemy + PyMySQL kết nối kho lưu trữ media đám mây (Cloudinary CDN).
* **Interactive Frontend:** Hệ thống giao diện trực quan hóa dữ liệu (Wrapped Stories & Quiz Cards).

---

## Tech Stack
* **Backend:** Python 3.10+, FastAPI, Uvicorn, Pydantic v2
* **AI & LLM:** Google GenAI SDK (`google-genai`)
* **Database & Storage:** MySQL (SQLAlchemy, PyMySQL), Cloudinary CDN
* **Networking:** Requests, HTTPX

---

## Cài đặt & Cấu hình (Quickstart)

### 1. Cài đặt thư viện phụ thuộc
pip install fastapi>=0.100.0 uvicorn>=0.22.0 pydantic>=2.0.0 sqlalchemy>=2.0.0 pymysql>=1.1.0 google-genai>=0.1.0 requests>=2.31.0

### 2. Cài đặt Database:
python init_quiz_db.py
