# xmen.wrapped

Hệ thống tổng hợp hành vi người dùng và phân tích dữ liệu cá nhân hóa (Personalized Data Storytelling & Archetype Profiling), xây dựng trên kiến trúc bất đồng bộ (Async Backend) tích hợp LLM và kho lưu trữ đa phương tiện tối ưu hóa CDN.

---

### 1. Tính năng cốt lõi & Tư duy Kiến trúc (Key Engineering Highlights)

* **Behavioral Archetype & Scoring Engine (`quiz_scoring.py`, `quiz_metadata.py`):** 
  Thuật toán phân tích phản hồi hành vi, tính toán trọng số tương tác và định danh chân dung người dùng (User Persona Clustering) phục vụ chiến dịch cá nhân hóa nội dung số.
* **LLM Integration & Dynamic Content (`gemini_quiz_engine.py`, `gemini_client.py`):** 
  Xây dựng wrapper chuẩn hóa tương tác với Google GenAI SDK, tối ưu hóa Prompt Engineering để sinh nội dung tương tác theo ngữ cảnh thời gian thực.
* **Async Backend & Connection Pooling (`main.py`, `db_connection.py`):** 
  Backend hiệu năng cao phát triển trên FastAPI + Uvicorn; quản lý vòng đời truy vấn qua SQLAlchemy Connection Pooling nhằm tối ưu thông lượng (Throughput) và cách ly tải trọng cơ sở dữ liệu.
* **Media Delivery Pipeline & Data Visualization (`*.html`):** 
  Đồng bộ hóa metadata và đường dẫn media đám mây (Cloudinary CDN), giảm thiểu tải trọng tĩnh (Payload Size) để tối ưu thời gian phản hồi (Low-Latency UI Delivery).

---

### 2. Tech Stack

* **Backend:** Python 3.10+, FastAPI, Uvicorn, Pydantic v2
* **Database & ORM:** MySQL, SQLAlchemy (Engine & Session Pooling), PyMySQL
* **AI & LLM Services:** Google GenAI SDK (`google-genai`)
* **Storage & CDN:** Cloudinary CDN
* **Networking & Tunneling:** ngrok (Public Ingress Tunneling), HTTPX, Requests

---

### 3. Cấu Trúc Repository

```text
├── db_connection.py        # Quản trị Pool kết nối MySQL & SQLAlchemy Session
├── gemini_client.py        # Client Wrapper cấu hình Google GenAI SDK
├── gemini_quiz_engine.py   # Engine xử lý logic sinh nội dung & Dynamic Prompts
├── quiz_scoring.py         # Thuật toán tính điểm & phân loại User Persona
├── quiz_metadata.py        # Metadata schemas, cấu hình luật chấm và archetype
├── init_quiz_db.py         # Data Definition Script (DDL) khởi tạo schema DB
├── main.py                 # FastAPI Application Entrypoint & RESTful Routing
├── requirements.txt        # Danh mục quản lý thư viện phụ thuộc (Dependencies)
└── *.html                  # Giao diện trực quan hóa dữ liệu (Wrapped Story UI)
```

---

### 4. Cài đặt & Triển khai (Quickstart)

#### a. Khởi tạo môi trường & Cài đặt phụ thuộc:

```bash
pip install -r requirements.txt
```

#### b. Cấu hình môi trường (.env):

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=wrapped_db
GEMINI_API_KEY=your_gemini_api_key
```

#### c. Khởi tạo Database Schema:

```bash
python init_quiz_db.py
```

#### d. Khởi chạy máy chủ API:

```bash
# Terminal 1: Chạy API Server
uvicorn main:app --reload

# Terminal 2: Mở tunnel truy cập public
ngrok http 8000
```
