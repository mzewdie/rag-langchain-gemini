import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
import logging
from src.rag_langchain.utils.logging_config import configure_logging
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma


def main():
    
    
    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info("Test")
    logger.debug("This is a DEBUG message.")
    logger.info("This is an INFO message.")
    
    """
    
Logging in den anderen Modulen: In anderen Modulen

Nehmen wir an, wir erstellen später pdf_loader.py.

Dort genügt:

import logging

logger = logging.getLogger(__name__)

Mehr nicht.

Du musst nicht in jeder Datei configure_logging() aufrufen.

Das passiert genau einmal, wenn die Anwendung startet.

    
    """
    
    # Load environment variables from .env
    load_dotenv()

    # Read the API key
    api_key = os.getenv("GEMINI_API_KEY")

    # Create the chat model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
    )

    # Send a prompt
    response = llm.invoke("Explain what a Large Language Model is in one sentence.")

    # Print the response
    print(response.content)
    print(type(response))
    #prints <class 'langchain_core.messages.ai.AIMessage'>
    print(response)
    
    #loader = PyPDFLoader("data/PythonProgramming.pdf")
    #pdf_file="data/PythonLibReference.pdf"
    pdf_file="data/introduction-to-nutrition.pdf"
    loader = PyPDFLoader(pdf_file)

    logger.info(f"loading PDF {pdf_file}")
    documents = loader.load()
    print(f"Number of documents {len(documents)}")
    
    #inspect the first one
    """ doc = documents[0]
    print(type(doc))
    print(doc)
    print(doc.page_content)
    print(doc.metadata) """
    
    
    
    """ for doc in documents:
        logger.info("-" * 40)
        logger.info(f"Page: {doc.metadata['page']}")
        logger.info(doc.page_content[:400]) """
        
    
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                              chunk_overlap=200)
    chunks = splitter.split_documents(documents=documents)
    logger.info("Original documents: %d", len(documents))
    """ logger.info("Chunks created: %d", len(chunks))
    for chunk in chunks[:10]:
        logger.info("-" * 40)
        logger.info("Page chunk metada: %s", chunk.metadata["page"])
        logger.info("Source chunk metada: %s", chunk.metadata["source"])
        logger.info(f"Chunk Page Content: {chunk.page_content}")
         """
     #Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    #just experiment
    embedding = embeddings.embed_query("The cat is sleeping on the sofa.")
    logger.info("Embedding dimensions: %d", len(embedding))
    logger.debug("First 10 values: %s", embedding[:10])
    
    #adding to the vector store db
    vector_store = Chroma.from_documents(documents=chunks, embedding=embeddings)
    logger.info("vector Store created")
    
    #Verifying the store
    results=vector_store.similarity_search("Where is the kitten sleeping?",k=3)
    for doc in results:
        logger.info("-" * 40)
        logger.info("Page from vector store: %s", doc.metadata["page"])
        logger.info(doc.page_content[:200])
        
    #Retriuever
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    quesRetr="What are carbohydrates?"
    results = retriever.invoke(quesRetr) 
    logger.info(f"logging the restults of retriever for the question: {quesRetr}")
    for doc in results:
        logger.info("-" * 40)
        logger.info("Page: %s", doc.metadata["page"])
        logger.info(doc.page_content[:200])   
       
    
    
if __name__ == "__main__":
    main()