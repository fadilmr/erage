# import os
# import tempfile
# import streamlit as st
# from streamlit_chat import message
# from rag import bappenasRAG

# st.set_page_config(page_title="BappenasRAGDemo")


# def display_messages():
#     st.subheader("Chat")
#     # user_avatar_path = "profile.png"
#     for i, (msg, is_user) in enumerate(st.session_state["messages"]):
#         message(msg, is_user=is_user, key=str(i))
#     st.session_state["thinking_spinner"] = st.empty()


# def process_input():
#     if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
#         user_text = st.session_state["user_input"].strip()
#         with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
#             agent_text = st.session_state["assistant"].ask(user_text)

#         st.session_state["messages"].append((user_text, True))
#         st.session_state["messages"].append((agent_text, False))


# def read_and_save_file():
#     st.session_state["assistant"].clear()
#     st.session_state["messages"] = []
#     st.session_state["user_input"] = ""

#     for file in st.session_state["file_uploader"]:
#         with tempfile.NamedTemporaryFile(delete=False) as tf:
#             tf.write(file.getbuffer())
#             file_path = tf.name

#         with st.session_state["ingestion_spinner"], st.spinner(f"Ingesting {file.name}"):
#             st.session_state["assistant"].ingest(file_path)
#         os.remove(file_path)


# def page():
#     if len(st.session_state) == 0:
#         st.session_state["messages"] = []
#         st.session_state["assistant"] = bappenasRAG()

#     st.header("BappenasRAGDemo")

#     st.subheader("Upload a document")
#     st.file_uploader(
#         "Upload document",
#         type=["pdf"],
#         key="file_uploader",
#         on_change=read_and_save_file,
#         label_visibility="collapsed",
#         accept_multiple_files=True,
#     )

#     st.session_state["ingestion_spinner"] = st.empty()

#     display_messages()
#     st.text_input("Message", key="user_input", on_change=process_input)


# if __name__ == "__main__":
#     page()

import os
import tempfile
import streamlit as st
from streamlit_chat import message
from rag import bappenasRAG

st.set_page_config(page_title="BappenasRAGDemo", layout="centered")


def display_messages():
    # Display chat messages in a clean, simple format
    # for i, (msg, is_user) in enumerate(st.session_state["messages"]):
    #     message(msg, is_user=is_user, key=str(i), avatar_style="circle")
    for message, is_user in st.session_state["messages"]:
        if is_user:
            user = st.chat_message('User')
            user.write(message)
        else:
            assistant = st.chat_message('Assistant')
            assistant.write(message)
    st.session_state["thinking_spinner"] = st.empty()


def process_input():
    # Handle user input and generate assistant response
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        
        with st.session_state["thinking_spinner"]:
            agent_text = st.session_state["assistant"].ask(user_text)

        # Append user and assistant messages to session state
        st.session_state["messages"].append((user_text, True))  # User message
        st.session_state["messages"].append((agent_text, False))  # Assistant message

        # Clear input box after sending the message
        st.session_state["user_input"] = ""


def read_and_save_file():
    # Clear previous data and reset the assistant
    st.session_state["assistant"].clear()
    st.session_state["messages"] = []

    # Handle file ingestion
    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        # Ingest the file
        st.session_state["assistant"].ingest(file_path)
        os.remove(file_path)


def page():
    # Initialize session state if empty
    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        st.session_state["assistant"] = bappenasRAG()

    # File Upload Section
    st.file_uploader(
        "Upload PDF Document", 
        type=["pdf"], 
        key="file_uploader", 
        on_change=read_and_save_file, 
        accept_multiple_files=True
    )

    # Display chat history
    display_messages()

    # User input section with streamlined UI
    st.text_input(
        "Type your message here...",
        key="user_input",
        on_change=process_input,
        placeholder="Ask something..."
    )


if __name__ == "__main__":
    page()