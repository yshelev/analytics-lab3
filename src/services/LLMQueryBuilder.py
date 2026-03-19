class LLMQueryBuilder: 
    def __init__(self, system_prompt: str, user_prompt_base: str):
        self.system_prompt = system_prompt
        self.user_prompt_base = user_prompt_base

    def build(self, msg: str) -> dict: 
        user_prompt = self.user_prompt_base.format(
            msg=msg
        )
        
        return {
            "user_prompt": user_prompt, 
            "system_prompt": self.system_prompt
        }