import matplotlib.pyplot as plt
from torchvision import transforms
from torch.utils.data import DataLoader
from movie_dataset import MoviePosterDataset

# Trasformazioni da applicare al poster
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# Carica il dataset
dataset = MoviePosterDataset(
    csv_file="data/metadata.csv",
    transform=transform,
    label_column="genres"  # oppure "studio", "rating"
)

# DataLoader per batch
dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

# Mostra il primo batch
def show_batch():
    for images, labels in dataloader:
        print(f"Immagini: {images.shape}")  # ad esempio [4, 3, 224, 224]
        print(f"Etichette: {labels}")
        # Visualizza il batch
        fig, axs = plt.subplots(1, 4, figsize=(15, 5))
        for i in range(4):
            img = images[i].permute(1, 2, 0)  # da [C,H,W] a [H,W,C]
            axs[i].imshow(img)
            axs[i].axis('off')
            axs[i].set_title(labels[i])
        plt.tight_layout()
        plt.show()
        break

if __name__ == "__main__":
    show_batch()
