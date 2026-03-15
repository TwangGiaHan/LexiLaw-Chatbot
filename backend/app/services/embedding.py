import asyncio
from functools import partial
from sentence_transformers import SentenceTransformer
from app.core.config import settings

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer("BAAI/bge-m3")

    async def encode_query(self, query_text: str):
        loop = asyncio.get_running_loop()
        func = partial(self.model.encode, query_text, normalize_embeddings=True)
        vector = await loop.run_in_executor(None, func)
        return vector.tolist()

embedding_service = EmbeddingService()