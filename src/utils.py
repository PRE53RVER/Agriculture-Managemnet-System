import magic
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os

soil_plants_fertilizers = {
    "Black Soil": {
        "Suggested Plants": ["Cotton", "Wheat", "Soybeans", "Gram (Chickpeas)", "Peanuts", "Sugarcane", "Sunflowers"],
        "Suggested Fertilizers": ["Farmyard Manure", "Vermicompost", "NPK Fertilizers"]
    },
    "The Given image is not of a Soil": {
        "Suggested Plants": [""],
        "Suggested Fertilizers": [""]
    },
    "Laterite Soil": {
        "Suggested Plants": ["Cashew", "Rubber", "Teak", "Bamboo", "Orchids"],
        "Suggested Fertilizers": ["Organic Fertilizers", "Phosphorus-rich Fertilizers"]
    },
    "Peat Soil": {
        "Suggested Plants": ["Sphagnum Moss", "Azaleas", "Rhododendrons", "Carnivorous Plants"],
        "Suggested Fertilizers": ["Acidic Fertilizers", "Slow-release Fertilizers"]
    },
    "Yellow Soil": {
        "Suggested Plants": ["Maize", "Sorghum", "Millet", "Sesame", "Peanuts", "Castor"],
        "Suggested Fertilizers": ["Farmyard Manure", "NPK Fertilizers", "Potassium-rich Fertilizers"]
    }
}


current_file_path = os.path.dirname(os.path.abspath(__file__))
model = load_model(os.path.join(current_file_path, 'my_model.h5'), custom_objects={'KerasLayer': hub.KerasLayer})
def is_image_file(filename):
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(filename)
    return file_type.startswith('image/')


def predict(img_test):
    img_pil = Image.open(img_test)
    img_resize = img_pil.resize((224, 224))
    img_np = np.array(img_resize)
    img_scaled = img_np / 255.0
    img_reshaped = np.reshape(img_scaled, [1, 224, 224, 3])
    input_pred = model.predict(img_reshaped)
    input_label = np.argmax(input_pred)
    if input_label == 0:
        result =  "Black Soil"
    elif input_label == 1:
        result =  "The Given image is not of a Soil"
    elif input_label == 2:
        result =  "Laterite Soil"
    elif input_label == 3:
        result =  "Peat Soil"
    elif input_label == 4:
        result = "Yellow Soil"

    return {"soil" : result, "plants" : soil_plants_fertilizers[result]["Suggested Plants"], "fertilizers" : soil_plants_fertilizers[result]["Suggested Fertilizers"]}


