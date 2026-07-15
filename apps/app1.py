import streamlit as st
import time

st.title("My First Streamlit App for RAG")
st.write("Welcome to My RAG Project")

name = st.text_input("Your name:")
if st.button("Say Hello"):
    st.write(f"Hello {name}")
    
if st.button("Greet"):
    if name:
        st.success(f"Hello {name}!")
    else:
        st.warning("Please enter your name.")    
        
uploaded_file = st.file_uploader("Upload a PDF")       

question = st.text_input("Ask a question")
print(question)

text = st.text_area("Prompt")
if st.button("Ask"):
    st.write(question)
    st.write(text)
    
uploaded_file = st.file_uploader(
    "Choose a PDF",
    type="pdf"
)
print(uploaded_file)
#st.write(uploaded_file.get("name"))

#spinner
with st.spinner("Creating embeddings..."):
    #build_vector_database()
    time.sleep(4)
    
 #This one is perfect for RAG.

with st.expander("Retrieved Chunks"):
    #st.write(chunk)
    time.sleep(1)   