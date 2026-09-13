import os
import json
import numpy as np
from PIL import Image
import keras

# Support both local backend/ and root-relative paths
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "saved_model", "multicrop_model.keras")
)
CLASSES_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "saved_model", "multicrop_classes.json")
)

# Fallback to parent dir if running from outer workspace
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = os.path.abspath(
        os.path.join(BASE_DIR, "..", "saved_model", "multicrop_model.keras")
    )
    CLASSES_PATH = os.path.abspath(
        os.path.join(BASE_DIR, "..", "saved_model", "multicrop_classes.json")
    )

CROP_DISPLAY_NAMES = {
    "Apple": "Apple",
    "Pepper,_bell": "Bell Pepper",
    "Cherry_(including_sour)": "Cherry",
    "Corn_(maize)": "Corn (Maize)",
    "Grape": "Grape",
    "Potato": "Potato",
    "Strawberry": "Strawberry",
    "Tomato": "Tomato"
}

class MultiCropClassifier:
    def __init__(self, model_path: str = MODEL_PATH, classes_path: str = CLASSES_PATH):
        self.model_path = model_path
        self.classes_path = classes_path
        self.model = None
        self.classes = []

    def load_model(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found at {self.model_path}")
        if not os.path.exists(self.classes_path):
            raise FileNotFoundError(f"Classes file not found at {self.classes_path}")

        print(f"Loading multi-crop model from {self.model_path}...")
        self.model = keras.models.load_model(self.model_path)
        with open(self.classes_path, "r", encoding="utf-8") as f:
            self.classes = json.load(f)
        print(f"Multi-crop model loaded successfully with {len(self.classes)} classes.")

    def format_crop_name(self, raw_crop: str) -> str:
        return CROP_DISPLAY_NAMES.get(raw_crop, raw_crop.replace("_", " "))

    def format_disease_name(self, raw_disease: str) -> str:
        return raw_disease.replace("_", " ").strip()

    def predict(self, image: Image.Image) -> dict:
        if self.model is None:
            raise RuntimeError("Model is not loaded.")

        # Resize to 224x224 matching MobileNetV2 input shape
        img_resized = image.convert("RGB").resize((224, 224))
        img_arr = np.expand_dims(np.array(img_resized, dtype=np.float32), axis=0)

        preds = self.model.predict(img_arr, verbose=0)[0]
        top_idx = int(np.argmax(preds))
        raw_label = self.classes[top_idx]
        confidence = float(preds[top_idx]) * 100.0

        if "___" in raw_label:
            raw_crop, raw_condition = raw_label.split("___", 1)
        else:
            raw_crop, raw_condition = "Unknown", raw_label

        crop_name = self.format_crop_name(raw_crop)
        disease_name = self.format_disease_name(raw_condition)

        return {
            "raw_label": raw_label,
            "crop": crop_name,
            "disease": disease_name,
            "confidence": round(confidence, 2)
        }

classifier = MultiCropClassifier()
