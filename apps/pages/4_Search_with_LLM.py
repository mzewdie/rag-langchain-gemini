import streamlit as st
from src.llm.llm_service import LLMService

    
st.write("Communication with AI")
st.write("Ask the AI")
question=st.text_input("Your Question Please:")
llm_service=LLMService()
if("llm_service") not in st.session_state:
    st.session_state["llm_service"]=llm_service


if st.button("Submit Question"):
    if question:
        with st.spinner("I search ..."):
            response=st.session_state.llm_service.ask(question=question)
            #st.write(response("content"))
            st.write(response.content)
    else:
        st.write("Please enter the question first")