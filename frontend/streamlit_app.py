# frontend/streamlit_app.py

import streamlit as st
import requests
from PIL import Image
import io
import base64
from typing import Optional, Dict, Any

import subprocess
import socket
import os
import sys
import time
import uuid

import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError

def is_port_in_use(port):
    """Check if a port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0

def start_backend():
    """Start Flask backend if not already running."""
    backend_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "backend", "app.py")
    )

    if not os.path.exists(backend_path):
        raise FileNotFoundError(f"Backend file not found: {backend_path}")

    if not is_port_in_use(5000):
        print(f"Starting backend server from {backend_path}...")
        subprocess.Popen(
            [sys.executable, backend_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(2)
    else:
        print("Backend already running.")

start_backend()

def upload_image_to_s3(image: Image.Image, filename: str, bucket_name: str) -> bool:
    """Upload a PIL image to S3."""
    try:
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)

        s3 = boto3.client("s3")
        s3.upload_fileobj(buffer, bucket_name, filename, ExtraArgs={"ContentType": "image/jpeg"})

        return True
    except (BotoCoreError, NoCredentialsError, Exception) as e:
        st.error(f"Failed to upload image to S3: {str(e)}")
        return False

class PhotoCaptionApp:
    def __init__(self):
        self.api_base_url = self._get_api_base_url()
        self.available_models = {
            "claude-3.5-sonnet-v1": "Claude 3.5 Sonnet"
        }

    def _get_api_base_url(self) -> str:
        import os
        return (
            st.secrets.get("API_BASE_URL") or 
            os.getenv("API_BASE_URL") or 
            "http://localhost:5000/api"
        )

    def _encode_image_to_base64(self, image: Image.Image) -> str:
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        img_bytes = buffer.getvalue()
        return base64.b64encode(img_bytes).decode()

    def _call_caption_api(self, image_b64: str, model: str) -> Dict[str, Any]:
        try:
            payload = {
                "image": image_b64,
                "model": model
            }

            response = requests.post(
                f"{self.api_base_url}/caption",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"API request failed: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}

    def _validate_image(self, uploaded_file) -> Optional[Image.Image]:
        if uploaded_file is None:
            return None

        try:
            if uploaded_file.size > 10 * 1024 * 1024:
                st.error("Image file is too large. Please upload an image smaller than 10MB.")
                return None

            image = Image.open(uploaded_file)
            if image.mode != 'RGB':
                image = image.convert('RGB')

            return image

        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
            return None

    def render_header(self):
        st.title("🖼️ AI Photo Captioning")
        st.markdown("""
        Upload an image and let AI generate a descriptive caption for you.
        Choose your preferred AI model and get instant results!
        """)

    def render_model_selector(self) -> str:
        st.subheader("⚙️ Model Selection")
        selected_model = st.selectbox(
            "Choose AI Model:",
            options=list(self.available_models.keys()),
            format_func=lambda x: self.available_models[x],
            key="model_selector"
        )
        return selected_model

    def render_image_uploader(self) -> Optional[Image.Image]:
        st.subheader("📤 Upload Image")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
            key="image_uploader",
            help="Supported formats: PNG, JPG, JPEG, GIF, BMP (Max size: 10MB)"
        )

        if uploaded_file is not None:
            image = self._validate_image(uploaded_file)
            if image:
                # Upload to S3
                filename = f"user_uploads/{uuid.uuid4().hex}.jpg"
                bucket_name = "karim-s3-bucket-internship-week1-image-captioner"

                if upload_image_to_s3(image, filename, bucket_name):
                    st.success(f"Image uploaded to S3 as `{filename}`")
                else:
                    st.warning("Image upload to S3 failed. Continuing...")

                st.image(image, caption="Uploaded Image", use_container_width=True)
                return image

        return None

    def render_caption_section(self, image: Image.Image, model: str):
        st.subheader("✨ Generated Caption")

        if st.button("Generate Caption", type="primary", use_container_width=True):
            with st.spinner(f"Generating caption using {self.available_models[model]}..."):
                image_b64 = self._encode_image_to_base64(image)
                result = self._call_caption_api(image_b64, model)
                st.session_state.caption_result = result

        if hasattr(st.session_state, 'caption_result'):
            result = st.session_state.caption_result

            if result.get("success", False):
                caption = result.get("caption", "")
                st.success("Caption generated successfully!")

                st.markdown("### 📝 Caption:")
                st.markdown(
                    f'<div style="padding: 15px; border-radius: 5px; border-left: 3px solid #4CAF50;"><p style="margin: 0; font-size: 16px;">{caption}</p></div>',
                    unsafe_allow_html=True
                )

                if "model_used" in result:
                    st.caption(f"Generated by: {result['model_used']}")
            else:
                error_msg = result.get("error", "Unknown error occurred")
                st.error(f"Failed to generate caption: {error_msg}")

                if st.button("🔄 Retry", key="retry_button"):
                    del st.session_state.caption_result
                    st.rerun()

    def render_sidebar(self):
        with st.sidebar:
            st.header("ℹ️ About")
            st.markdown("""
            This app uses advanced AI models to generate descriptive captions for your images.
            
            **How it works:**
            1. Upload an image
            2. Select an AI model
            3. Click "Generate Caption"
            4. Get your AI-generated caption!
            """)

            st.header("📊 Model Info")
            st.markdown("""
            **Claude 3.5 Sonnet:**
            - High-quality image understanding
            - Detailed and accurate captions
            - Fast processing time
            """)

    def run(self):
        st.set_page_config(
            page_title="AI Photo Captioning",
            page_icon="🖼️",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        self.render_header()
        self.render_sidebar()

        col1, col2 = st.columns([1, 1])

        with col1:
            selected_model = self.render_model_selector()
            uploaded_image = self.render_image_uploader()

        with col2:
            if uploaded_image is not None:
                self.render_caption_section(uploaded_image, selected_model)
            else:
                st.info("👈 Please upload an image to get started!")

        if hasattr(st.session_state, 'caption_result'):
            if st.button("🗑️ Clear Results", key="clear_results"):
                del st.session_state.caption_result
                st.rerun()


def main():
    app = PhotoCaptionApp()
    app.run()

if __name__ == "__main__":
    main()
