import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv


 # Load environment variables from .env
load_dotenv()

# Read the API key
api_key = os.getenv("GEMINI_API_KEY")
model = "gemini-2.5-flash"



    
class LLMService():
    def __init__(self):
        self.llm=ChatGoogleGenerativeAI(model=model,google_api_key=api_key)
        
    def ask(self,question):
        return self.llm.invoke(question)  
    
    def invoke(self,prompt: str):
        return self.llm.invoke(prompt)