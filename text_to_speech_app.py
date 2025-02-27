import streamlit as st
from openai import OpenAI
import os
from tempfile import NamedTemporaryFile

from config import openai_api_key

def run_text_to_speech_app():

    
    text_input = st.text_area(
        "Enter text to convert to speech",
        height=150,
        placeholder="Type the text you want to convert to speech..."
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        voice = st.selectbox(
            "Select voice",
            ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        )
    
    with col2:
        model = st.selectbox(
            "Select model",
            ["tts-1", "tts-1-hd"]
        )
    
    if st.button("Generate Speech"):
        if not text_input:
            st.warning("Please enter some text to convert to speech")
        else:
            try:
                client = OpenAI(api_key=openai_api_key)
                
                with st.spinner("Generating audio..."):
                    response = client.audio.speech.create(
                        model=model,
                        voice=voice,
                        input=text_input
                    )
                    

                    with NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                        temp_path = temp_file.name
                        response.stream_to_file(temp_path)
                    
 
                    with open(temp_path, "rb") as audio_file:
                        audio_bytes = audio_file.read()
                    

                    os.unlink(temp_path)
  
                    st.audio(audio_bytes, format="audio/mp3")

                    st.download_button(
                        label="Download audio",
                        data=audio_bytes,
                        file_name="generated_speech.mp3",
                        mime="audio/mp3"
                    )

                    st.info(f"Audio generated with {model} model using {voice} voice")
            
            except Exception as e:
                st.error(f"Error generating speech: {str(e)}")
    
    st.divider()
    
    with st.expander("Voice Samples"):
        st.markdown("""
        **Voice Descriptions:**
        - **Alloy**: Versatile, balanced voice
        - **Echo**: Deep, calm male voice
        - **Fable**: Story-telling style, appropriate for narration
        - **Onyx**: Authoritative, commanding male voice
        - **Nova**: Feminine voice with a soft and friendly tone
        - **Shimmer**: Bright, youthful female voice
        """)
        
    with st.expander("Model Information"):
        st.markdown("""
        **TTS-1**: Standard model, good for most use cases
        
        **TTS-1-HD**: Higher quality with more natural sound, but slightly slower and more expensive
        """)