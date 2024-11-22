from fastapi import FastAPI, File, UploadFile
import uvicorn
from io import BytesIO
import numpy as np
from PIL import Image
import tensorflow as tf
from keras.api.models import load_model
import keras

app = FastAPI()

MODEL_POTATO = tf.keras.models.load_model("C:/Users/Marble/Desktop/test/app/models/potatomodel.h5", compile=False)
MODEL_CORN = tf.keras.models.load_model("C:/Users/Marble/Desktop/test/app/models/cornmodel.h5", compile=False)
MODEL_APPLE = tf.keras.models.load_model("C:/Users/Marble/Desktop/test/app/models/applemodel.h5", compile=False)

POTATO_CLASS_NAMES = ["Early Blight", "Healthy", "Late Blight"]
CORN_CLASS_NAMES = ["Cercospora Spot-Gray Leaf Spot", "Common Rust", "Healthy", "Northern Leaf Blight"]
APPLE_CLASS_NAMES = ["Black Rot", "Healthy", "Scab"]


@app.get("/ping")
async def ping():
    return "Hello, I am alive"

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image


@app.post("/predictForPotato")
async def predictForPotato(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)
    prediction = MODEL_POTATO.predict(img_batch)
    predicted_class = POTATO_CLASS_NAMES[np.argmax(prediction[0])]
    confidence = np.max(prediction[0])
    return {
        'predicted_class': predicted_class,
        'accuracy': float(confidence)
    }


@app.post("/predictForCorn")
async def predictForCorn(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)
    prediction = MODEL_CORN.predict(img_batch)
    predicted_class = CORN_CLASS_NAMES[np.argmax(prediction[0])]
    confidence = np.max(prediction[0])
    return {
        'predicted_class': predicted_class,
        'accuracy': float(confidence)
    }


@app.post("/predictForApple")
async def predictForApple(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)
    prediction = MODEL_APPLE.predict(img_batch)
    predicted_class = APPLE_CLASS_NAMES[np.argmax(prediction[0])]
    confidence = np.max(prediction[0])
    return {
        'predicted_class': predicted_class,
        'accuracy': float(confidence)
    }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
