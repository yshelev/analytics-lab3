from src.services.LLMQueryService import LLMQueryService
from src.services.LLMQueryBuilder import LLMQueryBuilder
from src.config import Config
from src.constants import user_prompt_base, system_prompt 
import pandas as pd
import json

class LLMService: 
    query_service: LLMQueryService 
    query_builder: LLMQueryBuilder
    
    def __init__(self):
        self.input_filename = "data/input.csv"
        self.output_filename = "data/output.csv"
        
        llm_config = Config()
        
        self.query_builder = LLMQueryBuilder(
            system_prompt=system_prompt,
            user_prompt_base=user_prompt_base
        )
        
        self.query_service = LLMQueryService(
            llm_config=llm_config
        )
    
    async def proccess_msg(self, msg: str) -> bool: 
        prompt = self.query_builder.build(msg)
        
        response, error = await self.query_service.proccess_query(prompt["system_prompt"], prompt["user_prompt"])
        
        return error if error else response
        