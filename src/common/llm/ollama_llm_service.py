from src.common.llm.llm_service import LLMService



class OllamaLLMService(LLMService):
    
    def __init__(self,model):
        self.model=model
        
    def invoke(self, prompt):
        return super().invoke(prompt)
    