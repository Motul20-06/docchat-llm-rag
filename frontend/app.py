# frontend/app.py

import streamlit as st
import requests

API = "http://localhost:8000"

st.set_page_config(page_title="DocChat AI", layout="wide")

# Sidebar navigation
page = st.sidebar.selectbox("Navigate", ["User Chat", "Admin Panel"])

# =========================
# USER CHAT PAGE
# =========================
if page == "User Chat":
    st.title("🤖 DocChat AI")

    if "history" not in st.session_state:
        st.session_state.history = []

    question = st.text_input("Ask something from document")

    if st.button("Send"):
        res = requests.get(f"{API}/ask", params={"q": question})
        answer = res.json()["answer"]

        st.session_state.history.append(("You", question))
        st.session_state.history.append(("Bot", answer))

    # Chat display
    for role, msg in st.session_state.history:
        if role == "You":
            st.markdown(f"**🧑 You:** {msg}")
        else:
            st.markdown(f"**🤖 Bot:** {msg}")

# =========================
# ADMIN PANEL
# =========================
elif page == "Admin Panel":
    st.title("🛠️ Admin Panel")

    uploaded_file = st.file_uploader("Upload PDF")

    if uploaded_file:
        files = {"file": uploaded_file.getvalue()}
        res = requests.post(f"{API}/upload", files=files)
        st.success(res.json())

    st.subheader("📂 Uploaded Documents")

    docs = requests.get(f"{API}/docs").json()
    st.write(docs["documents"])

    st.subheader("🧪 Test Query")

    test_q = st.text_input("Test question")

    if st.button("Test"):
        res = requests.get(f"{API}/ask", params={"q": test_q})
        st.write(res.json()["answer"])