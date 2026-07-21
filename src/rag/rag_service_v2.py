
from common.llm.llm_service_v1 import LLMService
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import logging
from common.utils.logging_config import configure_logging
#from pathlib import Path
import re
from src.exceptions.exceptions import EmbeddingQuotaExceededError



"""
Streamlit UI
     |
     v
RAGService
     |
     +-- PDF Loader
     +-- Splitter
     +-- Embeddings
     +-- Chroma
     +-- Retriever
     +-- Prompt Builder
     +-- LLM
"""

configure_logging()
logger = logging.getLogger(__name__)

class RAGService:

    def __init__(self,
                 search_config: dict,
                 chunk_size: int =1000, chunk_overlap: int = 200):

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001")
        self.search_config=search_config
        self.chunk_size=chunk_size
        self.chunk_overlap=chunk_overlap
        
        self.llm_service = LLMService()
        self.vectorstore = Chroma(persist_directory="./db",embedding_function=self.embeddings)
        
    #Load PDF    
    def load_pdf_document(self, pdf_file: str) -> list[Document]:
        loader = PyPDFLoader(pdf_file)
        return loader.load() 
    
    #Split Document
    def split_document(self, documents: list[Document]) -> list[Document]:
        #splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size,chunk_overlap=self.chunk_overlap)
        splitter = RecursiveCharacterTextSplitter(chunk_size=self.search_config["chunk_size"],chunk_overlap=self.search_config["chunk_overlap"])
        return splitter.split_documents(documents) 
    
    #Create Vector Store
    def save_chunks_to_vector_store(self, chunks: list[Document], original_file_name:str):
        try:
            for chunk in chunks:
                chunk.metadata["filename"] = original_file_name
                logger.info(f"Chunks after Updating the filename: {chunks}")         
                self.vectorstore.add_documents(chunks)
        except Exception as ex:
            if "RESOURCE_EXHAUSTED" in str(ex):
                logger.info("Embedding quota exceeded.")
                logger.info(f"The whole exception in save chunks is: {str(ex)}")
                match = re.search(r"Please retry in ([\d.]+)s",str(ex))
                logger.info(f"(match returns: {match})")
                if match:
                    seconds = int(match.group(1))
                    raise EmbeddingQuotaExceededError (retry_after=seconds)
                raise EmbeddingQuotaExceededError (retry_after=None)          
        
                
    def store_pdf_document_in_db(self, pdf_file:str, original_file_name:str)-> dict:
        #filename=Path(pdf_file).name
        logger.info(f"file name in store pdf document is: {original_file_name}")
        if(self.pdf_document_already_exists(original_file_name)):
            raise RuntimeError("The document is already persisted!")
        else:
            logger.info(f"uploaded_file name {original_file_name} doesn't exist")
        
        documents: list[Document]   = self.load_pdf_document(pdf_file=pdf_file)
        chunks: list[Document] = self.split_document(documents=documents)
        self.save_chunks_to_vector_store(chunks=chunks,original_file_name=original_file_name)
        statistics: dict = {
            "pages": len(documents),
            "chunks": len(chunks)
        }
        return statistics
        
    def pdf_document_already_exists(self,pdf_file:str):
        
         result = self.vectorstore.get()
         logger.info(f"Total documents in Chroma: {len(result['ids'])}")
         logger.info(f"First metadata: {result['metadatas'][0] if result['metadatas'] else None}")
         result = self.vectorstore.get(where={"filename": pdf_file})
        
         logger.info(f"Found matching documents. Result of vectorstore.get with odf file name: {result}")
         return len(result["ids"]) > 0
    
    # To test  search_type="mmr",       
    def retrieve_similar_documents_threshold(self,search_str: str, number_of_documents=4) -> list[Document]:
        for threshold in [
            0.3,
            0.4,
            0.5,
            0.6,
            0.7
            ]:
            retriever = self.vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": number_of_documents,
                           "score_threshold": threshold})
            results = retriever.invoke(search_str)
            logger.info(f"Retriever with threshold of {threshold} is: {results}")
        
    
    # To test  search_type="mmr",  
    # search_type="similarity_score_threshold",
    #         search_kwargs={"k": number_of_documents,
    #                        "score_threshold": 0.6})     
    def retrieve_similar_documents(self,search_str: str, number_of_documents=4) -> list[Document]:
        
        logger.info(f"Search config is: {self.search_config}")
        
        search_type = self.search_config["search_type"]
        if search_type == "similarity":
            search_kwargs = {
                "k": self.search_config["number_of_chunks"]}

        elif search_type == "similarity_score_threshold":
            search_kwargs = {
                "k": self.search_config["number_of_chunks"],
                "score_threshold": self.search_config["threshold"]}

        elif search_type == "mmr":
           search_kwargs = {
               "k": self.search_config["number_of_chunks"],
               "fetch_k": 10 }

        retriever = self.vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs)
        
        results = retriever.invoke(search_str)
        return results 
          
     
    def build_prompt(self, documents: list[str], question: str) ->str:
        context="\n\n".join(
           doc.page_content for doc in documents)
        logger.info(f"Search Configuration in build prompt: {self.search_config}")
        if self.search_config["allow_general_knowledge"]:
            hint_for_llm = """
                Answer the question using the provided context.

                If the context is insufficient, use your general knowledge,
                but explicitly state that the answer was not found in the
                uploaded documents in the database. 
            """
        else:
            hint_for_llm= """
                Answer the question using only the provided context.

                If the answer is not contained in the context, say:
                "I don't have enough information in the provided documents in the data base. You can use however the knowledgebase to get better response."
                
            """
        
        prompt = f"""
                 {hint_for_llm}
                 
                 Context:
                 {context}

                 Question:
                {question}

                Answer:
    
        """
        logger.info(f"Prompt is: {prompt}")
        return prompt
        
    def ask_question(self, question: str, search_config: dict):
        self.search_config=search_config
        documents=self.retrieve_similar_documents(question)
        logger.info(f"Retriever similar documents Results: {documents}")
        prompt=self.build_prompt(documents=documents,question=question)
        response=self.llm_service.invoke(prompt=prompt)
        return response
          
    
    
           
            
    #Load Existing Vector Store
    #This is useful when the application starts: 
    def load_vector_store(self):
        self.vectorstore = Chroma(
        persist_directory="./db",
        embedding_function=self.embeddings)  
      
    
      