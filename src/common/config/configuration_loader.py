# config.py

import yaml
from pathlib import Path


from .configuration import (
    LLMConfiguration,
    RAGConfiguration,
    Configuration
    
)


class ConfigurationLoader:

    def __init__(
        self,
        configuration: Configuration,):
        self.configuration=configuration

    @staticmethod
    def load(
        path: str = "configs/config.yaml")  -> Configuration:

        with open(path) as file:
            data = yaml.safe_load(file)

        llm_configuration = LLMConfiguration(
            provider=data["llm"]["provider"],
            model=data["llm"]["model"]
        )
        
        rag_configuration = RAGConfiguration(
                    provider=data["rag"]["provider"],
                    model=data["rag"]["model"]
                )
        
        configuration=Configuration(llm=llm_configuration,
                                    rag=rag_configuration)
 
        return configuration