import pandas as pd
from langchain_groq import ChatGroq
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

from config import Config
import constants

class LLMService:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.05,
            model_name=Config.MODEL,
            api_key=Config.GROQ_API_KEY,
        )
        self.agent = None
        self.current_df = None
    
    def _build_prefix(self, context: str = "") -> str:
        return constants.PREFIX_TEMPLATE.format(
            roles=constants.ROLES_AND_SAFETY,
            guide=constants.ANALYSIS_GUIDE,
            context=context or "Проведи полный EDA анализ"
        )
    
    def init_agent(self, df: pd.DataFrame, context: str = ""):
        self.current_df = df
        
        self.agent = create_pandas_dataframe_agent(
            self.llm,
            df,
            agent_type="openai-tools",
            allow_dangerous_code=True,  
            prefix=self._build_prefix(context),
            early_stopping_method="generate", 
            max_iterations=10,  
            handle_parsing_errors=True,
        )
    
    async def analyze(self, query: str) -> dict:
        if not self.agent:
            return {
                "output": "Агент не инициализирован. Сначала загрузите данные.",
                "ok": False
            }
        
        full_query = constants.USER_QUERY_TEMPLATE.format(query=query)
        
        try:
            result = self.agent.invoke({"input": full_query})
            return {
                "output": result.get("output", "Нет результата"),
                "ok": True
            }
        except Exception as e:
            return {
                "output": f"Ошибка анализа: {str(e)}",
                "ok": False
            }