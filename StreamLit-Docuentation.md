Lesson 2 – The Essential Streamlit Widgets

We'll only learn the widgets that we will actually use in our RAG application.

1. st.write()

This is the Swiss Army knife of Streamlit.

st.write("Hello")
st.write(42)
st.write(my_dataframe)
st.write(my_dictionary)

It automatically formats the object.

Think of it as:

print(...)

for web applications.

2. st.text_input()

Exactly like Python's

input()

Example:

question = st.text_input("Ask a question")

If the user types

What are proteins?

then

question

contains

"What are proteins?"

Exactly what we need later.

3. st.text_area()

Sometimes one line isn't enough.

text = st.text_area("Prompt")

Useful for:

long prompts
document text
editing

We probably won't need it much.

4. st.button()
if st.button("Ask"):
    st.write(question)

Remember:

The button does not call a callback.

Instead:

Button clicked
        │
        ▼
Entire script reruns
        │
        ▼
button == True

Only during that execution.

5. st.file_uploader()

This is probably our most important widget.

uploaded_file = st.file_uploader(
    "Choose a PDF",
    type="pdf"
)

Initially:

uploaded_file == None

After selecting a file:

UploadedFile(...)

We can then process it.

For our RAG app, this will replace:

pdf_path = Path(...)

The user chooses the document interactively.

6. st.spinner()

Suppose embedding generation takes 10 seconds.

Instead of a frozen page:

with st.spinner("Creating embeddings..."):
    build_vector_database()

The user sees:

Creating embeddings...

This greatly improves the user experience.

7. st.success()
st.success("Database created successfully!")

Green message.

8. st.error()
st.error("Invalid PDF.")

Red message.

9. st.warning()
st.warning("Please upload a document first.")

Yellow message.

10. st.expander()

This one is perfect for RAG.

with st.expander("Retrieved Chunks"):
    st.write(chunk)

Initially:

▶ Retrieved Chunks

Click:

▼ Retrieved Chunks

Page 4

...

Page 7

...

It keeps the interface clean while still allowing us to inspect what the retriever found.

A small exercise

Create a new app.py:

import streamlit as st

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
        with st.spinner("Searching..."):
            st.write(f"You asked: {question}")
    else:
        st.warning("Please enter a question.")

with st.expander("Debug"):
    st.write("Question:", question)
    st.write("Uploaded file:", uploaded_file)
What should you observe?

There are three things I'd like you to notice:

The rerun behavior. Every interaction reruns the script, but the widgets retain their current values. Streamlit manages this for you.
The UploadedFile object. If you expand the "Debug" section after selecting a PDF, you'll see that uploaded_file isn't just a filename. It's an object containing metadata and the file's content. Later, we'll pass this object to our backend instead of hardcoding a path.
The separation of concerns. Right now, the button simply echoes the question. Later, the code inside the button will become something like:
with st.spinner("Searching..."):
    answer = rag_service.ask(question)
    st.write(answer)

Notice that the Streamlit code doesn't need to know how the RAG pipeline works. It only knows when to call it and how to display the result. That's exactly the architecture we've been aiming for since the beginning.

Our next lesson

The next topic is st.session_state.

In my opinion, that's the point where Streamlit stops feeling like a simple script and starts feeling like a framework for building stateful applications. It's also the key to making our RAG application efficient, because we'll avoid rebuilding the vector store every time the user asks a new question.