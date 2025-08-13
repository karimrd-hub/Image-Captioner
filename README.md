- Choosing the model that will be used for captioning the images : 

1 - we started by defining the type of model we need to use to perform the task : we needed models that have an image encoder to be able to pass an image as input
2 - we explored benchmarks for multimodal models and vision-language models to obtain insights on what models perform better on sucht ype of tasks
3 - we used a model playground to test the performance of different models and by inspecting the results I preferred gemini-2.5-flash and llama-4-maverick in terms of analyzing the image and understanding the details
4 - I couldn't use maverick because of some integration errors with aws bedrock
5 - Finally, I used claude-3.5-sonnet-v1 with prompt engineering in order to get a robust, professional analysis that seems like the analysis of a fashion desginer


- Implementing the app : 
I used streamlit for the frontend and flask for the backend
1 - Fronted : 
    . I started by implementing the frontend using streamlit
    . In the start of the streamlit code I inserted a script that triggers the flask backend to run automatically
    . The user goes in and upload the image
    . The frontend makes sure that the uploaded image has a compatible format 
    . after the checks are complete, the app automatically uploads the image to an s3 bucket  
    . The app encodes the image into base64 format so it can be compatible with bedrock api requirements and then calls the "/api/caption" route from the backend that invokes the generate_caption() which calls caption_image() from utils/image_captioner.py method that invokes bedrock's claude-3.5-sonnet-v1 model to generate a caption and render it to the user



How to use the app : 
- cd week1
- streamlit run frontend/streamlit_app.py