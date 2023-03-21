import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import json
import requests
import base64

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

def predict(image):
    with open('class_names.txt') as f:
        class_names = f.readlines()

    # Lee la imagen
    img_data = image.read()

    # Encoding base64
    img_base64 = base64.b64encode(img_data).decode('utf-8')

    # Set the content type to 'application/octet-stream'
    api_key = ''  # ki
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    # Send the request with the image data
    scoring_uri = ''  # uri
    payload = json.dumps((img_base64, 'application/octet-stream'))
    response = requests.post(scoring_uri, data=payload, headers=headers)

    # Get the prediction result
    if response.status_code == 200:
        breed = response.json()['prediction']
    else:
        breed = f"Error!: {response.status_code}, {response.text}"

    return breed

if __name__ == "__main__":
    main()

