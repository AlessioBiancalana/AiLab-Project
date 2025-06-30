import os
from PIL import Image, ImageFilter
import random

# === Config ===
POSTER_DIR = "Data/Posters"              # Cartella dove hai i poster
OUTPUT_PATH = "Assets/background.jpg"    # Dove salvare il collage
POSTER_SIZE = (200, 300)                 # Dimensione di ciascun poster
GRID_COLUMNS = 22                        # Quante colonne
MAX_IMAGES = 220                         # Numero massimo di immagini nel collage

# === Crea collage ===
def create_collage():
    image_paths = [os.path.join(POSTER_DIR, f) for f in os.listdir(POSTER_DIR)
                   if f.lower().endswith(('.jpg', '.png'))][:MAX_IMAGES]
    random.shuffle(image_paths)  # 🔀 Ordine sparso

    if not image_paths:
        print("❌ Nessuna immagine trovata nella cartella.")
        return

    images = []
    for path in image_paths:
        try:
            img = Image.open(path).resize(POSTER_SIZE)
            images.append(img)
        except Exception as e:
            print(f"⚠️ Errore con {path}: {e}")

    rows = (len(images) + GRID_COLUMNS - 1) // GRID_COLUMNS
    collage_width = POSTER_SIZE[0] * GRID_COLUMNS
    collage_height = POSTER_SIZE[1] * rows

    collage = Image.new('RGB', (collage_width, collage_height), color=(20, 20, 40))  # sfondo scuro

    for index, img in enumerate(images):
        x = (index % GRID_COLUMNS) * POSTER_SIZE[0]
        y = (index // GRID_COLUMNS) * POSTER_SIZE[1]
        collage.paste(img, (x, y))

    # Sfocatura leggera (opzionale)
    collage = collage.filter(ImageFilter.GaussianBlur(2))

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    collage.save(OUTPUT_PATH)
    print(f"✅ Collage salvato in: {OUTPUT_PATH} ({collage_width}x{collage_height})")

if __name__ == "__main__":
    create_collage()
