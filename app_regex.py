import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import json
import requests
import base64
import os
from dotenv import load_dotenv
import io
import re

load_dotenv()

api_key = os.environ.get("API_KEY")
scoring_uri = os.environ.get("SCORING_URI")

fig = plt.figure()

st.header("Predict Dog Breed")
def main():
    file_uploaded = st.file_uploader("Choose File", type=["png","jpg","jpeg"])

    if file_uploaded is not None:
        image = Image.open(file_uploaded)
        plt.imshow(image)
        plt.axis("off")
        predictions = predict(file_uploaded)
        st.write(predictions)
        st.pyplot(fig)

def predict(file_uploaded):
    # Convert the file-like object to a PIL Image object
    image = Image.open(file_uploaded)

    # Convert the PIL Image object back to a file-like object
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='JPEG')
    img_data = img_bytes.getvalue()

    # Encode the image data as base64
    img_base64 = base64.b64encode(img_data)

    # Set the content type to 'application/json'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    # Send the request with the image data
    payload = json.dumps({"image": img_base64.decode('utf-8')})
    headers['Content-Type'] = 'application/json'
    response = requests.post(scoring_uri, data=payload, headers=headers)

    # Get the prediction result
    response_str = response.content.decode('utf-8')
    print(response_str)
    
    #match = re.search(r'\{"prediction"\s*:\s*"([^"]+)"\}', response_str)
    #match = re.search(r'\{"prediction"\s*:\s*"([^"]+?)\s*"\}', response_str)
    match = re.search(r'["\']?prediction["\']?\s*:\s*["\']?(\w+(\s+\w+)*)["\']?', response_str)

    if match:
        breed = match.group(1)
    else:
        breed = f"Error!: breed not found in response. Response: {response_str}"

    return breed.strip()

if __name__ == "__main__":
    main()

