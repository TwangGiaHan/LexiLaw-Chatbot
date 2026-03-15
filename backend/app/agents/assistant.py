import asyncio
from time import time
from app.agents.router import router_agent
from app.agents.researcher import ResearcherAgent
from app.agents.prompts import MAIN_SYSTEM_PROMPT, RAG_SYSTEM_PROMPT
from app.core.llm import get_chat_model
from app.utils.sse_stream import SSEStream
from app.db import add_chat_messages, get_chat_messages

class LegalAssistant:
    def __init__(self, chat_id, rdb, history_size=6):
        self.chat_id = chat_id
        self.rdb = rdb
        self.history_size = history_size
        self.researcher = ResearcherAgent()

    async def _handle_conversation_task(self, message: str, sse: SSEStream):
        try:
            start_time = time()
            raw_history = await get_chat_messages(self.rdb, self.chat_id, last_n=self.history_size)
            formatted_history = [
                {"role": "assistant" if h["role"] == "assistant" else "user", "content": h["content"]}
                for h in raw_history if h.get("content")
            ]
            history_time = time() - start_time
            print(f"Thời gian lấy lịch sử: {history_time:.2f}s")

            intent_start = time()
            intent_task = asyncio.create_task(router_agent.classify_intent(message, formatted_history[-2:] if formatted_history else []))
            context_task = asyncio.create_task(self.researcher.gather_all_evidence(message))
            
            intent, context = await asyncio.gather(intent_task, context_task)
            intent_time = time() - intent_start
            print(f"Thời gian phân loại intent: {intent_time:.2f}s")
            print(f"Thời gian phân loại intent + gather context: {intent_time:.2f}s")

            sys_inst = MAIN_SYSTEM_PROMPT
            if intent == "LEGAL_QUERY":
                context_str = "\n".join([f"[{d['source']}]: {d['content']}" for d in context])
                sys_inst = f"{RAG_SYSTEM_PROMPT}\n\nNGỮ CẢNH PHÁP LUẬT:\n{context_str}"

            model_start = time()
            model = get_chat_model(system_instruction=sys_inst)
            client = model["client"]
            chat_messages = []
            if model["system_instruction"]:
                chat_messages.append({"role": "system", "content": model["system_instruction"]})
            chat_messages.extend(formatted_history)
            chat_messages.append({"role": "user", "content": message})
            model_time = time() - model_start
            print(f"Thời gian khởi tạo model: {model_time:.2f}s")

            stream_start = time()
            full_response = ""
            response = await client.chat.completions.create(
                model=model["model"],
                messages=chat_messages,
                stream=True
            )
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    await sse.send(content)
                    full_response += content
            stream_time = time() - stream_start
            print(f"Thời gian stream response: {stream_time:.2f}s")

            # Redis
            save_start = time()
            await add_chat_messages(self.rdb, self.chat_id, [
                {'role': 'user', 'content': message, 'created': int(time())},
                {'role': 'assistant', 'content': full_response, 'created': int(time())}
            ])
            save_time = time() - save_start
            print(f"Thời gian lưu Redis: {save_time:.2f}s")

            total_time = time() - start_time
            print(f"Tổng thời gian: {total_time:.2f}s")

        except Exception as e:
            print(f"Error in conversation task: {str(e)}")
            import traceback
            traceback.print_exc()
            await sse.send(f"Lỗi: {str(e)}")
        finally:
            await sse.close()

    def run(self, message: str):
        sse = SSEStream()
        asyncio.create_task(self._handle_conversation_task(message, sse))
        return sse