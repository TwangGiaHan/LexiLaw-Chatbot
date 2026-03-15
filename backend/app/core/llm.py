# import google.generativeai as genai
# from app.core.config import settings

# # Cấu hình Google AI SDK
# genai.configure(api_key=settings.GEMINI_API_KEY)

# # Khởi tạo model instance
# llm_model = genai.GenerativeModel(
#     model_name=settings.GEMINI_MODEL,
#     # Bạn có thể thêm system_instruction ở đây hoặc trong Agent logic
# )

# import google.generativeai as genai
# from app.core.config import settings

# genai.configure(api_key=settings.GEMINI_API_KEY)

# def get_chat_model(system_instruction: str):
#     # Sử dụng tính năng native của Gemini để giữ vai trò ổn định
#     return genai.GenerativeModel(
#         model_name=settings.GEMINI_MODEL,
#         system_instruction=system_instruction
#     )

# app/core/llm.py
import os
from typing import Optional, AsyncGenerator
from google import genai
from google.genai import types

_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
_aclient = _client.aio

class ChatModel:
    def __init__(self, system_instruction: Optional[str] = None):
        self.system_instruction = system_instruction or ""

    async def generate_stream(self, user_text: str) -> AsyncGenerator[str, None]:
        # JSON mode không cần cho answer tự do → chỉ text
        cfg = types.GenerateContentConfig(temperature=0.2)
        contents = self.system_instruction + "\n\n" + user_text if self.system_instruction else user_text
        # Google GenAI SDK stream: trả về text nguyên khối (tuỳ bản SDK),
        # fallback: cắt thành chunks giả lập để SSE
        resp = await _aclient.models.generate_content(model=_GEMINI_MODEL, contents=contents, config=cfg)
        text = (resp.text or "")
        step = 500
        for i in range(0, len(text), step):
            yield text[i:i+step]

def get_chat_model(system_instruction: Optional[str] = None) -> ChatModel:
    return ChatModel(system_instruction)