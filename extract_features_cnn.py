import os
import numpy as np
import pandas as pd
from PIL import Image
import torch
import torchvision.transforms as transforms
import torchvision.models as models

# === Config ===
metadata_path = "Data/metadata.csv"
features_out = "features.npy"
ids_out = "ids.npy"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# === Model Setup ===
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model = torch.nn.Sequential(*list(model.children())[:-1])  # remove classifier
model.eval().to(device)

# === Transformations ===
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# === Load metadata ===
metadata = pd.read_csv(metadata_path)
features = []
ids = []

print("🚀 Extracting features using ResNet50...")

for idx, row in metadata.iterrows():
    image_path = row["poster_path"]
    if not os.path.exists(image_path):
        print(f"❌ Missing: {image_path}")
        continue

    try:
        image = Image.open(image_path).convert("RGB")
        image = transform(image).unsqueeze(0).to(device)

        with torch.no_grad():
            feature = model(image).squeeze().cpu().numpy()

        features.append(feature)
        ids.append(row["id"])

        if idx % 25 == 0:
            print(f"✅ Processed {idx+1}/{len(metadata)}")

    except Exception as e:
        print(f"⚠️ Error processing {image_path}: {e}")

# === Save features ===
np.save(features_out, np.array(features))
np.save(ids_out, np.array(ids))
print("✅ Feature extraction complete. Files saved:")
print(f"  - {features_out}")
print(f"  - {ids_out}")
