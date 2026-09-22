import glob
import io
import numpy as np
from PIL import Image
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from api.main import app

def run_tests():
    with TestClient(app) as client:
        print("1. Health Check:")
        h = client.get("/health")
        print("  ", h.json())
        assert h.status_code == 200
        assert h.json()["supported_classes"] == 31

        tests = [
            ("Apple Cedar Rust", "dataset/test/Apple___Cedar_apple_rust/*.JPG"),
            ("Potato Healthy", "dataset/test/Potato___healthy/*.JPG"),
            ("Corn Common Rust", "dataset/test/Corn_(maize)___Common_rust_/*.JPG"),
            ("Grape Black Rot", "dataset/test/Grape___Black_rot/*.JPG"),
            ("Tomato Septoria", "dataset/test/Tomato___Septoria_leaf_spot/*.JPG"),
            ("Strawberry Scorch", "dataset/test/Strawberry___Leaf_scorch/*.JPG"),
        ]

        print("\n2. Leaf Predictions Across Crops:")
        for name, pattern in tests:
            files = glob.glob(pattern)
            if not files:
                continue
            with open(files[0], "rb") as f:
                res = client.post("/predict", files={"file": ("leaf.jpg", f, "image/jpeg")})
            data = res.json()
            is_leaf = data["is_leaf"]
            crop = data["crop"]
            disease = data["disease"]
            conf = data["confidence"]
            print(f"   {name:<20} -> is_leaf: {is_leaf}, crop: {crop}, disease: {disease}, conf: {conf}%")
            assert is_leaf is True
            assert data["advisory"] is not None

        print("\n3. Non-Leaf Gatekeeper Tests:")
        # Solid blue
        blue = Image.fromarray(np.zeros((224, 224, 3), dtype=np.uint8) + np.array([20, 50, 220], dtype=np.uint8))
        buf = io.BytesIO()
        blue.save(buf, format="JPEG")
        buf.seek(0)
        r1 = client.post("/predict", files={"file": ("car.jpg", buf, "image/jpeg")}).json()
        print(f"   Blue Object  -> is_leaf: {r1['is_leaf']} | Msg: {r1['message']}")
        assert r1["is_leaf"] is False

        # Skin / portrait tone
        skin = Image.fromarray(np.zeros((224, 224, 3), dtype=np.uint8) + np.array([220, 175, 140], dtype=np.uint8))
        buf = io.BytesIO()
        skin.save(buf, format="JPEG")
        buf.seek(0)
        r2 = client.post("/predict", files={"file": ("face.jpg", buf, "image/jpeg")}).json()
        print(f"   Face / Skin  -> is_leaf: {r2['is_leaf']} | Msg: {r2['message']}")
        assert r2["is_leaf"] is False

        # Noise
        noise = Image.fromarray(np.uint8(np.random.randint(0, 256, (224, 224, 3))))
        buf = io.BytesIO()
        noise.save(buf, format="JPEG")
        buf.seek(0)
        r3 = client.post("/predict", files={"file": ("noise.jpg", buf, "image/jpeg")}).json()
        print(f"   Random Noise -> is_leaf: {r3['is_leaf']} | Msg: {r3['message']}")
        assert r3["is_leaf"] is False

        print("\n4. Input Validation & Error Handling Tests:")

        # Unsupported extension (.txt)
        res_ext = client.post("/predict", files={"file": ("test.txt", b"some text", "text/plain")})
        print(f"   Unsupported ext (.txt) -> Status: {res_ext.status_code}, Detail: {res_ext.json().get('detail')}")
        assert res_ext.status_code == 400

        # Empty file (0 bytes)
        res_empty = client.post("/predict", files={"file": ("empty.jpg", b"", "image/jpeg")})
        print(f"   Empty file (0 bytes)   -> Status: {res_empty.status_code}, Detail: {res_empty.json().get('detail')}")
        assert res_empty.status_code == 400

        # Oversized file (>10 MB)
        big_content = b"0" * (10 * 1024 * 1024 + 100)
        res_big = client.post("/predict", files={"file": ("large.png", big_content, "image/png")})
        print(f"   Oversized file (>10MB) -> Status: {res_big.status_code}, Detail: {res_big.json().get('detail')}")
        assert res_big.status_code == 400

        # RGBA PNG Image Mode Conversion Test
        rgba_img = Image.new("RGBA", (224, 224), (50, 180, 50, 255))
        rgba_buf = io.BytesIO()
        rgba_img.save(rgba_buf, format="PNG")
        rgba_buf.seek(0)
        res_rgba = client.post("/predict", files={"file": ("rgba_leaf.png", rgba_buf, "image/png")})
        print(f"   RGBA PNG Conversion    -> Status: {res_rgba.status_code}, is_leaf: {res_rgba.json().get('is_leaf')}")
        assert res_rgba.status_code == 200

    print("\n>>> ALL END-TO-END & ROBUSTNESS VERIFICATION CHECKS PASSED WITH EXCELLENCE! <<<")

if __name__ == "__main__":
    run_tests()
