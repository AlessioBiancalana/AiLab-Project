import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from Scripts.recommender import ContentBasedRecommender
from .tooltip import Tooltip
import os

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.bg_color = "#1A1A2E"
        self.recommender = ContentBasedRecommender()

        self.root.title("🎥 Movie Recommendation System")
        self.root.geometry("1200x900")
        self.root.configure(bg=self.bg_color)

        self.setup_style()
        ttk.Button(self.root, text="Choose a Poster 🎞️", command=self.on_select_poster).pack(pady=20)

        self.inner_frame = ttk.Frame(self.root, style="Custom.TFrame")
        self.inner_frame.pack(fill="both", expand=True, padx=20)

    def setup_style(self):
        # Custom style for GUI appearance
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.TFrame", background=self.bg_color)
        style.configure("Custom.TLabel", background=self.bg_color)
        style.configure("TButton", font=("Helvetica", 14),
                        background="#333333", foreground="white")
        style.map("TButton", background=[('active', '#555555')])

    def on_select_poster(self):
        # Let user select an image file
        file_path = filedialog.askopenfilename(title="Select Poster", filetypes=[("Image Files", "*.jpg *.png")])
        if file_path:
            self.display_info(file_path)

    def display_info(self, path):
        # Clear previous results
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        # Get best matching movie for selected poster
        best_id, result = self.recommender.find_best_match(path)
        if result is None:
            ttk.Label(self.inner_frame, text="❌ No match found.", font=("Helvetica", 14),
                      foreground="#FFA500", background=self.bg_color).pack(pady=10)
            return

        # Main result section
        main_frame = ttk.Frame(self.inner_frame, style="Custom.TFrame")
        main_frame.pack(fill="x", pady=10)

        # Load and display selected poster
        img = Image.open(path).resize((200, 300))
        photo = ImageTk.PhotoImage(img)
        img_label = ttk.Label(main_frame, image=photo, style="Custom.TLabel")
        img_label.image = photo
        img_label.grid(row=0, column=0, rowspan=6, padx=10)

        # Display movie info
        ttk.Label(main_frame, text=f"🎮 {result['title']}", font=("Helvetica", 26, "bold"),
                  foreground="#FFD369", background=self.bg_color).grid(row=0, column=1, sticky="w")
        ttk.Label(main_frame, text=f"📅 Year: {int(result['year'])}   ⏱️ Duration: {int(result['duration'])} min   ⭐ Rating: {result['rating']}",
                  font=("Helvetica", 12), foreground="#CCCCCC", background=self.bg_color).grid(row=1, column=1, sticky="w", pady=2)
        ttk.Label(main_frame, text=f"🎭 Genre: {result['genres']}", font=("Helvetica", 15),
                  foreground="#CCCCCC", background=self.bg_color).grid(row=2, column=1, sticky="w", pady=2)
        ttk.Label(main_frame, text=f"🎬 Director: {result['director']}", font=("Helvetica", 15),
          foreground="#CCCCCC", background=self.bg_color).grid(row=5, column=1, sticky="w", pady=2)
        ttk.Label(main_frame, text=f"🏢 Studio: {result['studio']}", font=("Helvetica", 15),
                  foreground="#CCCCCC", background=self.bg_color).grid(row=3, column=1, sticky="w", pady=2)
        main_actors = result['cast'].split(', ')[:5]
        ttk.Label(main_frame, text=f"👥 Main cast: {', '.join(main_actors)}", font=("Helvetica", 15),
                  foreground="#CCCCCC", background=self.bg_color).grid(row=4, column=1, sticky="w", pady=5)

        # Plot description
        desc_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        desc_frame.grid(row=6, column=1, sticky="w", pady=(10,15))
        ttk.Label(desc_frame, text="📖 Plot:", font=("Helvetica", 18, "italic"),
                  foreground="#FFD369", background=self.bg_color).pack(side="left", anchor="n")
        ttk.Label(desc_frame, text=result['description'], wraplength=800,
                  font=("Helvetica", 15), justify="left", foreground="#CCCCCC", background=self.bg_color).pack(side="left", padx=(10,0))

        # Recommended section
        ttk.Label(self.inner_frame, text="🎞️ Recommended similar movies:", font=("Helvetica", 18, "bold"),
                  foreground="#FFD369", background=self.bg_color).pack(anchor="w", padx=10, pady=(0,15))

        similar_movies = self.recommender.recommend(best_id, top_n=5)
        rec_frame = ttk.Frame(self.inner_frame, style="Custom.TFrame")
        rec_frame.pack(fill="x", padx=10)

        # Loop through recommended movies
        for idx, (_, sim_row) in enumerate(similar_movies.iterrows()):
            movie_frame = tk.Frame(rec_frame, bg="#2A2A40", width=240, height=400, bd=2, relief="ridge")
            movie_frame.grid(row=0, column=idx, padx=10, pady=5)
            movie_frame.grid_propagate(False)

            container = tk.Frame(movie_frame, bg="#2A2A40")
            container.place(relx=0.5, rely=0.5, anchor="center")

            sim_path = sim_row['poster_path']
            if os.path.exists(sim_path):
                sim_img = Image.open(sim_path).resize((150, 220))
                sim_photo = ImageTk.PhotoImage(sim_img)
                sim_label = tk.Label(container, image=sim_photo, bg="#2A2A40")
                sim_label.image = sim_photo
                sim_label.pack(pady=(0, 5))

            # Info for each recommended movie
            tk.Label(container, text=f"🎮 {sim_row['title']}", font=("Helvetica", 12, "bold"),
                     fg="#FFD369", bg="#2A2A40", wraplength=200, justify="center").pack()
            tk.Label(container, text=f"📅 {int(sim_row['year'])}", font=("Helvetica", 11),
                     fg="#CCCCCC", bg="#2A2A40").pack()
            tk.Label(container, text=f"🎭 {sim_row['genres']}", font=("Helvetica", 11),
                     fg="#CCCCCC", bg="#2A2A40", wraplength=200, justify="center").pack()
            tk.Label(container, text=f"⭐ {sim_row['rating']}", font=("Helvetica", 11),
                     fg="#FFD369", bg="#2A2A40").pack(pady=(0,5))

            # Tooltip with movie description
            Tooltip(movie_frame, sim_row['description'], bg="#2A2A40", fg="white")
