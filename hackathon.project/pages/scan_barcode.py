import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("Scan Medicine Barcode")

# Option 1: Camera
camera_image = st.camera_input("Take a picture of the barcode")

# Option 2: Upload image
uploaded_file = st.file_uploader(
    "Or upload a barcode image",
    type=["png", "jpg", "jpeg"]
)

image = None

if camera_image:
    image = Image.open(camera_image)

elif uploaded_file:
    image = Image.open(uploaded_file)

if image:

    st.image(image, caption="Barcode Image", use_column_width=True)

    image_np = np.array(image)

    detector = cv2.barcode.BarcodeDetector()

    decoded_info, decoded_type, points = detector.detectAndDecode(image_np)

    if decoded_info:
        barcode_number = decoded_info[0]
        st.success(f"Barcode detected: {barcode_number}")
    else:
        st.error("No barcode detected. Try a clearer image.")