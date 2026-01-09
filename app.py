import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.title("🎓 Chatbot hỗ trợ sinh viên")

with open("static/index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=700, scrolling=True)
