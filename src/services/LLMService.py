import os
import pandas as pd
from langchain_groq import ChatGroq
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

from src.config import Config
from src import constants

class LLMService:
    """Сервис анализа данных через LangChain + Groq."""
    
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            model_name=Config.MODEL,
            api_key=Config.GROQ_API_KEY,
        )
        self.agent = None
        self.current_df = None
    
    def _build_prefix(self, context: str = "") -> str:
        """Собрать системный префикс для агента."""
        return constants.PREFIX_TEMPLATE.format(
            roles=constants.ROLES_AND_SAFETY,
            guide=constants.ANALYSIS_GUIDE,
            context=context or "Проведи полный EDA анализ"
        )
    
    def init_agent(self, df: pd.DataFrame, context: str = ""):
        """Инициализировать агента с новым датасетом."""
        self.current_df = df
        
        self.agent = create_pandas_dataframe_agent(
            self.llm,
            df,
            agent_type="zero-shot-react-description",
            allow_dangerous_code=True,  
            prefix=self._build_prefix(context),
            max_iterations=5,  
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
    
    async def proccess_msg(self, text: str) -> str:
        return "Отправьте файл с данными для анализа"