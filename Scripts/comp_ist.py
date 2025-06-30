import cv2
import matplotlib.pyplot as plt

# === Inserisci i percorsi dei due poster ===
path1 = 'Data/Posters/1000001.jpg'
path2 = 'Data/Posters/1000009.jpg'

# Carica e converti in RGB
img1 = cv2.imread(path1)
img2 = cv2.imread(path2)
img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

# Canali colore
color = ('r', 'g', 'b')

# === Plot ===
fig, axs = plt.subplots(2, 2, figsize=(12, 8))

# Immagine 1
axs[0, 0].imshow(img1_rgb)
axs[0, 0].set_title('Poster 1')
axs[0, 0].axis('off')

# Istogramma 1
axs[0, 1].set_title('Histogram - Poster 1')
for i, col in enumerate(color):
    hist = cv2.calcHist([img1], [i], None, [256], [0, 256])
    axs[0, 1].plot(hist, color=col)
axs[0, 1].set_xlim([0, 256])

# Immagine 2
axs[1, 0].imshow(img2_rgb)
axs[1, 0].set_title('Poster 2')
axs[1, 0].axis('off')

# Istogramma 2
axs[1, 1].set_title('Histogram - Poster 2')
for i, col in enumerate(color):
    hist = cv2.calcHist([img2], [i], None, [256], [0, 256])
    axs[1, 1].plot(hist, color=col)
axs[1, 1].set_xlim([0, 256])

plt.tight_layout()
plt.show()
