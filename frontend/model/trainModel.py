import os

import cv2
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

from MaskCreator import load_annotations_and_create_masks


# Definirea modelului U-Net
def build_unet(input_size=(256, 256, 1)):
    inputs = tf.keras.Input(shape = input_size)


    # Encoder
    conv1 = tf.keras.layers.Conv2D(64, 3, activation="relu", padding="same")(inputs)
    conv1 = tf.keras.layers.Conv2D(64, 3, activation="relu", padding="same")(conv1)
    pool1 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(conv1)

    conv2 = tf.keras.layers.Conv2D(128, 3, activation="relu", padding="same")(pool1)
    conv2 = tf.keras.layers.Conv2D(128, 3, activation="relu", padding="same")(conv2)
    pool2 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(conv2)

    # Bottleneck
    conv3 = tf.keras.layers.Conv2D(256, 3, activation="relu", padding="same")(pool2)
    conv3 = tf.keras.layers.Conv2D(256, 3, activation="relu", padding="same")(conv3)

    # Decoder
    up4 = tf.keras.layers.Conv2DTranspose(128, 2, strides=(2, 2), padding="same")(conv3)
    up4 = tf.keras.layers.concatenate([up4, conv2])
    conv4 = tf.keras.layers.Conv2D(128, 3, activation="relu", padding="same")(up4)
    conv4 = tf.keras.layers.Conv2D(128, 3, activation="relu", padding="same")(conv4)

    up5 = tf.keras.layers.Conv2DTranspose(64, 2, strides=(2, 2), padding="same")(conv4)
    up5 = tf.keras.layers.concatenate([up5, conv1])
    conv5 = tf.keras.layers.Conv2D(64, 3, activation="relu", padding="same")(up5)
    conv5 = tf.keras.layers.Conv2D(64, 3, activation="relu", padding="same")(conv5)

    outputs = tf.keras.layers.Conv2D(1, 1, activation="sigmoid")(conv5)

    model = tf.keras.models.Model(inputs, outputs)
    return model

# Încărcarea datelor
def load_data(image_dir, mask_dir, img_size=(256, 256)):
    images = []
    masks= []
    computedMasks = load_annotations_and_create_masks(mask_dir,img_size)

    img_size=(256,256)
    for img_file in os.listdir(image_dir):
        img_path = os.path.join(image_dir, img_file)

        resized_img = cv2.resize(cv2.imread(img_path, cv2.IMREAD_GRAYSCALE), img_size)
        mask = cv2.resize(src = computedMasks[img_file], dsize =img_size )
        print(mask.shape)
        print(resized_img.shape)


        images.append(tf.keras.utils.img_to_array(resized_img) / 255.0)
        masks.append(tf.keras.utils.img_to_array(mask) / 255.0)

    return np.array(images), np.array(masks)


if __name__ == "__main__":
# Setări
    IMAGE_DIR = r"C:\Users\username\Desktop\BV FINAL\BV FINAL\Borcan Valentina 2\borcan valentina\t2"
    MASK_DIR = "Borcan Valentina_csv T2.csv"    # Schimbă cu calea ta
    IMG_SIZE = (512, 512)
    BATCH_SIZE = 16
    EPOCHS = 50


    # Încărcarea datelor
    images, masks = load_data(IMAGE_DIR, MASK_DIR, IMG_SIZE)

    # Împărțirea datelor în seturi de antrenament și validare
    X_train, X_val, y_train, y_val = train_test_split(images, masks, test_size=0.2, random_state=42)

    input_size=(256,256,1)
    # Construirea modelului
    absolute_path = r"C:\Users\username\Documents\GitHub\CervicalCancerScanner\frontend\model\unet_cervical.keras"
    model= build_unet(input_size)
    opt=tf.keras.optimizers.Adam(learning_rate=0.001)
    model.compile(optimizer=opt, loss="binary_crossentropy", metrics=['accuracy'])
    # Antrenarea modelului
    if tf.test.is_gpu_available :
        model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            batch_size=BATCH_SIZE,
            epochs=EPOCHS
        )

    # Salvarea modelului
    model.save("unet_cervical.keras")