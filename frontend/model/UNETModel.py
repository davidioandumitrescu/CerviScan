import streamlit as st
import numpy as np
import cv2
import tensorflow as tf


absolute_path=r"C:\Users\Raul\Documents\GitHub\CervicalCancerScanner\frontend\model\unet_cervical.keras"
@st.cache_resource
def load_unet_model():
    model = tf.keras.models.load_model(absolute_path)
    return model


def iterate_over_images(images):
    model=load_unet_model()
    model.compile()
    loaded_images=[]
    for image in images:
        loaded_images.append(cv2.imread(image))
    result_images = []
    for image in loaded_images:
        result_image = predict_and_highlight(image,model)
        st.image(result_image, caption="Highlighted Image", use_column_width=True)
        result_images.append(result_image)
    return result_images

def predict_and_highlight(image,model):
    img_resized = cv2.resize(image, (256, 256), interpolation=cv2.INTER_AREA)
    if img_resized.shape[2] == 3:
        img_resized = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    img_array = img_resized / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    if model:
        mask_pred = model.predict(img_array)[0, :, :, 0]
    else:
        mask_pred = np.zeros((256, 256))

    mask_pred = (mask_pred > 0.5).astype(np.uint8)
    mask_pred = cv2.resize(mask_pred, (image.shape[1], image.shape[0]))

    contours, _ = cv2.findContours(mask_pred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    result_image = image.copy()
    for contour in contours:
        if cv2.contourArea(contour) > 100:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            cv2.circle(result_image, center, int(radius), (255, 0, 0), 2)

    return result_image
