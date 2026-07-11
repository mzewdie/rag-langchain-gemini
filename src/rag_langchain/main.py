import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


def main():
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


if __name__ == "__main__":
    main()