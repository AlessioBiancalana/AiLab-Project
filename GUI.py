import cv2
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import os

# Caricamento dati
features = np.load("features.npy")
ids = np.load("ids.npy")
metadata = pd.read_csv("data/metadata.csv")

# Prepara nearest neighbors
nn = NearestNeighbors(n_neighbors=6, metric="euclidean")
nn.fit(features)

# Font personalizzati
TITLE_FONT = ("Helvetica", 24, "bold")
LABEL_FONT = ("Helvetica", 13)
ITALIC_FONT = ("Helvetica", 13, "italic")
BOLD_LABEL = ("Helvetica", 15, "bold")

# Funzione per estrarre istogramma
def extract_color_histogram(image_path, bins=(8, 8, 8)):
    image = cv2.imread(image_path)
    if image is None:
        return None
    image = cv2.resize(image, (128, 128))
    hist = cv2.calcHist([image], [0, 1, 2], None, bins,
                        [0, 256, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    return hist

# Mostra anteprima immagine
def show_image(path, size=(180, 260)):
    image = Image.open(path).resize(size)
    return ImageTk.PhotoImage(image)

# Funzione principale
def process_image():
    path = filedialog.askopenfilename(
        title="Scegli il poster del film",
        filetypes=[("Immagini", "*.jpg *.jpeg *.png *.bmp")]
    )
    if not path:
        return

    query_feat = extract_color_histogram(path)
    if query_feat is None:
        messagebox.showerror("Errore", "Immagine non valida o non leggibile.")
        return

    distances, indices = nn.kneighbors([query_feat])
    best_idx = indices[0][0]
    best_id = ids[best_idx]
    result = metadata[metadata["id"] == best_id].iloc[0]

    genre = result['genres'].split('|')[0]
    recommendations = metadata[
        metadata['genres'].str.contains(genre) & (metadata['id'] != best_id)
    ].head(5)

    for widget in result_frame.winfo_children():
        widget.destroy()

    top_frame = ttk.Frame(result_frame)
    top_frame.pack(fill=X, pady=10)

    try:
        poster_img = show_image(path)
        img_label = ttk.Label(top_frame, image=poster_img)
        img_label.image = poster_img
        img_label.pack(side=LEFT, padx=10)
    except:
        pass

    info_box = ttk.Labelframe(top_frame, text="🎬 Informazioni Film", padding=10)
    info_box.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

    ttk.Label(info_box, text=result['title'], font=TITLE_FONT).pack(anchor="w", pady=(0, 10))
    ttk.Label(info_box, text=f"📅 Anno: {result['year']}   ⏱️ Durata: {result['duration']} min   ⭐ Rating: {result['rating']}", font=LABEL_FONT).pack(anchor="w")
    ttk.Label(info_box, text=f"🎭 Genere: {result['genres']}", font=LABEL_FONT).pack(anchor="w")
    ttk.Label(info_box, text=f"🏢 Studio: {result['studio']}", font=LABEL_FONT).pack(anchor="w")
    main_actors = result['cast'].split(', ')[:5]
    ttk.Label(info_box, text=f"👥 Cast: {', '.join(main_actors)}", font=LABEL_FONT).pack(anchor="w", pady=5)

    ttk.Separator(result_frame, orient="horizontal").pack(fill=X, pady=10)

    ttk.Label(result_frame, text="📝 Trama:", font=ITALIC_FONT).pack(anchor="w")
    ttk.Label(result_frame, text=result['description'], wraplength=800, font=LABEL_FONT, justify="left").pack(anchor="w")

    ttk.Label(result_frame, text="🎞️ Film simili consigliati:", font=BOLD_LABEL).pack(anchor="w", pady=(20, 10))

    sim_frame = ttk.Frame(result_frame)
    sim_frame.pack(fill=BOTH, expand=True)

    for i, row in recommendations.iterrows():
        sim_box = ttk.Frame(sim_frame)
        sim_box.pack(anchor="w", fill=X, pady=5)

        img_path = f"data/posters/{row['id']}.jpg"
        if os.path.exists(img_path):
            try:
                sim_img = show_image(img_path, size=(100, 150))
                sim_label = ttk.Label(sim_box, image=sim_img)
                sim_label.image = sim_img
                sim_label.pack(side=LEFT, padx=5)
            except:
                pass

        text = f"{row['title']} ({row['year']})\n🎭 {row['genres']}"
        ttk.Label(sim_box, text=text, font=LABEL_FONT, justify="left").pack(anchor="w", padx=10)

# === GUI ===
app = ttk.Window(themename="darkly")
app.title("🎥 Poster Movie Finder - in stile Letterboxd")
app.geometry("950x1000")
app.minsize(850, 900)

ttk.Label(app, text="🎥 Poster Movie Finder", font=("Helvetica", 28, "bold")).pack(pady=25)

ttk.Button(app, text="📁 Carica poster", bootstyle=PRIMARY, command=process_image).pack(pady=15)

result_frame = ttk.Frame(app, padding=25)
result_frame.pack(fill=BOTH, expand=True)

app.mainloop()
