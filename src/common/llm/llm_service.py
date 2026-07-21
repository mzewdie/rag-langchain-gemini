
from abc import ABC, abstractmethod

class LLMService(ABC):
    
    @abstractmethod
    def invoke(self,
               prompt: str
               ) ->str:
        pass
    
    