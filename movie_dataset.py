import os
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset

class MoviePosterDataset(Dataset):
    def __init__(self, csv_file, transform=None, label_column="genres"):
        """
        Args:
            csv_file (string): Percorso al file CSV con le annotazioni.
            transform (callable, optional): Trasformazioni da applicare alle immagini.
            label_column (string): Colonna del CSV da usare come etichetta.
        """
        self.annotations = pd.read_csv(csv_file)
        self.transform = transform
        self.label_column = label_column

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, idx):
        # Ottieni percorso immagine
        img_path = self.annotations.iloc[idx]["poster_path"]
        image = Image.open(img_path).convert("RGB")

        # Ottieni la label dalla colonna specificata
        label = self.annotations.iloc[idx][self.label_column]

        if self.transform:
            image = self.transform(image)

        return image, label
