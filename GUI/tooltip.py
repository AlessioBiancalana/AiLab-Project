import tkinter as tk

class Tooltip:
    def __init__(self, widget, text, bg="#333333", fg="white"):
        self.widget = widget  # Target widget
        self.text = text  # Tooltip text
        self.bg = bg  # Background color
        self.fg = fg  # Foreground (text) color
        self.tipwindow = None  # Tooltip window reference
        self._hover_widgets = set()  # Track widgets with hover binding

        self._bind_recursive(widget)  # Bind events to widget and children

    def _bind_recursive(self, widget):
        widget.bind("<Enter>", self._on_enter, add="+")  # Show on mouse enter
        widget.bind("<Leave>", self._on_leave, add="+")  # Hide on mouse leave
        self._hover_widgets.add(widget)  # Add to hover set

        for child in widget.winfo_children():  # Bind recursively to children
            self._bind_recursive(child)

    def _on_enter(self, event=None):
        if self.tipwindow is None:  # Show tooltip if not visible
            self.show_tip(event)

    def _on_leave(self, event=None):
        event.widget.after(100, self._check_leave)  # Delay check before hiding

    def _check_leave(self):
        x, y = self.widget.winfo_pointerxy()  # Mouse pointer position
        widget_under_mouse = self.widget.winfo_containing(x, y)  # Widget under cursor
        if widget_under_mouse not in self._hover_widgets:  # If outside
            self.hide_tip()  # Hide tooltip

    def show_tip(self, event=None):
        if not self.text:  # Do nothing if no text
            return

        x = self.widget.winfo_pointerx() + 10  # X position near cursor
        y = self.widget.winfo_pointery() + 10  # Y position near cursor

        self.tipwindow = tw = tk.Toplevel(self.widget)  # Create tooltip window
        tw.wm_overrideredirect(True)  # Remove window decorations
        tw.wm_geometry(f"+{x}+{y}")  # Position tooltip
        tw.configure(background=self.bg)  # Set background

        label = tk.Label(  # Tooltip label
            tw, text=self.text, justify='left',
            background=self.bg, foreground=self.fg,
            relief='solid', borderwidth=1,
            font=("Helvetica", 10), wraplength=300
        )
        label.pack(ipadx=5, ipady=5)  # Padding around text

    def hide_tip(self):
        if self.tipwindow:  # Destroy tooltip if it exists
            self.tipwindow.destroy()
            self.tipwindow = None
