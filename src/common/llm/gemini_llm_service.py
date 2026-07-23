from src.common.llm.llm_service import LLMService
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv


 # Load environment variables from .env
load_dotenv()

# Read the API key
api_key = os.getenv("GEMINI_API_KEY")
#model = "gemini-2.5-flash"


class GeminiLLMService(LLMService):
    
    def __init__(self, model):
        self.model=model
        self.llm=ChatGoogleGenerativeAI(model=model,google_api_key=api_key)
        
    def invoke(self, prompt) -> str:
        return self.llm.invoke(prompt).content