from dataclasses import dataclass

@dataclass
class LLMConfiguration:
    
    provider: str
    model: str
    
    