import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
import logging
from common.utils.logging_config import configure_logging
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# Load environment variables from .env
load_dotenv()

configure_logging()
logger = logging.getLogger(__name__)

# Read the API key
api_key = os.getenv("GEMINI_API_KEY")
model = "gemini-2.5-flash"

#Embeddings
#embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

#Embeddings
#  embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    #just experiment
#    embedding = embeddings.embed_query("The cat is sleeping on the sofa.")

class RAGService:
    
    def __init__(self):
        self.embeddings=GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    def load_pdf_document(self, pdf_file_path):
        loader = PyPDFLoader(pdf_file_path)
        documents = loader.load()
        return documents
    
    def split_document(self, documents):
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                  chunk_overlap=200)
        chunks = splitter.split_documents(documents=documents)
        return chunks
    
    def embed_chunks(self,chunks):
        embedding = self.embeddings.embed_documents(chunks[0].page_content)
        return embedding
        
    def store_in_vector_db(self, chunks, embedding):
        vector_store = Chroma.from_documents(documents=chunks, embedding=embedding)
        return vector_store
    
    def similarity_search(self,vector_store,search_str):
        results=vector_store.similarity_search(search_str,k=3) 
        return results  
    
    def retrieve_from_vector_db(self,vector_store,retriever_query_str):
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        results = retriever.invoke(retriever_query_str)
        return results 
    
    def add_pdf_document_to_vector_db(self,pdf_file):
        documents=self.load_pdf_document(pdf_file_path=pdf_file)
        #logger.info(f"doucment loaded: {documents}")
        chunks=self.split_document(documents=documents)
        #logger.info(f"chunked documents: {chunks}")
        embedding=self.embed_chunks(chunks=chunks)
        logger.info(f"embedding results: {embedding}")
        vector_store=self.store_in_vector_db(chunks=chunks,embedding=embedding)
        return vector_store