import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import os
import torchvision.transforms as transforms
default_metadata_path = "Data/metadata.csv"

def image_transform():
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

class ContentBasedRecommender:
    def __init__(self, metadata_path=default_metadata_path):
        self.metadata = pd.read_csv(metadata_path)
        self._prepare()

    def _prepare(self):
        self.metadata = self.metadata.dropna(subset=["genres", "description", "cast"])
        self.metadata["text"] = self.metadata["genres"] + " " + self.metadata["description"] + " " + self.metadata["cast"]
        self.vectorizer = TfidfVectorizer(stop_words="english", max_features=10000)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.metadata["text"])

    def find_best_match(self, image_path):
        # Semplice placeholder: confronta solo il nome del file per matchare con il dataset
        filename = os.path.basename(image_path)
        match = self.metadata[self.metadata['poster_path'].str.contains(filename, na=False)]
        if match.empty:
            return None, None
        return match.iloc[0]['id'], match.iloc[0]

    def recommend(self, movie_id, top_n=5):
        if movie_id not in self.metadata["id"].values:
            return []

        idx = self.metadata.index[self.metadata["id"] == movie_id][0]
        cosine_sim = cosine_similarity(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()
        similar_indices = cosine_sim.argsort()[::-1][1:top_n+1]
        return self.metadata.iloc[similar_indices]
