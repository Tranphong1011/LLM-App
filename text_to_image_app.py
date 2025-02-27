import streamlit as st
from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO
from io import BytesIO

from config import openai_api_key

def run_text_to_image_app():
    col1, col2 = st.columns(2)

    with col1:
        model_option = st.selectbox(
            "Select DALL-E model", 
            ["dall-e-3", "dall-e-2"]
        )
        
        style_option = st.selectbox(
            "Select style (DALL-E 3 only)",
            ["vivid", "natural"],
            disabled=model_option != "dall-e-3"
        )

    with col2:
        size_options = {
            "dall-e-3": ["256x256", "512x512", "1024x1024", "1024x1792", "1792x1024"],
            "dall-e-2": ["256x256", "512x512", "1024x1024"]
        }
        
        size_option = st.selectbox(
            "Select image size",
            size_options[model_option]
        )

    st.divider()

    prompt = st.text_area("Enter your image description", height=100)

    def generate_image(client, prompt, model, size, style=None):
        try:
            kwargs = {
                "model": model,
                "prompt": prompt,
                "size": size,
                "n": 1,
            }
            
            if model == "dall-e-3" and style:
                kwargs["style"] = style
                
            response = client.images.generate(**kwargs)
            image_url = response.data[0].url
            
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            return img
        
        except Exception as e:
            st.error(f"Error generating image: {str(e)}")
            return None

    if st.button("Generate Image"):
        if not prompt:
            st.warning("Please enter a description for your image")
        else:
            try:
                client = OpenAI(api_key=openai_api_key)
                
                with st.spinner("Generating your image..."):
                    image = generate_image(
                        client=client,
                        prompt=prompt,
                        model=model_option,
                        size=size_option,
                        style=style_option if model_option == "dall-e-3" else None
                    )
                    
                    if image:
                        st.image(image, caption="Generated Image", use_column_width=True)
                        
                        buf = BytesIO()
                        image.save(buf, format="PNG")
                        byte_im = buf.getvalue()
                        st.download_button(
                            label="Download Image",
                            data=byte_im,
                            file_name="generated_image.png",
                            mime="image/png"
                        )
            except Exception as e:
                st.error(f"Error: {str(e)}")
            st.warning("Please enter a description for your image")