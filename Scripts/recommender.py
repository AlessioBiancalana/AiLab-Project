import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import os
import torchvision.transforms as transforms
import cv2

# Default path to metadata CSV
default_metadata_path = "Data/metadata.csv"

def image_transform():
    # Define a sequence of transformations for input images (if needed with CNN)
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

class ContentBasedRecommender:
    def __init__(self, metadata_path=default_metadata_path,
                 features_path="features.npy", ids_path="ids.npy"):
        # Load metadata from CSV and remove entries with missing critical fields
        self.metadata = pd.read_csv(metadata_path)
        self.metadata = self.metadata.dropna(subset=["genres", "description", "cast", "studio", "director"])

        # Load visual features and corresponding IDs
        self.features = np.load(features_path)  # shape: (n_movies, n_features)
        self.ids = np.load(ids_path)            # shape: (n_movies,)

        # Prepare text-based TF-IDF matrix
        self._prepare_text_features()

    def _prepare_text_features(self):
        # Initialize TF-IDF vectorizer
        from sklearn.feature_extraction.text import TfidfVectorizer
        from scipy.sparse import hstack

        vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)

        # Compute TF-IDF for different text fields with different weights
        tfidf_genres = vectorizer.fit_transform(self.metadata["genres"]) * 2
        tfidf_desc = vectorizer.fit_transform(self.metadata["description"]) * 2.5
        tfidf_director = vectorizer.fit_transform(self.metadata["director"]) * 2
        tfidf_cast = vectorizer.fit_transform(self.metadata["cast"]) * 0.5
        tfidf_studio = vectorizer.fit_transform(self.metadata["studio"]) * 1

        # Combine all weighted features into a single matrix
        self.tfidf_matrix = hstack([tfidf_genres, tfidf_desc, tfidf_director, tfidf_cast, tfidf_studio])

    def extract_color_histogram(self, image_path, bins=(8, 8, 8)):
        # Extract a color histogram from the given image
        if not os.path.exists(image_path):
            return None

        image = cv2.imread(image_path)                     # Load image using OpenCV
        image = cv2.resize(image, (128, 128))              # Resize to fixed size
        hist = cv2.calcHist([image], [0, 1, 2], None, bins, # Compute histogram in BGR space
                            [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()         # Normalize and flatten to 1D vector
        return hist

    def find_best_match(self, image_path):
        # Extract visual features from the query image
        query_feat = self.extract_color_histogram(image_path)
        if query_feat is None:
            return None, None

        # Compute Euclidean distances between query and dataset features
        distances = np.linalg.norm(self.features - query_feat, axis=1)

        # Find index of closest match (minimum distance)
        best_idx = np.argmin(distances)

        # Retrieve corresponding ID and metadata record
        best_id = self.ids[best_idx]
        result = self.metadata[self.metadata["id"] == best_id]

        if result.empty:
            return None, None

        return best_id, result.iloc[0]

    def recommend(self, movie_id, top_n=5, alpha=0.5):
        """
        Recommend top N movies based on hybrid similarity (text + visual).
        :param movie_id: ID of the reference movie
        :param top_n: number of recommendations to return
        :param alpha: weight for text similarity (between 0 and 1)
        """
        if movie_id not in self.metadata["id"].values:
            return []

        # Get index of the selected movie
        idx = self.metadata.index[self.metadata["id"] == movie_id][0]

        # --- TEXTUAL SIMILARITY ---
        sim_text = cosine_similarity(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()

        # --- VISUAL SIMILARITY ---
        query_feat = self.features[idx]
        dists = np.linalg.norm(self.features - query_feat, axis=1)
        sim_visual = 1 / (1 + dists)  # Convert distance to similarity

        # --- HYBRID SIMILARITY ---
        hybrid_sim = alpha * sim_text + (1 - alpha) * sim_visual

        # Get indices of top N most similar movies (excluding itself)
        sorted_indices = hybrid_sim.argsort()[::-1]
        sorted_indices = [i for i in sorted_indices if i != idx][:top_n]

        return self.metadata.iloc[sorted_indices]