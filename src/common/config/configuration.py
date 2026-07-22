from dataclasses import dataclass

@dataclass
class LLMConfiguration:
    provider: str
    model: str

@dataclass
class RAGConfiguration:
    provider: str
    model: str



@dataclass
class Configuration:
    llm: LLMConfiguration
    rag: RAGConfiguration
    
    
    
    
    