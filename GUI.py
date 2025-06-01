import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from Scripts.recommender import ContentBasedRecommender
import os

recommender = ContentBasedRecommender()

class Tooltip:
    def __init__(self, widget, text, bg="#333333", fg="white"):
        self.widget = widget
        self.text = text
        self.bg = bg
        self.fg = fg
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # rimuove bordo e barra titolo
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background=self.bg, foreground=self.fg,
                         relief='solid', borderwidth=1,
                         font=("Helvetica", 10), wraplength=300)
        label.pack(ipadx=5, ipady=5)

    def hide_tip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

def on_select_poster():
    file_path = filedialog.askopenfilename(title="Seleziona il poster", filetypes=[("Image Files", "*.jpg *.png")])
    if file_path:
        display_info(file_path)

def display_info(path):
    for widget in inner_frame.winfo_children():
        widget.destroy()

    best_id, result = recommender.find_best_match(path)
    if result is None:
        ttk.Label(inner_frame, text="❌ Nessuna corrispondenza trovata.", font=("Helvetica", 14), foreground="#FFA500", background=bg_color).pack(pady=10)
        return

    inner_frame.configure(style="Custom.TFrame")

    # --- Film principale ---
    main_frame = ttk.Frame(inner_frame, style="Custom.TFrame")
    main_frame.pack(fill="x", pady=10)

    img = Image.open(path).resize((150, 220))
    photo = ImageTk.PhotoImage(img)
    img_label = ttk.Label(main_frame, image=photo, style="Custom.TLabel")
    img_label.image = photo
    img_label.grid(row=0, column=0, rowspan=6, padx=10)

    ttk.Label(main_frame, text=f"🎮 {result['title']}", font=("Helvetica", 22, "bold"), foreground="#FFD369", background=bg_color).grid(row=0, column=1, sticky="w")
    ttk.Label(main_frame, text=f"📅 Anno: {result['year']}   ⏱️ Durata: {result['duration']} min   ⭐ Rating: {result['rating']}",
              font=("Helvetica", 12), foreground="#CCCCCC", background=bg_color).grid(row=1, column=1, sticky="w", pady=2)
    ttk.Label(main_frame, text=f"🎭 Genere: {result['genres']}", font=("Helvetica", 12), foreground="#CCCCCC", background=bg_color).grid(row=2, column=1, sticky="w", pady=2)
    ttk.Label(main_frame, text=f"🏢 Studio: {result['studio']}", font=("Helvetica", 12), foreground="#CCCCCC", background=bg_color).grid(row=3, column=1, sticky="w", pady=2)
    main_actors = result['cast'].split(', ')[:5]
    ttk.Label(main_frame, text=f"👥 Cast principale: {', '.join(main_actors)}", font=("Helvetica", 12), foreground="#CCCCCC", background=bg_color).grid(row=4, column=1, sticky="w", pady=5)
    ttk.Label(main_frame, text="📖 Trama:", font=("Helvetica", 12, "italic"), foreground="#FFD369", background=bg_color).grid(row=5, column=1, sticky="nw", pady=(10,0))
    ttk.Label(main_frame, text=result['description'], wraplength=850, font=("Helvetica", 12), justify="left", foreground="#E0E0E0", background=bg_color).grid(row=6, column=0, columnspan=2, sticky="w", padx=10, pady=(0,15))

    # --- Film consigliati ---
    ttk.Label(inner_frame, text="🎞️ Film simili consigliati:", font=("Helvetica", 18, "bold"), foreground="#FFD369", background=bg_color).pack(anchor="w", padx=10, pady=(0,15))

    similar_movies = recommender.recommend(best_id, top_n=5)

    rec_frame = ttk.Frame(inner_frame, style="Custom.TFrame")
    rec_frame.pack(fill="x", padx=10)

    for idx, (_, sim_row) in enumerate(similar_movies.iterrows()):
        movie_frame = ttk.Frame(rec_frame, borderwidth=2, relief="ridge", style="Movie.TFrame", width=180)
        movie_frame.grid(row=0, column=idx, padx=10, sticky="n")
        movie_frame.grid_propagate(False)

        sim_path = sim_row['poster_path']
        if os.path.exists(sim_path):
            sim_img = Image.open(sim_path).resize((130, 180))
            sim_photo = ImageTk.PhotoImage(sim_img)
            sim_label = ttk.Label(movie_frame, image=sim_photo, style="Custom.TLabel")
            sim_label.image = sim_photo
            sim_label.pack(pady=5)

        ttk.Label(movie_frame, text=f"🎮 {sim_row['title']}", font=("Helvetica", 13, "bold"), wraplength=170, foreground="#FFD369", background="#2A2A40", justify="center").pack(pady=(5,0))
        ttk.Label(movie_frame, text=f"📅 {int(sim_row['year'])}", font=("Helvetica", 11), foreground="#CCCCCC", background="#2A2A40").pack()
        ttk.Label(movie_frame, text=f"🎭 {sim_row['genres']}", font=("Helvetica", 11), wraplength=170, justify="center", foreground="#CCCCCC", background="#2A2A40").pack()
        ttk.Label(movie_frame, text=f"⭐ {sim_row['rating']}", font=("Helvetica", 11), foreground="#FFD369", background="#2A2A40").pack(pady=(0,5))

        # Tooltip con la trama del film consigliato
        Tooltip(movie_frame, sim_row['description'], bg="#2A2A40", fg="white")

# --- GUI principale ---

root = tk.Tk()
root.title("🎥 Sistema di Raccomandazione Film")
root.geometry("1200x900")
bg_color = "#1A1A2E"  # blu notte scuro, più soft del nero puro
root.configure(bg=bg_color)

style = ttk.Style()
style.theme_use('clam')

style.configure("Custom.TFrame", background=bg_color)
style.configure("Custom.TLabel", background=bg_color)
style.configure("Movie.TFrame", background="#2A2A40", bordercolor="#FFD369")

style.configure("TButton",
                font=("Helvetica", 14),
                background="#333333",
                foreground="white")

style.map("TButton",
          background=[('active', '#555555')])

ttk.Button(root, text="Scegli un Poster 🎞️", command=on_select_poster).pack(pady=20)

inner_frame = ttk.Frame(root, style="Custom.TFrame")
inner_frame.pack(fill="both", expand=True, padx=20)

root.mainloop()
