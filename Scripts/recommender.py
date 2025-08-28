import pandas as pd  # Data handling
import numpy as np  # Numeric operations
from sklearn.feature_extraction.text import TfidfVectorizer  # Text features
from sklearn.metrics.pairwise import cosine_similarity  # Similarity measure
from PIL import Image  # Image processing
import os  # File system
import torch  # Deep learning
import torchvision.transforms as transforms  # Image transforms
import torchvision.models as models  # Pretrained models

# Default metadata path
default_metadata_path = "Data/metadata.csv"

def image_transform():
    # Define preprocessing for CNN input images
    return transforms.Compose([
        transforms.Resize((224, 224)),  # Resize to 224x224
        transforms.ToTensor(),  # Convert to tensor
        transforms.Normalize(mean=[0.485, 0.456, 0.406],  # Normalize
                             std=[0.229, 0.224, 0.225])
    ])

class ContentBasedRecommender:
    def __init__(self, metadata_path=default_metadata_path,
                 features_path="features.npy", ids_path="ids.npy"):
        self.metadata = pd.read_csv(metadata_path)  # Load metadata
        # Drop rows missing required fields
        self.metadata = self.metadata.dropna(subset=["genres", "description", "cast", "studio", "director"])

        self.features = np.load(features_path)  # Load visual features
        self.ids = np.load(ids_path)  # Load IDs

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # Choose device
        self.model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)  # Pretrained ResNet50
        self.model = torch.nn.Sequential(*list(self.model.children())[:-1])  # Remove classifier layer
        self.model.eval().to(self.device)  # Eval mode, move to device

        self.transform = image_transform()  # Image preprocessing

        self._prepare_text_features()  # Build TF-IDF features

    def _prepare_text_features(self):
        from sklearn.feature_extraction.text import TfidfVectorizer
        from scipy.sparse import hstack

        vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)

        # Create TF-IDF for each metadata field with weights
        tfidf_genres = vectorizer.fit_transform(self.metadata["genres"]) * 2
        tfidf_desc = vectorizer.fit_transform(self.metadata["description"]) * 2.5
        tfidf_director = vectorizer.fit_transform(self.metadata["director"]) * 2
        tfidf_cast = vectorizer.fit_transform(self.metadata["cast"]) * 0.5
        tfidf_studio = vectorizer.fit_transform(self.metadata["studio"]) * 1

        # Combine features into one sparse matrix
        self.tfidf_matrix = hstack([tfidf_genres, tfidf_desc, tfidf_director, tfidf_cast, tfidf_studio])

    def extract_visual_features(self, image_path):
        if not os.path.exists(image_path):  # Skip if missing
            return None

        try:
            image = Image.open(image_path).convert("RGB")  # Open image
            image = self.transform(image).unsqueeze(0).to(self.device)  # Preprocess and send to device

            with torch.no_grad():  # Disable gradients
                features = self.model(image).squeeze().cpu().numpy()  # Extract features
            return features
        except Exception as e:
            print(f"Error processing image: {e}")
            return None

    def find_best_match(self, image_path):
        query_feat = self.extract_visual_features(image_path)  # Get features
        if query_feat is None:
            return None, None

        query_feat = query_feat.reshape(1, -1)  # Reshape for sklearn
        all_feats = self.features  # Precomputed features

        sims = cosine_similarity(query_feat, all_feats).flatten()  # Compute similarity
        best_idx = np.argmax(sims)  # Best index
        best_id = self.ids[best_idx]  # Best match ID
        result = self.metadata[self.metadata["id"] == best_id]  # Metadata row

        if result.empty:
            return None, None

        return best_id, result.iloc[0]  # Return ID and metadata row

    def recommend(self, movie_id, top_n=5, alpha=0.6):
        if movie_id not in self.metadata["id"].values:  # Invalid ID
            return []

        idx = self.metadata.index[self.metadata["id"] == movie_id][0]  # Get index

        # Compute cosine similarity on text features
        cosine_sim = cosine_similarity(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()
        similar_indices = cosine_sim.argsort()[::-1][1:top_n+1]  # Get top N similar

        return self.metadata.iloc[similar_indices]  # Return recommendations
