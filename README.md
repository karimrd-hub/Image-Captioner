# 🖼️ Designer AI eye Image Captioning App

## 🧠 Choosing the Model for Captioning Images

1. 📝 We started by defining the type of model needed to perform the task: we required models with an **image encoder** to accept an image as input.
2. 📊 We explored **benchmarks** for multimodal models and vision-language models to understand which ones perform best for such tasks.
3. 🧪 We used a **model playground** to test the performance of different models. After inspecting the results, I preferred **gemini-2.5-flash** and **llama-4-maverick** for their ability to analyze images and understand fine details.
4. 🚫 I could not use *maverick* due to some integration errors with AWS Bedrock.
5. ✅ Finally, I chose **claude-3.5-sonnet-v1** with **prompt engineering** to produce a robust, professional analysis resembling that of a fashion designer.

---

In task1/ you will find :  

gucci_under_1000 : 20 designs from gucci with price under 1000 euro
men_clothing : 500 images of men clothing
women_clothing : 500 images of men clothing
women_clothing_subset : a subset of 20 images of women clothing on which i tested the caption generation and saved the output to "example_of_20_captions.csv"
women_gucci_under_1000
women_saint_laurent : 50 designs bn=y saint laurent
women_shoes : 100 shoes designs
claude_3.5_sonnet.ipynb : the code that I used to invoke claude-3.5-sonnet-v1 on bedrock
example_of_20_captions.csv
mytheresa_scraper.ipynb : the codes I used to scrape mytheresa

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

1. **Create an S3 Bucket**

   * Go to the AWS console → search for **S3** → create an S3 bucket.
   * Paste the name of the created bucket in `frontend/streamlit_app.py` → `bucket_name`.

2. **Setup the Virtual Environment and Install Dependencies**

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment (PowerShell)
./.venv/Scripts/Activate.ps1

# Install required packages
pip install -r requirements.txt
```

3. **Configure AWS Credentials**

   * Fill your AWS credentials in a `.env` file.

4. **Run the App**

```bash
streamlit run frontend/streamlit_app.py
```
