import tkinter as tk

class Tooltip:
    def __init__(self, widget, text, bg="#333333", fg="white"):
        self.widget = widget
        self.text = text
        self.bg = bg
        self.fg = fg
        self.tipwindow = None
        self._hover_widgets = set()

        # Bind a tutti i figli
        self._bind_recursive(widget)

    def _bind_recursive(self, widget):
        widget.bind("<Enter>", self._on_enter, add="+")
        widget.bind("<Leave>", self._on_leave, add="+")
        self._hover_widgets.add(widget)

        for child in widget.winfo_children():
            self._bind_recursive(child)

    def _on_enter(self, event=None):
        if self.tipwindow is None:
            self.show_tip(event)

    def _on_leave(self, event=None):
        # Usa after per evitare sfarfallii se il mouse passa velocemente tra figli
        event.widget.after(100, self._check_leave)

    def _check_leave(self):
        x, y = self.widget.winfo_pointerxy()
        widget_under_mouse = self.widget.winfo_containing(x, y)
        if widget_under_mouse not in self._hover_widgets:
            self.hide_tip()

    def show_tip(self, event=None):
        if not self.text:
            return

        x = self.widget.winfo_pointerx() + 10
        y = self.widget.winfo_pointery() + 10

        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.configure(background=self.bg)

        label = tk.Label(tw, text=self.text, justify='left',
                         background=self.bg, foreground=self.fg,
                         relief='solid', borderwidth=1,
                         font=("Helvetica", 10), wraplength=300)
        label.pack(ipadx=5, ipady=5)

    def hide_tip(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None
