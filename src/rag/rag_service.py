import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
import logging
from src.rag_langchain_old.utils.logging_config import configure_logging
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# Load environment variables from .env
load_dotenv()

# Read the API key
api_key = os.getenv("GEMINI_API_KEY")
model = "gemini-2.5-flash"

#Embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

class RAGService:
    
    def __init__(self):
        self.embeddings=embeddings
    
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
        embedding = self.embeddings.aembed_documents(chunks)
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