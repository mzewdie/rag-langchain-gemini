import streamlit as st

if "counter" not in st.session_state:
    st.session_state["counter"]=0
    
st.title="Session State Demo"   
if st.button("Increment"):
    st.session_state["counter"]+=1
    
if st.button("Reset"):
    st.session_state["counter"]=0
    
st.write(f"Counter: {st.session_state["counter"]}")   
    