import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
import logging

def main():
    
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s",
                        filename="logs/rag-logs.log")

    logger = logging.getLogger(__name__)
    
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
    
    for doc in documents:
        logger.info("-" * 40)
        logger.info(f"Page: {doc.metadata['page']}")
        logger.info(doc.page_content[:200])


if __name__ == "__main__":
    main()