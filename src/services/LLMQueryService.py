from src.config import Config
import requests
import json

class LLMQueryService: 
    def __init__(self, llm_config: Config, model: str = "nvidia/nemotron-3-nano-30b-a3b"):
        self.llm_config = llm_config
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {self.llm_config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
    def proccess_query(self, system_prompt: str, user_prompt: str) -> str: 
        payload = {
            "model": self.model, 
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.2,  
            "max_tokens": 400
        }
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            if content == None: 
                content = None, 
                error = "Модель не дала ответ"
            else:
                error = None    
        
        except Exception as e: 
                content = None, 
                error = f"Возникла ошибка {e}"
        
        return content, error