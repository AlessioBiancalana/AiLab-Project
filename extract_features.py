import cv2
import os
import numpy as np
import pandas as pd

# === Load metadata ===
metadata = pd.read_csv("data/metadata.csv")

# === Function to compute RGB color histogram ===
def extract_color_histogram(image_path, bins=(8, 8, 8)):
    image = cv2.imread(image_path)                   # Read the image
    image = cv2.resize(image, (128, 128))            # Resize for uniformity
    hist = cv2.calcHist([image], [0, 1, 2], None, bins,  # RGB histogram
                        [0, 256, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()       # Normalize and flatten
    return hist

features = []
ids = []

# === Extract features for each poster ===
for idx, row in metadata.iterrows():
    poster_path = row["poster_path"]
    if os.path.exists(poster_path):
        feat = extract_color_histogram(poster_path)
        features.append(feat)
        ids.append(row["id"])

# === Save extracted features and corresponding movie IDs ===
np.save("features.npy", np.array(features))
np.save("ids.npy", np.array(ids))
print("✅ Features successfully extracted and saved.")
