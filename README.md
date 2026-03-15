# LexiLaw - Trợ lý ảo AI Tư vấn Luật Lao động Việt Nam

LexiLaw là một hệ thống RAG (Retrieval-Augmented Generation) được thiết kế chuyên biệt để tư vấn và giải đáp các vấn đề pháp lý liên quan đến Luật Lao động Việt Nam.

Hệ thống tận dụng kiến trúc hiện đại với Frontend React/Vite tốc độ cao, Backend FastAPI xử lý bất đồng bộ mượt mà và sức mạnh của các mô hình LLM hàng đầu (OpenAI).

## 🚀 Tính Năng Nổi Bật

- **Tư vấn Pháp luật Chính xác:** Cung cấp thông tin và giải đáp thắc mắc dựa trên các điều khoản luật lao động thực tế.
- **Hybrid Search RAG:** Kết hợp tìm kiếm Dense Vector (ngữ nghĩa) và Sparse Vector (từ khóa BM25) bằng **Qdrant** để lấy ngữ cảnh chuẩn xác nhất.
- **Re-ranking Đa Ngôn Ngữ:** Sử dụng **Cohere Rerank 3.5** tối ưu hóa thứ hạng kết quả tìm kiếm cho văn bản tiếng Việt.
- **Tích Hợp Knowledge Graph (Đang phát triển):** Lưu trữ và truy vấn mối quan hệ phức tạp giữa các điều luật, quy định và chế tài bằng **Neo4j**.
- **Hỗ trợ Streaming (SSE):** Trải nghiệm phản hồi theo thời gian thực (typing effect) không độ trễ như ChatGPT.
- **Quản lý Ngữ cảnh Đa Phiên:** Lưu trữ lịch sử trò chuyện an toàn bằng **Redis** để duy trì ngữ cảnh cho các luồng chat liên tục.
- **Giao Diện Trực Quan:** Thiết kế tối giản, thân thiện, dễ sử dụng, hoàn toàn tương thích trên mọi thiết bị.

## 🛠 Công Nghệ Sử Dụng

### Frontend
- **Framework:** React 19, Vite
- **Styling:** Tailwind CSS (PostCSS)
- **State Management:** Immer, Use-immer
- **Hiển thị văn bản:** React Markdown

### Backend
- **Framework:** FastAPI (Python 3.10+)
- **LLM:** OpenAI API (`gpt-4o-mini`)
- **Embeddings:** BAAI/bge-m3 (qua `SentenceTransformers`)
- **Vector Database:** Qdrant (Cloud/Local)
- **Graph Database:** Neo4j (Aura Cloud/Local)
- **Caching & Memory:** Redis (Async)

## 📦 Kiến Trúc Hệ Thống (Dockerized)

Dự án được cấu hình bằng Docker và Docker Compose để triển khai dễ dàng thông qua 3 dịch vụ chính:
1. **Frontend:** Nginx phục vụ static file của React/Vite.
2. **Backend:** FastAPI được host qua Uvicorn.
3. **Redis:** Lưu trữ bộ nhớ cache và lịch sử chat.
*(Lưu ý: Qdrant và Neo4j đang được thiết lập sử dụng Cloud instance nhưng có thể config để chạy local map qua `docker-compose`)*.

---

## 🚦 Khởi Chạy Dự Án Bằng Docker

Cách đơn giản nhất để chạy toàn bộ dự án là sử dụng Docker. Hãy cài đặt [Docker](https://www.docker.com/) và [Docker Compose](https://docs.docker.com/compose/) trước khi tiếp tục.

### 1. Cấu hình biến môi trường
Tạo file `.env` bên trong thư mục `backend/` với các thiết lập sau:

```env
# App Config
APP_NAME="LexiLaw RAG Chatbot"
DEBUG=False
ALLOW_ORIGINS="*"

# Qdrant Cloud / Local
QDRANT_URL="<Mã_URL_Qdrant_Của_Bạn>"
QDRANT_API_KEY="<API_Key_Qdrant_Của_Bạn>"
COLLECTION_NAME="legal_laws"
VECTOR_SEARCH_TOP_K=10

# OpenAi LLM
OPENAI_API_KEY="<API_Key_OpenAI_Của_Bạn>"
OPENAI_MODEL="gpt-4o-mini"

# Cohere Rerank
COHERE_API_KEY="<API_Key_Cohere_Của_Bạn>"

# Redis
REDIS_URL="redis://redis:6379/0"

# Neo4j (GraphRAG)
NEO4J_URI="<Neo4j_URI>"
NEO4J_USERNAME="<Neo4j_User>"
NEO4J_PASSWORD="<Neo4j_Password>"
NEO4J_DATABASE="neo4j"
```

### 2. Triển khai với Docker Compose

Tại thư mục gốc của project (nơi chứa file `docker-compose.yml`), chạy lệnh:

```bash
docker-compose up --build -d
```

Các dịch vụ sẽ tự động cài đặt dependency và khởi chạy:
- **Frontend** chạy tại: `http://localhost:3000`
- **Backend API Docs** chạy tại: `http://localhost:8000/docs`

---

## 💻 Chạy Dự Án Thủ Công (Development Mode)

Nếu bạn muốn debug trực tiếp không dùng Docker, hãy làm theo các bước sau.

### 1. Khởi động Redis (Yêu cầu)
Bạn cần một instance Redis đang chạy ở port `6379`.
Trường hợp dùng Docker cài sẵn: `docker run -d -p 6379:6379 redis:7-alpine`

### 2. Chạy Backend
Mở Terminal, di chuyển vào thư mục `backend/` và thực thi:

```bash
# Tạo và kích hoạt môi trường ảo (Khuyên dùng)
python -m venv myenv
source myenv/bin/activate  # Trên Windows: .\myenv\Scripts\activate

# Cài đặt thư viện
pip install -r requirements.txt

# Đảm bảo bạn đã đổi dòng REDIS_URL trong file .env thành LOCAL:
# REDIS_URL="redis://localhost:6379/0"

# Khởi động Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Chạy Frontend
Mở Terminal mới, di chuyển vào thư mục `frontend/` và thực thi:

```bash
# Cài đặt thư viện Nodejs
npm install

# Chạy server phát triển Vite
npm run dev
```
Mở trình duyệt truy cập url được Vite thông báo (thường là `http://localhost:5173`).

---

## 📂 Tổ chức mã nguồn chính

```
LawRAG/
│
├── frontend/                 # Giao diện người dùng
│   ├── src/components/       # Các components React (Chatbot, Message, Input)
│   ├── src/api/              # Các cấu hình gọi API sang Backend
│   ├── Dockerfile            # Cấu hình container Frontend (Node + Nginx)
│   └── package.json
│
├── backend/                  # API và Logic xử lý
│   ├── app/
│   │   ├── agents/           # Logic của Bot: Researcher, Router, Prompts
│   │   ├── core/             # Cấu hình chung (.env loader, neo4j, qdrant, redis, llm)
│   │   ├── services/         # Layer gọi model LLM, embedding, retrieval
│   │   ├── api.py            # Khai báo các Routes / Endpoints
│   │   └── main.py           # Init app FastAPI
│   ├── worker/               # Mã nguồn nạp dữ liệu offline (ingest data)
│   ├── Dockerfile            # Cấu hình container Backend (Python)
│   └── requirements.txt
│
└── docker-compose.yml        # Tích hợp dịch vụ toàn hệ thống
```

---

## Giấy Phép & Tuyên Bố Miễn Trừ Trách Nhiệm

Mặc dù hệ thống LexiLaw sử dụng công nghệ tìm kiếm tiên tiến dựa trên tài liệu Luật Lao động, tuy nhiên các tư vấn do AI sinh ra hoàn toàn **chỉ mang tính chất tham khảo**. Bạn nên đối chiếu và xác minh tính pháp lý với Cơ quan có thẩm quyền hoặc Luật sư chuyên gia trong các quyết định quan trọng.

Dự án này là mã nguồn mở, phục vụ mục đích học thuật và nghiên cứu công nghệ đồ thị kiến thức (Knowledge Graph) kết hợp RAG.
