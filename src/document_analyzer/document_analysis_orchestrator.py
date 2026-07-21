from src.common.document.analysis_document import AnalysisDocument

class DocumentAnalysisOrchestrator:
    
    def __init__(self,
        summary_service,
        quiz_service = None,
        flashcard_service = None,
        translation_service = None,
        metadata_service = None):
        self.summary_service = summary_service
        self.quiz_service = quiz_service
        self.flashcard_service = flashcard_service
        self.translation_service = translation_service
        self.metadata_service = metadata_service
        
    def execute(self,
                document,
                action):
        
        match action:
            case "summary":
                if self.summary_service is None:
                    raise ValueError("SummaryService is not configured.")
                return self.summary_service.generate(document)
                
          
            case _:
                raise ValueError(
                    f"Unsupported action: {action}")