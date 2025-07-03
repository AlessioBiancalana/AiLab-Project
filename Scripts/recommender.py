import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import os
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import cv2

# Default path to metadata CSV
default_metadata_path = "Data/metadata.csv"

def image_transform():
    # Define a sequence of transformations for input images (for CNN)
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

class ContentBasedRecommender:
    def __init__(self, metadata_path=default_metadata_path,
                 features_path="features.npy", ids_path="ids.npy"):
        self.metadata = pd.read_csv(metadata_path)
        self.metadata = self.metadata.dropna(subset=["genres", "description", "cast", "studio", "director"])

        self.features = np.load(features_path)
        self.ids = np.load(ids_path)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        self.model = torch.nn.Sequential(*list(self.model.children())[:-1])  # remove classifier
        self.model.eval().to(self.device)

        self.transform = image_transform()

        self._prepare_text_features()

    def _prepare_text_features(self):
        from sklearn.feature_extraction.text import TfidfVectorizer
        from scipy.sparse import hstack

        vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)

        tfidf_genres = vectorizer.fit_transform(self.metadata["genres"]) * 2
        tfidf_desc = vectorizer.fit_transform(self.metadata["description"]) * 2.5
        tfidf_director = vectorizer.fit_transform(self.metadata["director"]) * 2
        tfidf_cast = vectorizer.fit_transform(self.metadata["cast"]) * 0.5
        tfidf_studio = vectorizer.fit_transform(self.metadata["studio"]) * 1

        self.tfidf_matrix = hstack([tfidf_genres, tfidf_desc, tfidf_director, tfidf_cast, tfidf_studio])

    def extract_visual_features(self, image_path):
        if not os.path.exists(image_path):
            return None

        try:
            image = Image.open(image_path).convert("RGB")
            image = self.transform(image).unsqueeze(0).to(self.device)

            with torch.no_grad():
                features = self.model(image).squeeze().cpu().numpy()
            return features
        except Exception as e:
            print(f"Error processing image: {e}")
            return None

    def find_best_match(self, image_path):
        query_feat = self.extract_visual_features(image_path)
        if query_feat is None:
            return None, None

        # Reshape query to 2D for sklearn
        query_feat = query_feat.reshape(1, -1)
        all_feats = self.features  # shape: (n_movies, 2048)

        # Compute cosine similarity
        sims = cosine_similarity(query_feat, all_feats).flatten()

        # Get the index with highest similarity
        best_idx = np.argmax(sims)
        best_id = self.ids[best_idx]
        result = self.metadata[self.metadata["id"] == best_id]

        if result.empty:
            return None, None

        return best_id, result.iloc[0]

    def recommend(self, movie_id, top_n=5, alpha=0.6):
        if movie_id not in self.metadata["id"].values:
            return []

        idx = self.metadata.index[self.metadata["id"] == movie_id][0]

        cosine_sim = cosine_similarity(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()
        similar_indices = cosine_sim.argsort()[::-1][1:top_n+1]

        return self.metadata.iloc[similar_indices]
