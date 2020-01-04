import tkinter.ttk as ttk
import tkinter as tkinter
class CustomeScrollbar:
    def __init__(self):
        win = tk.Tk()
        style = ttk.Style()
        # style.theme_use('clam')
        style.element_create("Custom.Vertical.Scrollbar", "from", "clam")
        style.layout("Custom.Vertical.TScrollbar",
                     [('Vertical.Scrollbar.trough', {'sticky': 'ns', 'children':
                         [('Vertical.Scrollbar.thumb', {'sticky': 'nswe', 'unit': '1',
                        'children': [
                        ('Vertical.Scrollbar.grip', {'sticky': ''})]})]})])
        style.configure("Vertical.TScrollbar", gripcount=0, background="red", bordercolor="white",
                        lightcolor="gray", troughcolor="white", darkcolor="gray", arrowsize=12)

        # style.element_create("Custom.Horizontal.Scrollbar", "from", "default")
        style.layout("Custom.Horizontal.TScrollbar",
                     [('Horizontal.Scrollbar.trough', {'sticky': 'ns', 'children':
                         [('Horizontal.Scrollbar.thumb', {'sticky': 'nswe', 'unit': '1',
                                                          'children': [
                                                              ('Horizontal.Scrollbar.grip', {'sticky': ''})]})]})])
        style.configure("Horizontal.TScrollbar", gripcount=0, background="red", bordercolor="white",
                        lightcolor="gray", troughcolor="white", darkcolor="gray", arrowsize=12)

import tkinter as tk

class Example(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        self.menubar = tk.Menu()
        self.test1Menu = tk.Menu()
        self.test2Menu = tk.Menu()
        self.menubar.add_cascade(label="Test1", menu=self.test1Menu)
        self.menubar.add_cascade(label="Test2", menu=self.test2Menu)

        self.test1Menu.add_command(label="Enable Test2", command=self.enable_menu)
        self.test1Menu.add_command(label="Disable Test2", command=self.disable_menu)
        self.test2Menu.add_command(label="One")
        self.test2Menu.add_command(label="Two")
        self.test2Menu.add_command(label="Three")
        self.test2Menu.add_separator()
        self.test2Menu.add_command(label="Four")
        self.test2Menu.add_command(label="Five")

        root.configure(menu=self.menubar)

    def enable_menu(self):
        self.menubar.entryconfig("Test2", state="normal")

    def disable_menu(self):
        self.menubar.entryconfig("Test2", state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    app = Example(root)
    app.pack(fill="both", expand=True)
    root.mainloop()