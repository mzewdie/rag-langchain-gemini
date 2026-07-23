from src.common.document.analysis_document import AnalysisDocument
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from pathlib import Path
#from src.common.utils.logging_config import configure_logging
import logging


logger = logging.getLogger(__name__)
    
class PDFLoader:
    def __init__(self):
        pass
    
    def load(self,pdffile: Path) -> AnalysisDocument:
        loader: PyPDFLoader = PyPDFLoader(pdffile)
        loadedPDF: list[Document] =loader.load()
        
        #logger.info(f"Loaded PDF Document: {loadedPDF}")
        
        content = "\n\n".join(doc.page_content 
                              for doc in loadedPDF)
        metadata={}
        metadata["total_pages_loaded"] = len(loadedPDF)
        
        analysis_document = AnalysisDocument(filename=pdffile,
                                    content=content,
                                    document_type="pdf",
                                    pages=len(loadedPDF),
                                    metadata=metadata)
        #logger.info(f"Converted Anlalysis Document: {analysis_document}")
        #use __repr__ with %r
        logger.info("%r",analysis_document)
        #logger.info(f"log info: {analysis_document}")
        
        logger.info("Loaded document: %s",analysis_document)
        logger.debug("Document details: %r",analysis_document)
        return analysis_document