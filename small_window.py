import tkinter as tk
from tkinter import ttk
class SmallWindow:
    """Class for create small windows of same structure like rename, create file or folder"""
    def create_win(self, title, btn_text, callback):
        """Initialize all the window's widgets and attach to window"""
        self.win = tk.Toplevel()
        self.center_small_window(self.win)
        self.win.resizable(0, 0)
        self.win.grab_set()
        self.win.title(title)
        self.win.geometry('300x100')
        self.entry = ttk.Entry(self.win, font=('Consolas', 12))
        self.entry.focus_force()
        self.entry.pack(fill='x', pady=(10, 0), padx=5)
        self.win.bind('<Return>', callback)
        self.btn = ttk.Button(self.win, text=btn_text, width=23, command=callback)
        self.btn.pack(pady=(20, 0), ipady=2, side='left', expand=True, padx=5)
        self.btn2 = ttk.Button(self.win, text='Cancel', command=self.win.destroy, width=23)
        self.btn2.pack(pady=(20, 0), ipady=2, side='left', expand=True, padx=5)
        self.btn2.bind('<Return>', self.win.destroy)
        # self.win.mainloop()

    def center_small_window(self, win):
        """Display small windows in the central area of main window"""
        w = 600
        h = 200
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        win.geometry(f"{w}x{h}+{int(x)}+{int(y)}")  # set the window in center of the screen
