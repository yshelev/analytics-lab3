from src.config import Config
import aiohttp

class LLMQueryService: 
    def __init__(self, llm_config: Config, model: str = "llama3-70b-8192"):
        self.llm_config = llm_config
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {self.llm_config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        
    async def proccess_query(self, system_prompt: str, user_prompt: str) -> str: 
        payload = {
            "model": self.model, 
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.2,  
            "max_tokens": 400, 
            "response_format": {"type": "json_object"}
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload,
                    timeout=30
                ) as response:
                    response.raise_for_status()
                    result = await response.json()
                    content = result['choices'][0]['message']['content']
                    
                    if content is None:
                        return None, "Модель не дала ответ"
                    return content, None
                    
            except Exception as e:
                return None, f"Возникла ошибка {e}"