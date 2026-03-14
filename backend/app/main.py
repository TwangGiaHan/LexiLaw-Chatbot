# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.api import router
# from app.config import settings

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.ALLOW_ORIGINS,
#     allow_credentials=True,
#     allow_methods=['*'],
#     allow_headers=['*'],
# )

# app.include_router(router)

# @app.head('/health')
# @app.get('/health')
# def health_check():
#     return 'ok'


from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.neo4j import neo4j_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Kiểm tra kết nối hoặc khởi tạo gì đó nếu cần
    yield
    # Shutdown: Đóng các kết nối dài hạn
    await neo4j_client.close()

app = FastAPI(lifespan=lifespan)