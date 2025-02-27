import streamlit as st

# Sidebar with app selection
st.set_page_config(page_title="Main App", layout="wide")
st.sidebar.title("Applications")

app_selection = st.sidebar.radio("Select an app:", ["QA App", "Conversation App", "Text to Image App", "Text to Speech App", "test"])


if app_selection == "QA App":
    from qa_app import run_qa_app
    run_qa_app()
elif app_selection == "Conversation App":
    from conversation_app import run_conversation_app
    st.info("This is gpt-3.5-turbo model")
    run_conversation_app()
elif app_selection == "test":
    from test import test
    test()
elif app_selection == "Text to Image App":
    from text_to_image_app import run_text_to_image_app
    st.title("🖼️ Text-to-Image Generator with DALL·E")
    run_text_to_image_app()
elif app_selection == "Text to Speech App":
    from text_to_speech_app import run_text_to_speech_app
    st.title("🔊 Text-to-Speech Generator")
    run_text_to_speech_app()

