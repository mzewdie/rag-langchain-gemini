import streamlit as st 
from src.rag.rag_service_v2 import RAGService

st.title("Searching LLM with the help of RAG System")
st.info(
    """
    Recommended settings:

    - Search Type: similarity
    - Number of Chunks: 3-4
    - Score Threshold: 0.6 (Gemini)
    - Chunk Size: 1000
    - Chunk Overlap: 200
    """
)

search_type = st.selectbox(
    "Search Type",
    ["similarity_score_threshold","similarity", "mmr" ],
    help="""
similarity:
Returns the most similar chunks.

mmr:
Returns relevant chunks while avoiding duplicates.

similarity_score_threshold:
Returns only chunks above a similarity threshold.
"""
)

threshold = st.slider(
    "Score Threshold",
    0.0,
    1.0,
    0.6,
    help="""
Minimum similarity score required for a chunk to be returned.

Lower values:
- More results
- More noise

Higher values:
- Fewer results
- More precise results

Typical values for Gemini embeddings:
0.5 - 0.6
"""
)

k = st.slider(
    "Number of Chunks",
    1,
    10,
    4,
    help="""
Maximum number of chunks retrieved from the vector database.

Small values:
- Faster
- Less context

Large values:
- More context
- More token usage
"""
)

chunk_size = st.slider(
    "Chunk Size",
    100,
    8000,
    5000,
    help="""
Size of each text chunk.

Small chunks:
- More precise retrieval

Large chunks:
- More context per chunk
"""
)

chunk_overlap = st.slider(
    "Chunk Overlap",
    100,
    500,
    200,
    help="""
Size of each the chunk overlap.
The overlapped chunk appears in both neighboured chunks

"""
)

allow_general_knowledge=st.toggle(
    "Allow General Knowledge",
    value=False
)

search_config={}
search_config["search_type"]=search_type 
search_config["threshold"]=threshold
search_config["number_of_chunks"]=k
search_config["chunk_size"]=chunk_size
search_config["chunk_overlap"]=chunk_overlap
search_config["allow_general_knowledge"]=allow_general_knowledge
st.session_state["search_config"]=search_config

st.write(f"Selected Search Configuration: {search_config}")

if "rag_service" not in st.session_state:
    st.session_state["rag_service"]=RAGService(search_config=search_config)
rag_service:RAGService = st.session_state["rag_service"] 



question=st.text_input("Your Question")
if st.button("Submit Question"):
    if not question:
        st.error("Please enter your Question")
    else:
        #results=rag_service.retrieve_similar_documents(search_str=question,number_of_documents=4)
        #st.write(f"Type of Response is: {type(results)}")
        #Type of Response is: <class 'list'>
        #st.write(f"Search Results in RAG DB: {results}")
        # for result in results:
        #     st.write(20*"-")
        #     st.write(result.page_content)
        with st.spinner("Searching in RAG Database and LLM ..."):
            response=rag_service.ask_question(question=question,search_config=st.session_state["search_config"])
            st.write(response.content)
       