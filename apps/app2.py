import streamlit as st
import time

st.title("Streamlit Widgets Demo")

question = st.text_input("Ask a question")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type="pdf"
)

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")

if st.button("Ask"):
    if question:
        time.sleep(5)
        with st.spinner("Searching..."):
            st.write(f"You asked: {question}")
    else:
        st.warning("Please enter a question.")

with st.expander("Debug"):
    st.write("Question:", question)
    st.write("Uploaded file:", uploaded_file)