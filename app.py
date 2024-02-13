# Import necessary libraries
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Google Gemini Pro Vision API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(user_input, image, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([user_input, image[0], prompt])
    return response.text


# Function to set up image for processing
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


# Initialize Streamlit app
st.set_page_config(page_title="NutriGenie", page_icon="🍏")
st.title("NutriGenie")
st.write(
    "Your personal nutrition assistant. Analyze food items from images and calculate their total calories."
)


# Input prompt for user
user_input = st.text_input(
    "Please enter your question or instruction: ", key="user_input"
)

# File uploader for image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display uploaded image
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Submit button to process input
submit = st.button("Analyze Nutrition")

# Prompt for user input format
input_prompt = """
Imagine you are a nutritionist examining an image of food items to calculate their total calories and provide details for each item. Please list the food items detected in the image along with their respective calorie counts in the following format:

1. Food Item 1 - Calorie Count
2. Food Item 2 - Calorie Count
---
Example:
1. Apple - 52 calories
2. Salad - 120 calories
---

Ensure to be as descriptive as possible and list all the food items visible in the image.
"""

# If submit button is clicked
if submit:
    # Prepare image data for processing
    image_data = input_image_setup(uploaded_file)

    # Get response from Gemini API
    response = get_gemini_response(user_input, image_data, input_prompt)

    # Display response
    st.subheader("Nutritional Assessment:")
    st.write(response)
