import os
import shutil
import random

SOURCE_DIR = os.path.abspath("temp_pv/raw/color")
TARGET_DIR = os.path.abspath("dataset")

TRAIN_COUNT = 100
VAL_COUNT = 30
TEST_COUNT = 15

CLASSES = sorted([
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"
])

def main():
    random.seed(42)
    os.makedirs(os.path.join(TARGET_DIR, "train"), exist_ok=True)
    os.makedirs(os.path.join(TARGET_DIR, "val"), exist_ok=True)
    os.makedirs(os.path.join(TARGET_DIR, "test"), exist_ok=True)

    print(f"Preparing balanced dataset for {len(CLASSES)} classes...")
    total_copied = 0

    for cls in CLASSES:
        src_cls_dir = os.path.join(SOURCE_DIR, cls)
        if not os.path.exists(src_cls_dir):
            raise FileNotFoundError(f"Missing source directory: {src_cls_dir}")

        all_imgs = sorted([
            f for f in os.listdir(src_cls_dir)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ])
        random.shuffle(all_imgs)

        train_imgs = all_imgs[:TRAIN_COUNT]
        val_imgs = all_imgs[TRAIN_COUNT:TRAIN_COUNT + VAL_COUNT]
        test_imgs = all_imgs[TRAIN_COUNT + VAL_COUNT:TRAIN_COUNT + VAL_COUNT + TEST_COUNT]

        splits = [
            ("train", train_imgs),
            ("val", val_imgs),
            ("test", test_imgs)
        ]

        for split_name, imgs in splits:
            dest_dir = os.path.join(TARGET_DIR, split_name, cls)
            os.makedirs(dest_dir, exist_ok=True)
            for img in imgs:
                shutil.copy2(os.path.join(src_cls_dir, img), os.path.join(dest_dir, img))
                total_copied += 1

    print(f"Dataset preparation complete! Total files copied: {total_copied}")
    print(f"Train: {len(CLASSES) * TRAIN_COUNT}, Val: {len(CLASSES) * VAL_COUNT}, Test: {len(CLASSES) * TEST_COUNT}")

if __name__ == "__main__":
    main()
