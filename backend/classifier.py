import os
import json
import numpy as np
from PIL import Image

BASE_DIR = os.path.dirname(__file__)

TFLITE_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "saved_model", "multicrop_model.tflite")
)
MODEL_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "saved_model", "multicrop_model.keras")
)
CLASSES_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "saved_model", "multicrop_classes.json")
)

# Fallbacks to parent dir if running from root workspace
if not os.path.exists(TFLITE_PATH):
    TFLITE_PATH = os.path.abspath(
        os.path.join(BASE_DIR, "..", "saved_model", "multicrop_model.tflite")
    )
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = os.path.abspath(
        os.path.join(BASE_DIR, "..", "saved_model", "multicrop_model.keras")
    )
if not os.path.exists(CLASSES_PATH):
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
    def __init__(self, tflite_path: str = TFLITE_PATH, model_path: str = MODEL_PATH, classes_path: str = CLASSES_PATH):
        self.tflite_path = tflite_path
        self.model_path = model_path
        self.classes_path = classes_path
        self.model = None
        self.interpreter = None
        self.use_tflite = False
        self.classes = []

    def load_model(self):
        if not os.path.exists(self.classes_path):
            raise FileNotFoundError(f"Classes file not found at {self.classes_path}")

        with open(self.classes_path, "r", encoding="utf-8") as f:
            self.classes = json.load(f)

        # Prefer TFLite for cloud deployment (low RAM ~35MB vs ~500MB)
        if os.path.exists(self.tflite_path):
            try:
                print(f"Loading TFLite model from {self.tflite_path}...")
                try:
                    import tflite_runtime.interpreter as tflite
                    self.interpreter = tflite.Interpreter(model_path=self.tflite_path)
                except ImportError:
                    import tensorflow as tf
                    self.interpreter = tf.lite.Interpreter(model_path=self.tflite_path)
                self.interpreter.allocate_tensors()
                self.input_details = self.interpreter.get_input_details()
                self.output_details = self.interpreter.get_output_details()
                self.use_tflite = True
                print(f"TFLite multi-crop model loaded successfully with {len(self.classes)} classes.")
                return
            except Exception as e:
                print(f"TFLite loading failed ({e}); falling back to standard Keras...")

        # Fallback to Keras model
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Neither TFLite nor Keras model found ({self.tflite_path}, {self.model_path})")

        print(f"Loading Keras model from {self.model_path}...")
        import keras
        self.model = keras.models.load_model(self.model_path)
        self.use_tflite = False
        print(f"Keras multi-crop model loaded successfully with {len(self.classes)} classes.")

    def is_ready(self) -> bool:
        return (self.model is not None) or (self.interpreter is not None)

    def format_crop_name(self, raw_crop: str) -> str:
        return CROP_DISPLAY_NAMES.get(raw_crop, raw_crop.replace("_", " "))

    def format_disease_name(self, raw_disease: str) -> str:
        return raw_disease.replace("_", " ").strip()

    def predict(self, image: Image.Image) -> dict:
        if not self.use_tflite and self.model is None and self.interpreter is None:
            raise RuntimeError("Model is not loaded.")

        # Resize to 224x224 matching model input shape
        img_resized = image.convert("RGB").resize((224, 224))
        img_arr = np.expand_dims(np.array(img_resized, dtype=np.float32), axis=0)

        if self.use_tflite:
            self.interpreter.set_tensor(self.input_details[0]["index"], img_arr)
            self.interpreter.invoke()
            preds = self.interpreter.get_tensor(self.output_details[0]["index"])[0]
        else:
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
