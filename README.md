# 🖼️ Designer AI eye Image Captioning App

## 🧠 Choosing the Model for Captioning Images

1. 📝 We started by defining the type of model needed to perform the task: we required models with an **image encoder** to accept an image as input.
2. 📊 We explored **benchmarks** for multimodal models and vision-language models to understand which ones perform best for such tasks.
3. 🧪 We used a **model playground** to test the performance of different models. After inspecting the results, I preferred **gemini-2.5-flash** and **llama-4-maverick** for their ability to analyze images and understand fine details.
4. 🚫 I could not use *maverick* due to some integration errors with AWS Bedrock.
5. ✅ Finally, I chose **claude-3.5-sonnet-v1** with **prompt engineering** to produce a robust, professional analysis resembling that of a fashion designer.

---

## ⚙️ Implementing the App

The app is built using **Streamlit** for the frontend and **Flask** for the backend.

### 🎨 Frontend (Streamlit)

* 💻 Implemented the frontend using **Streamlit**.
* ⚡ At the start of the Streamlit script, I added a snippet to **automatically trigger** the Flask backend to run.
* 📤 The user uploads an image through the interface.
* 🔍 The frontend ensures that the uploaded image has a **compatible format**.
* ☁️ Once validated, the image is **automatically uploaded** to an S3 bucket.
* 🔑 The image is encoded into **Base64 format** to meet AWS Bedrock API requirements.
* 🔄 The frontend then calls the `/api/caption` route from the backend, which invokes `generate_caption()`. This in turn calls `caption_image()` from `utils/image_captioner.py`, which uses Bedrock's **claude-3.5-sonnet-v1** model to generate a caption and return it to the user.

---

## 🚀 How to Use the App

```bash
cd week1
streamlit run frontend/streamlit_app.py
```

