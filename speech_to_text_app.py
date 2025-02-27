import streamlit as st
from openai import OpenAI
import tempfile


from config import openai_api_key

def run_speech_to_text_app():
    
    
    uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        model = st.selectbox(
            "Select model",
            ["whisper-1"]
        )
    
    with col2:
        language = st.selectbox(
            "Language (optional)",
            [None, "en", "es", "fr", "de", "it", "pt", "nl", "ja", "zh", "ru", "ar"],
            format_func=lambda x: "Auto-detect" if x is None else x
        )
    
    options = st.expander("Advanced options")
    with options:
        prompt = st.text_area(
            "Prompt (optional)",
            placeholder="Optional text to guide the model's style, continuation, or help with context",
            help="Use this to provide context for better accuracy"
        )
        
        response_format = st.selectbox(
            "Response format",
            ["json", "text", "srt", "verbose_json", "vtt"],
            index=1
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.1,
            help="Controls randomness. Lower values are more focused and deterministic."
        )
    
    if st.button("Transcribe Audio"):
        if uploaded_file is not None:
            try:
                client = OpenAI(api_key=openai_api_key)
                
                with st.spinner("Transcribing audio..."):
                  
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        audio_path = tmp_file.name
                    
                    #
                    params = {
                        "model": model,
                        "file": open(audio_path, "rb"),
                        "response_format": response_format,
                        "temperature": temperature,
                    }
                    
                    
                    if language:
                        params["language"] = language
                    if prompt:
                        params["prompt"] = prompt
                    
                    # Call the API
                    transcript = client.audio.transcriptions.create(**params)
                    
                
                    # os.unlink(audio_path)
                    
                    
                    if response_format == "json" or response_format == "verbose_json":
                        st.json(transcript)
                        transcription_text = transcript.text
                    else:
                        transcription_text = transcript
                        st.text_area("Transcription", transcription_text, height=250)
                    
                    
                    st.download_button(
                        label="Download transcription",
                        data=transcription_text,
                        file_name=f"transcription.{response_format if response_format in ['srt', 'vtt'] else 'txt'}",
                        mime="text/plain"
                    )
            
            except Exception as e:
                st.error(f"Error transcribing audio: {str(e)}")
        else:
            st.warning("Please upload an audio file to transcribe")
    
    st.divider()
    
    with st.expander("Supported file formats"):
        st.markdown("""
        - MP3
        - MP4
        - MPEG
        - MPGA
        - M4A
        - WAV
        - WEBM
        
        Maximum file size: 25MB
        """)
    
    with st.expander("Response format options"):
        st.markdown("""
        - **text**: Plain text transcript
        - **json**: JSON with transcript text
        - **verbose_json**: JSON with additional details including timestamps
        - **srt**: SubRip subtitle format
        - **vtt**: WebVTT subtitle format
        """)