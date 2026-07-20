import streamlit as st
from src.rag.rag_service_v2 import RAGService
import tempfile
import pdb
from src.exceptions.exceptions import EmbeddingQuotaExceededError

#pdb.set_trace()

st.title("Welcome To RAG Administration ")

uploaded_file=st.file_uploader("Upload the PDF File:",
                               type="PDF")
chunk_size = st.number_input(
    "Chunk Size",
    value=5000,
    step=100
)

chunk_overlap = st.number_input(
    "Chunk Overlap",
    value=200,
    step=50
)

if "rag_service" not in st.session_state:
    st.session_state["rag_service"]=RAGService(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
rag_service:RAGService = st.session_state["rag_service"]    

if st.button("Add Document to Vector DB"):
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False,
                                     suffix=".pdf"
                                     ) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            pdf_path=tmp_file.name
            with st.spinner("Storing the document in the vector data base"):
                try:
                    stats = (rag_service.store_pdf_document_in_db(pdf_path,uploaded_file.name))
                    st.success(f"Document {uploaded_file.name} is succefully stored in the vector database")
                    st.write(f"Pages: {stats['pages']}")
                    st.write(f"Chunks: {stats['chunks']}")
                except EmbeddingQuotaExceededError as ex:
                    if ex.retry_after:
                        st.warning(
                            f"Embedding quota exceeded. "
                            f"Please try again in {ex.retry_after} seconds.")
                    else:
                        st.warning("Embedding quota exceeded. "
                                   "Please check your Google quota.")           
                except Exception as ex:
                    st.error(str(ex))
                    
    else:
        st.write("Please select the document first")   