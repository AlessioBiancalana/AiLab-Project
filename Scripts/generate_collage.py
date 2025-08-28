import os
from PIL import Image, ImageFilter
import random  

# === Config ===
POSTER_DIR = "Data/Posters"              # Folder with poster images
OUTPUT_PATH = "Assets/background.jpg"    # Output collage path
POSTER_SIZE = (200, 300)                 # Size of each poster
GRID_COLUMNS = 22                        # Number of columns in grid
MAX_IMAGES = 220                         # Max number of images

# === Create collage ===
def create_collage():
    # Collect image paths (only jpg/png), limit to MAX_IMAGES
    image_paths = [os.path.join(POSTER_DIR, f) for f in os.listdir(POSTER_DIR)
                   if f.lower().endswith(('.jpg', '.png'))][:MAX_IMAGES]
    random.shuffle(image_paths)  # Shuffle images

    if not image_paths:  # Exit if no images
        print("❌ No images found in folder.")
        return

    images = []
    for path in image_paths:
        try:
            img = Image.open(path).resize(POSTER_SIZE)  # Open and resize
            images.append(img)
        except Exception as e:
            print(f"⚠️ Error with {path}: {e}")  # Skip if error

    # Calculate grid dimensions
    rows = (len(images) + GRID_COLUMNS - 1) // GRID_COLUMNS
    collage_width = POSTER_SIZE[0] * GRID_COLUMNS
    collage_height = POSTER_SIZE[1] * rows

    # Create empty collage (dark background)
    collage = Image.new('RGB', (collage_width, collage_height), color=(20, 20, 40))

    # Paste each image into grid
    for index, img in enumerate(images):
        x = (index % GRID_COLUMNS) * POSTER_SIZE[0]
        y = (index // GRID_COLUMNS) * POSTER_SIZE[1]
        collage.paste(img, (x, y))

    # Optional blur effect
    collage = collage.filter(ImageFilter.GaussianBlur(2))

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)  # Ensure output folder
    collage.save(OUTPUT_PATH)  # Save collage
    print(f"✅ Collage saved at: {OUTPUT_PATH} ({collage_width}x{collage_height})")

if __name__ == "__main__":  # Run if executed directly
    create_collage()
