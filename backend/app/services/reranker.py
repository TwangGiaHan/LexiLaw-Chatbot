import asyncio
from functools import partial
from FlagEmbedding import FlagReranker
from typing import List, Any
import cohere
from app.core.config import settings

class RerankerService:
    def __init__(self):
        self.reranker = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True)

    async def rerank(self, query: str, hits: List[Any], top_k: int = 5):
        if not hits: return []

        pairs = [(query, h.payload["content"]) for h in hits]
        
        loop = asyncio.get_running_loop()
        func = partial(self.reranker.compute_score, pairs)
        scores = await loop.run_in_executor(None, func)
        
        scored_hits = sorted(zip(hits, scores), key=lambda x: x[1], reverse=True)
        
        return [hit for hit, score in scored_hits[:top_k]]

class CohereReranker:
    def __init__(self):
        self.co = cohere.Client(settings.COHERE_API_KEY)

    async def rerank(self, query, initial_hits, top_k=5):
        if not initial_hits: return []
        
        docs = [h.payload['content'] for h in initial_hits]
        
        response = self.co.rerank(
            model='rerank-v3.5',
            query=query,
            documents=docs,
            top_n=top_k
        )
        
        final_results = []
        for res in response.results:
            hit = initial_hits[res.index]
            hit.score = res.relevance_score
            final_results.append(hit)
            
        return final_results

# reranker_service = RerankerService()
reranker_service = CohereReranker()