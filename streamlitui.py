import os
import tempfile
import streamlit as st
from streamlit_chat import message
from webquery import WebQuery

st.set_page_config(page_title="ChatPDF")

# Obtener la clave de API de OpenAI desde una variable de entorno
openai_api_key = os.getenv("OPENAI_API_KEY")

def display_messages():
    st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()


def process_input():
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
            query_text = st.session_state["webquery"].ask(user_text)

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((query_text, False))


def main():
    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        st.session_state["url"] = ""
        if is_openai_api_key_set():
            st.session_state["webquery"] = WebQuery(openai_api_key)
        else:
            st.session_state["webquery"] = None

    st.header("Website to Chatbot")

    if st.text_input("OpenAI API Key", value=openai_api_key, key="input_OPENAI_API_KEY", type="password"):
        if (
            len(st.session_state["input_OPENAI_API_KEY"]) > 0
            and st.session_state["input_OPENAI_API_KEY"] != openai_api_key
        ):
            openai_api_key = st.session_state["input_OPENAI_API_KEY"]
            st.session_state["messages"] = []
            st.session_state["user_input"] = ""
            st.session_state["webquery"] = WebQuery(openai_api_key)

    st.subheader("Add a url")
    if st.text_input("Input url", value=st.session_state["url"], key="input_url", type="default"):
        if (
            len(st.session_state["input_url"]) > 0
            and st.session_state["input_url"] != st.session_state["url"]
        ):
            st.session_state["url"] = st.session_state["input_url"]

    st.session_state["ingestion_spinner"] = st.empty()

    display_messages()
    st.text_input("Message", key="user_input", disabled=not is_openai_api_key_set(), on_change=process_input)

    st.divider()
    st.markdown("Source code: [Github](https://github.com/Anil-matcha/Website-to-Chatbot)")


if __name__ == "__main__":
    main()
