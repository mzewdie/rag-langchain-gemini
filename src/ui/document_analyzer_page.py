import streamlit as st 
import tempfile
import logging

from src.common.document.pdf_loader import PDFLoader
from src.common.document.analysis_document import AnalysisDocument
from src.document_analyzer.summary_service import SummaryService
from src.common.config.configuration_loader import ConfigurationLoader
from src.common.config.configuration import Configuration
from src.common.llm.llm_factory import LLMFactory
from src.common.llm.llm_service import LLMService
from src.document_analyzer.document_analysis_orchestrator import DocumentAnalysisOrchestrator
from src.document_analyzer.action import Action
from src.common.utils.logging_config import configure_logging


    
configure_logging()
logger = logging.getLogger(__name__)

st.title("AI Document Analyzer")

uploaded_file=st.file_uploader("Upload PDF",
                 "pdf")


selected_action = st.selectbox(
    "Action",
    [
        "Summarize",
        "Quiz",
        "Flashcards",
        "Translation",
    ]
)

summary_button = st.button("Generate Summary")
#expander=st.expander("Summary:")

if summary_button:
    if not uploaded_file:
        st.error("Please upload the document to be summarised!")
    else:
        with tempfile.NamedTemporaryFile(delete=False,
                                         suffix=".pdf"
                                        ) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    pdf_path=tmp_file.name
                    logger.info(f"pdf file is {pdf_path}")
        with st.spinner("Summarizing the document ..."):
            pdfloader=PDFLoader()
            analysis_document:AnalysisDocument=pdfloader.load(pdffile=pdf_path)
            summary_service=SummaryService()
            configuration: Configuration = ConfigurationLoader.load()
            llm_service:LLMService=LLMFactory.create(configuration.llm)
            document_analysis_orchestrator=DocumentAnalysisOrchestrator(llm_service=llm_service,
                                                                       summary_service=summary_service)
            logger.info(f"Document extracted und to analyse: {analysis_document.content[:300]}")
            response=document_analysis_orchestrator.execute(document=analysis_document,action=Action.SUMMARY)
            #expander.write(response)
            if response:
                with st.expander("Summary"):
                    st.markdown(response)
            


