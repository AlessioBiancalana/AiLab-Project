import cv2
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# Carica le feature e metadati
features = np.load("features.npy")
ids = np.load("ids.npy")
metadata = pd.read_csv("data/metadata.csv")

# Funzione per estrarre istogramma dal poster input
def extract_color_histogram(image_path, bins=(8, 8, 8)):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (128, 128))
    hist = cv2.calcHist([image], [0, 1, 2], None, bins,
                        [0, 256, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    return hist

# === INPUT ===
input_poster = "sample_poster.jpg"  # ← cambialo col tuo file .jpg

query_feat = extract_color_histogram(input_poster)

# Fit KNN su dataset
nn = NearestNeighbors(n_neighbors=6, metric="euclidean")
nn.fit(features)

# Trova simili
distances, indices = nn.kneighbors([query_feat])

# Primo risultato = match più vicino
best_idx = indices[0][0]
best_id = ids[best_idx]
result = metadata[metadata["id"] == best_id].iloc[0]

# Output info film trovato
print(f"🎬 Film riconosciuto:")
print(f"Titolo: {result['title']}")
print(f"Anno: {result['year']}")
print(f"Durata: {result['duration']} min")
print(f"Rating: {result['rating']}")
print(f"Genere: {result['genres']}")
print(f"Studio: {result['studio']}")
print(f"Cast: {result['cast']}")
print(f"Trama: {result['description']}\n")

# Raccomanda altri film con stesso genere
genre = result['genres'].split('|')[0]  # usa il primo genere
recommendations = metadata[metadata['genres'].str.contains(genre) & (metadata['id'] != best_id)].head(5)

print("🎞️ Film simili consigliati:")
for i, row in recommendations.iterrows():
    print(f"- {row['title']} ({row['year']}) [{row['genres']}]")
