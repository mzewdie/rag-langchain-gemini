import logging
from src.common.document.pdf_loader import PDFLoader
from pathlib import Path
from src.common.utils.logging_config import configure_logging
from src.document_analyzer.summary_service import SummaryService
from src.document_analyzer.document_analysis_orchestrator import DocumentAnalysisOrchestrator
from src.common.llm.llm_configuration import LLMConfiguration
from src.common.llm.llm_factory import LLMFactory
#from src.common.config import Configuration
from src.common.config.configuration import Configuration
from src.common.config.configuration_loader import ConfigurationLoader
from src.document_analyzer.document_analysis_orchestrator import DocumentAnalysisOrchestrator
from src.document_analyzer.action import Action

def test_llm():
    """ 
    print(logger.isEnabledFor(logging.INFO))
    print(logger.name)
    print(logger.level)
    print(logger.parent.level) 
    """



    #pdf_file=Path("data/introduction-to-nutrition.pdf")
    pdf_file=Path("data/PythonProgramming.pdf")
    pdfloader=PDFLoader()
    analysis_document=pdfloader.load(pdffile=pdf_file)
    logger.info("PDF loaded successfully")
    #logger.info(analysis_document)

    """ 
logger.info("START")
logger.info(analysis_document.filename)
logger.info(len(analysis_document.content))
logger.info(len(str(analysis_document)))
logger.info("END") 
"""

    print("printing: {analysis_document}")
    #logger.info(analysis_document)

    summary_service=SummaryService()
    action="summary"
    document_analysis_orchestrator = DocumentAnalysisOrchestrator(summary_service=summary_service)
    result=document_analysis_orchestrator.execute(document=analysis_document,action=action)

    #using the configuration
    document_analysis_orchestrator=DocumentAnalysisOrchestrator()
    document_analysis_orchestrator.execute

    configuration = ConfigurationLoader.load()
    llm_service=LLMFactory.create(configuration.llm)
    llm_service.invoke("What is Python?")
    llm_service.invoke(analysis_document,action,prompt)
   
   
   
   
   
    
configure_logging()
logger = logging.getLogger(__name__)




#usage of the llm
""" pdf_file=Path("data/introduction-to-nutrition.pdf")
#pdf_file=Path("data/PythonProgramming.pdf")
pdfloader=PDFLoader()
analysis_document=pdfloader.load(pdffile=pdf_file)
summary_service=SummaryService()
prompt=summary_service.generate_prompt(document=analysis_document)
configuration = ConfigurationLoader.load()
llm_service=LLMFactory.create(configuration.llm)
response=llm_service.invoke(prompt)
logger.info(f"Summary of the document: {response.content}") """

pdf_file=Path("data/introduction-to-nutrition.pdf")
pdfloader=PDFLoader()
analysis_document=pdfloader.load(pdffile=pdf_file)
summary_service=SummaryService()
configuration: Configuration = ConfigurationLoader.load()
llm_service=LLMFactory.create(configuration.llm)
document_analysis_orchestrator=DocumentAnalysisOrchestrator(llm_service=llm_service,summary_service=summary_service)

response=document_analysis_orchestrator.execute(document=analysis_document,action=Action.SUMMARY)
logger.info(f"Summarized document is: {response} ")


