import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk, ImageDraw
from Scripts.recommender import ContentBasedRecommender  # Recommender system
from .tooltip import Tooltip
import os

class MainWindow:
    def __init__(self, root):
        self.root = root  # Root window
        self.bg_color = "#1A1A2E"  # Background color
        self.recommender = ContentBasedRecommender()  # Initialize recommender
        
        # Root window config
        self.root.title(" Movie Recommendation System")  # Window title
        self.root.geometry("1200x900")  # Window size
        self.root.iconbitmap('./film.ico')  # Window icon
        self.root.resizable(True, True)  # Allow resize
        # self.root.state("zoomed")  # Optional maximize on Windows
        self.root.configure(bg=self.bg_color)  # Set background color
        
        self.setup_style()  # Configure styles
        
        # Container for pages
        self.container = tk.Frame(self.root, bg=self.bg_color)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Start page
        self.start_page = tk.Frame(self.container, bg=self.bg_color)
        self.start_page.grid(row=0, column=0, sticky="nsew")
        
        # Load background image
        self.original_bg_image = Image.open("Assets/background.jpg")
        
        # Resize background to screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        resized = self.original_bg_image.resize((screen_width, screen_height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized)
        
        # Background label
        self.bg_label = tk.Label(self.start_page, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Bind resize event
        self.start_page.bind("<Configure>", self.resize_background)
        
        # Setup modern center frame
        self.setup_modern_center_frame()
        
        # Result page
        self.result_page = ttk.Frame(self.container, style="Custom.TFrame")
        self.result_page.grid(row=0, column=0, sticky="nsew")
        self.result_page.grid_columnconfigure(0, weight=1)
        
        self.inner_frame = ttk.Frame(self.result_page, style="Custom.TFrame")
        self.inner_frame.pack(fill="both", expand=True)
        
        # Show start page first
        self.start_page.tkraise()

    def create_rounded_rectangle(self, width, height, radius, fill_color, border_color=None, border_width=0):
        # Create rounded rectangle image
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        if border_width > 0 and border_color:  # With border
            draw.rounded_rectangle([0, 0, width-1, height-1], radius=radius, fill=border_color)
            draw.rounded_rectangle([border_width, border_width, width-1-border_width, height-1-border_width], 
                                   radius=radius-border_width, fill=fill_color)
        else:  # Only fill
            draw.rounded_rectangle([0, 0, width-1, height-1], radius=radius, fill=fill_color)
        
        return ImageTk.PhotoImage(image)

    def setup_modern_center_frame(self):
        # Setup central rounded frame
        box_width = 550
        box_height = 370
        radius = 25
        
        # Shadow
        shadow_image = self.create_rounded_rectangle(box_width, box_height, radius + 5, None)
        self.shadow_label = tk.Label(self.start_page, image=shadow_image, bg=self.bg_color)
        self.shadow_label.image = shadow_image
        self.shadow_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Main box
        main_box_image = self.create_rounded_rectangle(box_width, box_height, radius, "#FFFFFF")
        self.center_frame_bg = tk.Label(self.start_page, image=main_box_image, bg=self.bg_color)
        self.center_frame_bg.image = main_box_image
        self.center_frame_bg.place(relx=0.5, rely=0.5, anchor="center")
        
        # Transparent frame
        self.center_frame = tk.Frame(self.start_page, bg="#FFFFFF", bd=0, relief="flat")
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center", width=box_width-20, height=box_height-20)
        
        self.setup_modern_styles()  # Apply styles
        
        # Inner container
        self.inner_frame_modern = tk.Frame(self.center_frame, bg="#FFFFFF", bd=0)
        self.inner_frame_modern.pack(expand=True, fill="both", padx=30, pady=30)
        
        # Title
        self.title_label = tk.Label(
            self.inner_frame_modern, 
            text="🎬 Movie Recommendation System",
            font=("Segoe UI", 20, "bold"),
            background="#FFFFFF",
            anchor="center"
        )
        self.title_label.pack(pady=(0, 25))
        
        # Subtitle container
        self.icon_subtitle_frame = tk.Frame(self.inner_frame_modern, bg="#FFFFFF", bd=0)
        self.icon_subtitle_frame.pack(pady=(0, 30))
        
        # Subtitle
        self.subtitle_label = tk.Label(
            self.icon_subtitle_frame,
            text="Upload a movie poster to discover\nvisually and contextually similar movies",
            font=("Segoe UI", 16, "normal"),
            foreground="#666666",
            background="#FFFFFF",
            justify="center"
        )
        self.subtitle_label.pack()
        
        # Select button
        self.select_button = ttk.Button(
            self.inner_frame_modern,
            text="📁 Choose a Poster",
            command=self.on_select_poster,
            style="Success.TButton",
            width=25
        )
        self.select_button.pack(pady=20, ipady=8)
        
        # Info label
        self.info_label = tk.Label(
            self.inner_frame_modern,
            text="Supported formats: JPG, PNG, BMP, GIF",
            font=("Segoe UI", 10),
            foreground="#999999",
            background="#FFFFFF"
        )
        self.info_label.pack(pady=(10, 0))

    def setup_modern_styles(self):
        style = ttk.Style()
        # Entry style
        style.configure("Modern.TEntry", fieldbackground="#F8F9FA", borderwidth=1, relief="solid")
        # Green button
        style.configure("Success.TButton", font=("Segoe UI", 12, "bold"),
                        background="#20C997", foreground="white", relief="flat")
        # Yellow button
        style.configure("Success2.TButton", font=("Segoe UI", 12, "bold"),
                        background="#ffd369", foreground="white", relief="flat")
        # Hover effects
        style.map("Success.TButton",
                  background=[('active', '#17A2B8'), ('pressed', '#138496'), ('!active', '#20C997')],
                  foreground=[('active', 'white'), ('pressed', 'white'), ('!active', 'white')],
                  relief=[('pressed', 'flat'), ('!pressed', 'flat')])

    def resize_background(self, event):
        # Resize background on window resize
        if event.widget == self.start_page:
            new_width = event.width
            new_height = event.height
            resized = self.original_bg_image.resize((new_width, new_height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized)
            self.bg_label.config(image=self.bg_photo)

    def setup_style(self):
        # General style config
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.TFrame", background=self.bg_color)
        style.configure("Custom.TLabel", background=self.bg_color)
        style.configure("TButton", font=("Helvetica", 14), background="#333333", foreground="white")
        style.map("TButton", background=[('active', '#555555')])

    def on_select_poster(self):
        # Handle poster selection
        file_path = filedialog.askopenfilename(
            title="Select a movie poster",
            filetypes=[
                ("Images", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            print(f"Selected poster: {file_path}")
            self.display_info(file_path)

    def display_info(self, path):
        # Show movie info page
        self.result_page.tkraise()
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        
        # Choose button at top
        ttk.Button(self.inner_frame, text="📁 Choose a Poster",
                   command=self.on_select_poster, width=25, style="Success2.TButton").pack(pady=10)
        
        best_id, result = self.recommender.find_best_match(path)
        if result is None:
            ttk.Label(self.inner_frame, text="❌ No match found.", font=("Helvetica", 14),
                      foreground="#FFA500", background=self.bg_color).pack(pady=10)
            return
        
        # Main info frame
        main_frame = ttk.Frame(self.inner_frame, style="Custom.TFrame")
        main_frame.pack(fill="x", pady=10, anchor="center")
        
        # Poster
        img = Image.open(path).resize((200, 300))
        photo = ImageTk.PhotoImage(img)
        img_label = ttk.Label(main_frame, image=photo, style="Custom.TLabel")
        img_label.image = photo
        img_label.grid(row=0, column=0, rowspan=6, padx=10)
        
        # Title
        ttk.Label(main_frame, text=f"🎥 {result['title']}", font=("Helvetica", 26, "bold"),
                  foreground="#FFD369", background=self.bg_color).grid(row=0, column=1, sticky="w")
        
        # Year, duration, rating
        ttk.Label(main_frame, text=f"📅 Year: {int(result['year'])}   ⏱️ Duration: {int(result['duration'])} min   ⭐ Rating: {result['rating']}",
                  font=("Helvetica", 12), foreground="#CCCCCC", background=self.bg_color).grid(row=1, column=1, sticky="w", pady=2)
        
        # Genre
        ttk.Label(main_frame, text=f"🎭 Genre: {result['genres']}", font=("Helvetica", 15),
                  foreground="#CCCCCC", background=self.bg_color).grid(row=2, column=1, sticky="w", pady=2)
        
        # Studio
        ttk.Label(main_frame, text=f"🏢 Studio: {result['studio']}", font=("Helvetica", 15),
                  foreground="#CCCCCC", background=self.bg_color).grid(row=3, column=1, sticky="w", pady=2)
        
        # Main cast
        main_actors = result['cast'].split(', ')[:5]
        ttk.Label(main_frame, text=f"👥 Main cast: {', '.join(main_actors)}", font=("Helvetica", 15),
                  foreground="#CCCCCC", background=self.bg_color).grid(row=4, column=1, sticky="w", pady=5)
        
        # Director
        ttk.Label(main_frame, text=f"🎬 Director: {result['director']}", font=("Helvetica", 15),
                  foreground="#CCCCCC", background=self.bg_color).grid(row=5, column=1, sticky="w", pady=2)
        
        # Description
        desc_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        desc_frame.grid(row=6, column=1, sticky="w", pady=(10, 15))
        
        ttk.Label(desc_frame, text="📖 Plot:", font=("Helvetica", 18, "italic"),
                  foreground="#FFD369", background=self.bg_color).pack(side="left", anchor="n")
        
        ttk.Label(desc_frame, text=result['description'], wraplength=1200,
                  font=("Helvetica", 13), justify="left", foreground="#CCCCCC", background=self.bg_color).pack(side="left", padx=(10, 0))
        
        # Recommendations
        ttk.Label(self.inner_frame, text="🎞️ Recommended similar movies:", font=("Helvetica", 18, "bold"),
                  foreground="#FFD369", background=self.bg_color).pack(anchor="w", padx=10, pady=(0, 15))
        
        similar_movies = self.recommender.recommend(best_id, top_n=5, alpha=0.6)
        
        rec_frame = ttk.Frame(self.inner_frame, style="Custom.TFrame")
        rec_frame.pack(padx=10, anchor="w")
        
        # Show recommended movies
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
            
            tk.Label(container, text=f"🎥 {sim_row['title']}", font=("Helvetica", 12, "bold"),
                     fg="#FFD369", bg="#2A2A40", wraplength=200, justify="center").pack()
            
            tk.Label(container, text=f"📅 {int(sim_row['year'])}", font=("Helvetica", 11),
                     fg="#CCCCCC", bg="#2A2A40").pack()
            
            tk.Label(container, text=f"🎭 {sim_row['genres']}", font=("Helvetica", 11),
                     fg="#CCCCCC", bg="#2A2A40", wraplength=200, justify="center").pack()
            
            tk.Label(container, text=f"⭐ {sim_row['rating']}", font=("Helvetica", 11),
                     fg="#FFD369", bg="#2A2A40").pack(pady=(0, 5))
            
            movie_data = sim_row.to_dict()
            def open_details(event, data=movie_data):
                self.show_movie_details(data)
            
            movie_frame.bind("<Button-1>", open_details)
            for child in container.winfo_children():
                child.bind("<Button-1>", open_details)

    def show_movie_details(self, movie):
        # Detailed info window
        detail_win = tk.Toplevel(self.root)
        detail_win.title(f"🎬 {movie['title']}")
        detail_win.geometry("720x850")
        detail_win.configure(bg=self.bg_color)
        
        # Poster
        if os.path.exists(movie['poster_path']):
            img = Image.open(movie['poster_path']).resize((180, 280))
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(detail_win, image=photo, bg=self.bg_color)
            img_label.image = photo
            img_label.pack(pady=10)
        
        # Title
        tk.Label(detail_win, text=f"🎥 {movie['title']}", font=("Helvetica", 22, "bold"),
                 fg="#FFD369", bg=self.bg_color, wraplength=600, justify="center").pack(pady=(10, 5))
        
        # Year, duration, rating
        tk.Label(detail_win,
                 text=f"📅 Year: {int(movie['year'])}   ⏱️ Duration: {int(movie['duration'])} min   ⭐ Rating: {movie['rating']}",
                 font=("Helvetica", 12), fg="#CCCCCC", bg=self.bg_color).pack()
        
        # Helper functions for labels
        def highlight_label(text):
            return tk.Label(detail_win, text=text, font=("Helvetica", 12, "bold"),
                            fg="#FFD369", bg=self.bg_color, anchor="center", justify="center")
        
        def normal_label(text):
            return tk.Label(detail_win, text=text, font=("Helvetica", 11),
                            fg="#CCCCCC", bg=self.bg_color, justify="center", wraplength=600)
        
        # Sections
        highlight_label("🎭 Genre:").pack(pady=(10, 2), fill="x", expand=True)
        normal_label(movie['genres']).pack(fill="x")
        
        highlight_label("🏢 Studio:").pack(pady=(10, 2), fill="x", expand=True)
        normal_label(movie['studio']).pack(fill="x")
        
        highlight_label("🎬 Director:").pack(pady=(10, 2), fill="x", expand=True)
        normal_label(movie['director']).pack(fill="x")
        
        main_actors = movie['cast'].split(', ')[:5]
        highlight_label("👥 Main cast:").pack(pady=(10, 2), fill="x", expand=True)
        normal_label(", ".join(main_actors)).pack(fill="x")
        
        highlight_label("📖 Plot:").pack(pady=(20, 5), fill="x", expand=True)
        normal_label(movie['description']).pack(fill="x", pady=(0, 10))
