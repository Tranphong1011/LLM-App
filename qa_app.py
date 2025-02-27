import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from huggingface_hub import InferenceClient
from huggingface_hub.utils import HfHubHTTPError
from config import openai_api_key, huggingface_api_key

def run_qa_app():

# -------------------- OpenAI Chatbot --------------------

    st.header("Chatbot with OpenAI (GPT-3.5 Turbo)")

    def get_openai_response(question):
        """Generate response from OpenAI GPT-3.5-Turbo."""
        chat_model = ChatOpenAI(api_key=openai_api_key, model_name="gpt-3.5-turbo", temperature=0.0)
        messages = [
            SystemMessage(content="You are a friendly AI assistant."),
            HumanMessage(content=question)
        ]
        response = chat_model(messages)
        return response.content

    # User input for OpenAI model
    openai_user_input = st.text_input("You:", key="openai_input")
    if st.button("Generate",key="openai_button"):
        if openai_user_input:
            openai_response = get_openai_response(openai_user_input)
            st.subheader("OpenAI Answer:")
            st.write(openai_response)

    # -------------------- Hugging Face Chatbot --------------------

    st.header("Chatbot with Hugging Face")

    # Available Hugging Face models
    models = {
        "Zephyr-7B": {
            "provider": "hf-inference",
            "model_name": "HuggingFaceH4/zephyr-7b-beta",
            "max_tokens": 500,
        },
        "DeepSeek-R1": {
            "provider": "together",
            "model_name": "deepseek-ai/DeepSeek-R1",
            "max_tokens": 200,
        },
        "AlphaMaze-1.5B": {
            "provider": "hf-inference",
            "model_name": "homebrewltd/AlphaMaze-v0.2-1.5B",
            "max_tokens": 500,
        },
        "Phi-4": {
            "provider": "nebius",
            "model_name": "microsoft/phi-4",
            "max_tokens": 500,
        }
    }

    # Model selection
    selected_model = st.selectbox("Choose a Hugging Face model:", list(models.keys()))

    # User input for Hugging Face model
    hf_user_input = st.text_input("You:", key="hf_input")

    if st.button("Generate", key="hf_button"):
        if hf_user_input:
            try:
                # Get model information
                model_info = models[selected_model]
                provider = model_info["provider"]
                model_name = model_info["model_name"]
                max_tokens = model_info["max_tokens"]

                # Initialize Hugging Face inference client
                client = InferenceClient(provider=provider, api_key=huggingface_api_key)

                # Send request to the selected model
                messages = [{"role": "user", "content": hf_user_input}]
                completion = client.chat.completions.create(
                    model=model_name, messages=messages, max_tokens=max_tokens
                )

                # Display response
                hf_result = completion.choices[0].message
                st.subheader(f"Hugging Face ({selected_model}) Answer:")
                st.write(hf_result)

            except HfHubHTTPError as e:
                # Handle errors when the model exceeds quota
                if "You have exceeded your monthly included credits for Inference Providers" in str(e):
                    st.error("⚠️ This model has exceeded the usage limit. Please choose another model.")
                else:
                    st.error(f"❌ Error: {str(e)}")



