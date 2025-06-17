import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import os
import torchvision.transforms as transforms
import cv2

default_metadata_path = "Data/metadata.csv"

def image_transform():
    # Compose a set of image transformations: resize image to 224x224 and convert to tensor
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

class ContentBasedRecommender:
    def __init__(self, metadata_path=default_metadata_path,
                 features_path="features.npy", ids_path="ids.npy"):
        self.metadata = pd.read_csv(metadata_path)
        self.metadata = self.metadata.dropna(subset=["genres", "description", "cast", "studio", "director"])

        # Load precomputed visual features and ids
        self.features = np.load(features_path)
        self.ids = np.load(ids_path)

        # Prepare TF-IDF for text-based recommendations (come prima)
        self._prepare_text_features()

    def _prepare_text_features(self):
        from sklearn.feature_extraction.text import TfidfVectorizer
        from scipy.sparse import hstack
        
        vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
        tfidf_genres = vectorizer.fit_transform(self.metadata["genres"]) * 1.5
        tfidf_desc = vectorizer.fit_transform(self.metadata["description"]) * 2.5
        tfidf_director = vectorizer.fit_transform(self.metadata["director"]) * 2
        tfidf_cast = vectorizer.fit_transform(self.metadata["cast"]) * 0.5
        tfidf_studio = vectorizer.fit_transform(self.metadata["studio"]) * 1
        self.tfidf_matrix = hstack([tfidf_genres, tfidf_desc, tfidf_director, tfidf_cast, tfidf_studio])

    def extract_color_histogram(self, image_path, bins=(8, 8, 8)):
        if not os.path.exists(image_path):
            return None
        image = cv2.imread(image_path)
        image = cv2.resize(image, (128, 128))
        hist = cv2.calcHist([image], [0, 1, 2], None, bins,
                            [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        return hist

    def find_best_match(self, image_path):
        # Estrai feature del poster di input
        query_feat = self.extract_color_histogram(image_path)
        if query_feat is None:
            return None, None

        # Calcola distanza euclidea tra query e tutte le feature nel dataset
        distances = np.linalg.norm(self.features - query_feat, axis=1)

        # Prendi indice con distanza minima (miglior match)
        best_idx = np.argmin(distances)

        # Prendi l'id corrispondente e il record metadata
        best_id = self.ids[best_idx]
        result = self.metadata[self.metadata["id"] == best_id]
        if result.empty:
            return None, None
        return best_id, result.iloc[0]
    
    def recommend(self, movie_id, top_n=5):
        if movie_id not in self.metadata["id"].values:
            return []

        idx = self.metadata.index[self.metadata["id"] == movie_id][0]
        cosine_sim = cosine_similarity(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()
        similar_indices = cosine_sim.argsort()[::-1][1:top_n+1]
        return self.metadata.iloc[similar_indices]
