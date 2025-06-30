import cv2
import matplotlib.pyplot as plt

# Carica l'immagine del poster
image = cv2.imread('Data/Posters/1000007.jpg')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # OpenCV usa BGR, matplotlib usa RGB

# Calcola l'istogramma per ciascun canale (RGB)
color = ('r', 'g', 'b')
plt.figure(figsize=(12, 5))

# Mostra l'immagine originale
plt.subplot(1, 2, 1)
plt.imshow(image_rgb)
plt.title('Movie Poster')
plt.axis('off')

# Istogrammi
plt.subplot(1, 2, 2)
for i, col in enumerate(color):
    hist = cv2.calcHist([image], [i], None, [256], [0, 256])
    plt.plot(hist, color=col)
    plt.xlim([0, 256])
plt.title('RGB Color Histograms')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()
