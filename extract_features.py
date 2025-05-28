import cv2
import os
import numpy as np
import pandas as pd

# Carica i metadati
metadata = pd.read_csv("data/metadata.csv")

# Funzione per calcolare istogramma RGB
def extract_color_histogram(image_path, bins=(8, 8, 8)):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (128, 128))
    hist = cv2.calcHist([image], [0, 1, 2], None, bins,
                        [0, 256, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    return hist

features = []
ids = []

for idx, row in metadata.iterrows():
    poster_path = row["poster_path"]
    if os.path.exists(poster_path):
        feat = extract_color_histogram(poster_path)
        features.append(feat)
        ids.append(row["id"])

# Salva
np.save("features.npy", np.array(features))
np.save("ids.npy", np.array(ids))
print("✅ Features estratte e salvate con successo.")
