import logging
from src.common.document.pdf_loader import PDFLoader
from pathlib import Path
from src.common.utils.logging_config import configure_logging
from src.document_analyzer.summary_service import SummaryService
from src.document_analyzer.document_analysis_orchestrator import DocumentAnalysisOrchestrator
from src.common.llm.llm_configuration import LLMConfiguration
from src.common.llm.llm_factory import LLMFactory



configure_logging()
logger = logging.getLogger(__name__)

print(logger.isEnabledFor(logging.INFO))
print(logger.name)
print(logger.level)
print(logger.parent.level)



pdf_file=Path("data/introduction-to-nutrition.pdf")
#pdf_file=Path("data/PythonProgramming.pdf")
pdfloader=PDFLoader()
analysis_document=pdfloader.load(pdffile=pdf_file)
logger.info("PDF loaded successfully")
#logger.info(analysis_document)

""" logger.info("START")
logger.info(analysis_document.filename)
logger.info(len(analysis_document.content))
logger.info(len(str(analysis_document)))
logger.info("END") """

print("printing: {analysis_document}")
#logger.info(analysis_document)

summary_service=SummaryService()
action="summary"
document_analysis_orchestrator = DocumentAnalysisOrchestrator(summary_service=summary_service)
result=document_analysis_orchestrator.execute(document=analysis_document,action=action)

#LLM Service
llm_configuration = LLMConfiguration("gemini","gemini-2.5-flash")
#llm_factory= LLMFactory()
llm_service=LLMFactory.create(llm_configuration)
llm_service.invoke("What is Python?")