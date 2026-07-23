import logging

from src.common.document.analysis_document import AnalysisDocument
from src.common.config.configuration import Configuration
from src.common.config.configuration_loader import ConfigurationLoader
from src.common.llm.llm_factory import LLMFactory
from src.document_analyzer.action import Action


logger = logging.getLogger(__name__)

class DocumentAnalysisOrchestrator:
    
    def __init__(self,
        llm_service,
        summary_service,
        quiz_service = None,
        flashcard_service = None,
        translation_service = None,
        metadata_service = None):
        self.llm_service=llm_service
        self.summary_service = summary_service
        self.quiz_service = quiz_service
        self.flashcard_service = flashcard_service
        self.translation_service = translation_service
        self.metadata_service = metadata_service
        
    def execute(self,
                document: AnalysisDocument,
                action: Action):
        
        match action:
            case Action.SUMMARY:
                if self.summary_service is None:
                    raise ValueError("SummaryService is not configured.")
                return self.__summarize(document=document)
                
          
            case _:
                raise ValueError(
                    f"Unsupported action: {action}")
                
                
    def __summarize(self,document) -> str:
        prompt=self.summary_service.generate_prompt(document=document)
        
        response: str=self.llm_service.invoke(prompt)
        return response

    