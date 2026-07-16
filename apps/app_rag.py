import streamlit as st 
import tempfile
from src.rag.rag_service import RAGService
from src.llm.llm_service import LLMService

st.write("Welcome To RAG Service")

uploaded_file=st.file_uploader("Upload the PDF File:",
                               type="PDF")
  
if "rag_service" not in st.session_state:
    st.session_state["rag_service"]=RAGService() 
llm_service=LLMService()
if("llm_service") not in st.session_state:
    st.session_state["llm_service"]=llm_service    

if st.button("Load Document"):
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False,
                                     suffix=".pdf"
                                     ) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            pdf_path=tmp_file.name
        with st.spinner("Loading the document"):
            documents= st.session_state["rag_service"].load_pdf_document(pdf_path)
            st.write(documents[0])
            # for document in documents:
            #     st.write(f"Page: {document.metadata["page"]}")
            #     st.write(document.page_content) 
            st.session_state["documents"]=documents
    else:
        st.write("You must select first the pdf file")
        
#Splitter
if st.button("Splitt Document"):
    if "documents" not in st.session_state:
        st.write("You must first load the document")
    else:
       with st.spinner("Splitting the document"):
           chunks = st.session_state["rag_service"].split_document(st.session_state["documents"])
           st.session_state["chunks"]=chunks
           st.write(f"Total chunk pages {chunks[0].metadata['total_pages']}")
        #  for chunk in chunks:
        #        st.divider()
        #        st.write(f"Chunk Page is: {chunk.metadata['page']}")
        #        st.write(chunk.page_content) 
          
           #st.write(f"Here are the chunks: {chunks}")
          
question = st.text_input("Your Question:") 
if st.button("Search without RAG Service"):
    if question:
        with st.spinner("Searching ..."):
            response=st.session_state["llm_service"].ask(question)
            st.write(response.content)
    else:
        st.write("You must enter the question first")          
if st.button("Search with RAG Service"):
    if "documents" not in st.session_state:
        st.write("Please load first the document")  
    else:
        if question:
            chunks=st.session_state["rag_service"].split_document(st.session_state["documents"])
            embedd=st.session_state["rag_service"].embed_chunks(chunks)
            vector_store=st.session_state["rag_service"].store_in_vector_db(chunks,embedd)
            results=st.session_state["rag_service"].similarity_search(vector_store,question)
            st.write(f"Similarity Search delivers: {results}")
        else:
            st.write("You must enter the question first") 
                