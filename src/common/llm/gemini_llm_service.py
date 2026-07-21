from src.common.llm.llm_service import LLMService


class GeminiLLMService(LLMService):
    
    def __init__(self, model):
        self.model=model
        
    def invoke(self, prompt):
        print(f"GeminiLLMService invoked with prompt {prompt}")
        return super().invoke(prompt)