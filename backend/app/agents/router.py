from app.core.llm import get_chat_model
from app.agents.prompts import ROUTER_PROMPT

class RouterAgent:
    async def classify_intent(self, user_query: str, history: list = []) -> str:
        history_context = ""
        if history:
            history_context = "Lịch sử gần đây:\n" + "\n".join([f"{m['role']}: {m['content']}" for m in history])
        
        prompt = f"{ROUTER_PROMPT}\n\n{history_context}\nCâu hỏi hiện tại: {user_query}"
        
        model = get_chat_model()
        client = model["client"]
        response = await client.chat.completions.create(
            model=model["model"],
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )
        intent = response.choices[0].message.content.strip().upper()
        return intent if intent in ["LEGAL_QUERY", "GENERAL_CHAT"] else "LEGAL_QUERY"

router_agent = RouterAgent()