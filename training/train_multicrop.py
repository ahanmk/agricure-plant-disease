import os
import json
import tensorflow as tf
from tensorflow.keras import layers, models

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 8

DATASET_DIR = os.path.abspath("dataset")
TRAIN_DIR = os.path.join(DATASET_DIR, "train")
VAL_DIR = os.path.join(DATASET_DIR, "val")
TEST_DIR = os.path.join(DATASET_DIR, "test")

SAVED_MODEL_DIR = os.path.abspath("saved_model")
MODEL_EXPORT_PATH = os.path.join(SAVED_MODEL_DIR, "multicrop_model.keras")
CLASSES_EXPORT_PATH = os.path.join(SAVED_MODEL_DIR, "multicrop_classes.json")

def main():
    print(f"Loading datasets from {DATASET_DIR}...")
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        TRAIN_DIR,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=True,
        seed=123
    )

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        VAL_DIR,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False
    )

    test_ds = tf.keras.preprocessing.image_dataset_from_directory(
        TEST_DIR,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False
    )

    class_names = train_ds.class_names
    num_classes = len(class_names)
    print(f"Found {num_classes} classes.")

    os.makedirs(SAVED_MODEL_DIR, exist_ok=True)
    with open(CLASSES_EXPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(class_names, f, indent=2)
    print(f"Exported class names to {CLASSES_EXPORT_PATH}")

    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

    # Base model: MobileNetV2 frozen feature extractor
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = False

    data_augmentation = tf.keras.Sequential([
        layers.RandomFlip("horizontal_and_vertical"),
        layers.RandomRotation(0.15),
        layers.RandomZoom(0.1),
        layers.RandomContrast(0.1)
    ], name="data_augmentation")

    inputs = tf.keras.Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3), name="input_layer")
    x = data_augmentation(inputs)
    x = layers.Rescaling(scale=1./127.5, offset=-1.0)(x)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D(name="avg_pool")(x)
    x = layers.BatchNormalization(name="bn_1")(x)
    x = layers.Dropout(0.4, name="dropout_1")(x)
    x = layers.Dense(256, activation="relu", name="dense_features")(x)
    x = layers.BatchNormalization(name="bn_2")(x)
    x = layers.Dropout(0.3, name="dropout_2")(x)
    outputs = layers.Dense(num_classes, activation="softmax", name="predictions")(x)

    model = tf.keras.Model(inputs, outputs, name="CropDiseaseClassifier")

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    print("\n--- Training Regularized Feature Extraction Head ---")
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        verbose=1
    )

    print("\n--- Evaluating on Test Split ---")
    test_loss, test_acc = model.evaluate(test_ds, verbose=1)
    print(f"Final Test Accuracy: {test_acc * 100:.2f}% | Test Loss: {test_loss:.4f}")

    print(f"Saving multi-crop model to {MODEL_EXPORT_PATH}...")
    model.save(MODEL_EXPORT_PATH)
    print("Multi-crop model saved successfully!")

if __name__ == "__main__":
    main()
