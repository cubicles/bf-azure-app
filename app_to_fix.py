import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import json
import requests
import base64
import os
from dotenv import load_dotenv
import io

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
    # Remove this block of code:
    # with open('class_names.txt') as f:
    #     class_names = f.readlines()

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
    print(response.content)

    if response.status_code == 200:
        response_data = response.json()
        if 'prediction' in response_data:
            breed = response_data['prediction'].strip()  # Remove newline character
        else:
            breed = f"Error!: 'prediction' key not found in the response. Response: {response_data}"
    else:
        breed = f"Error!: {response.status_code}, {response.text}"

    return breed   

if __name__ == "__main__":
    main()

