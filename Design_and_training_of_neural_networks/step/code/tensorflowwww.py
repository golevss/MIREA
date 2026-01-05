import os
import numpy as np
import tensorflow as tf
import pandas as pd

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_ROOT = SCRIPT_DIR

TRAIN_DIR = os.path.join(DATA_ROOT, "train")
VAL_DIR   = os.path.join(DATA_ROOT, "val")
TEST_DIR  = os.path.join(DATA_ROOT, "test")

IMG_SIZE  = (224, 224)
BATCH_SIZE = 16
SEED = 42

# =====================
# Проверка структуры
# =====================
def print_dir_structure(root):
    print(f"\nСтруктура: {root}")
    if not os.path.exists(root):
        print("  (нет такой папки)")
        return
    for cls in sorted(os.listdir(root)):
        p = os.path.join(root, cls)
        if os.path.isdir(p):
            print(f"  - {cls}: {len(os.listdir(p))} изображений")

print_dir_structure(TRAIN_DIR)
print_dir_structure(VAL_DIR)
print_dir_structure(os.path.join(TEST_DIR, "unknown"))

# =====================
# Генераторы (ResNet50)
# =====================
train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest",
    brightness_range=[0.8, 1.2],
)

val_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input
)

test_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input
)

train_gen = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    shuffle=True,
    seed=SEED
)

val_gen = val_datagen.flow_from_directory(
    VAL_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    shuffle=False
)


test_gen = test_datagen.flow_from_directory(
    TEST_DIR,
    classes=["unknown"],
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode=None,
    shuffle=False
)

class_names = list(train_gen.class_indices.keys())
print("\nКлассы (как видит TF):", class_names)

# =====================
# Модель (как у тебя)
# =====================
base_model = ResNet50(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False

x = GlobalAveragePooling2D()(base_model.output)
x = Dense(512, activation="relu")(x)
x = Dropout(0.5)(x)
out = Dense(1, activation="sigmoid")(x)

model = Model(inputs=base_model.input, outputs=out)

model.compile(
    optimizer=Adam(learning_rate=1e-4),
    loss="binary_crossentropy",
    metrics=[
        "accuracy",
        tf.keras.metrics.Precision(name="precision"),
        tf.keras.metrics.Recall(name="recall"),
    ],
)

model.summary()

# =====================
# Колбэки
# =====================
callbacks = [
    EarlyStopping(monitor="val_loss", patience=3, restore_best_weights=True),
    ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2, verbose=1),
    ModelCheckpoint("best_tf_resnet50.h5", monitor="val_loss", save_best_only=True),
]

# =====================
# Обучение
# =====================
history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=100,
    callbacks=callbacks
)

model.save("binary_posyda_classification_resnet_tf.h5")

# =====================
# Предсказания на test/unknown
# =====================
pred_proba = model.predict(test_gen, verbose=1).ravel()
pred_label = (pred_proba >= 0.5).astype(int)


filepaths = test_gen.filepaths
filenames = [os.path.basename(p) for p in filepaths]

# print("\nПример предсказаний:")
# for i in range(min(5, len(filenames))):
#     print(filenames[i], "->", pred_label[i], f"(p={pred_proba[i]:.3f})")



probs = model.predict(test_gen, verbose=1).ravel()

labels = ["cleaned", "dirty"]

pred_ids = (probs >= 0.5).astype(int)
pred_labels = [labels[i] for i in pred_ids]
filenames = [os.path.basename(p) for p in test_gen.filepaths]

ids = [os.path.splitext(f)[0] for f in filenames]

df = pd.DataFrame({
    "id": ids,
    "label": pred_labels
})
df.to_csv("submission.csv", index=False)
