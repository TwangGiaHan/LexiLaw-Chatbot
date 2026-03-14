from qdrant_client import AsyncQdrantClient
from app.core.config import settings

# Khởi tạo client dùng chung
qdrant_client = AsyncQdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
    timeout=60
)