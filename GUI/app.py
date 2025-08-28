import tkinter as tk
from .main_window import MainWindow

def main():
    root = tk.Tk()  # Create root window
    app = MainWindow(root)  # Initialize main application window
    root.mainloop()  # Start GUI event loop

if __name__ == "__main__":  # Run only if script executed directly
    main()
