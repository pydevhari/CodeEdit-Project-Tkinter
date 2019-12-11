from project_explorer import ProjectExplorer
from find_replace import Replace
from font import Font
import tkinter as tk


class Toolbar(Replace, ProjectExplorer, Font):
    """Provide a toolbar from on the top of the main window."""
    
    # Access all the icons from the image folder.
    new_file_icon = tk.PhotoImage(file='images/new_file_icon2.png')
    open_file_icon = tk.PhotoImage(file='images/open_file_icon2.png')
    save_icon = tk.PhotoImage(file='images/save_file_icon2.png')
    cut_icon = tk.PhotoImage(file='images/cut_icon.png')
    paste_icon = tk.PhotoImage(file='images/paste_icon.png')
    copy_icon = tk.PhotoImage(file='images/copy_icon.png')
    undo_icon = tk.PhotoImage(file='images/undo_icon.png')
    redo_icon = tk.PhotoImage(file='images/redo_icon.png')
    select_all_icon = tk.PhotoImage(file='images/select_all_icon.png')
    search_icon = tk.PhotoImage(file='images/search_icon.png')
    replace_icon = tk.PhotoImage(file='images/replace_icon2.png')
    font_decrease_icon = tk.PhotoImage(file='images/font_decrease.png')
    font_increase_icon = tk.PhotoImage(file='images/font_increase.png')

    def __init__(self):
        self.close_button = tk.Button(self.toolbar_frame, text='x', font=(None, 10), bd=0, fg='black',
                              command=self.show_hide_toolbar)
        self.close_button.pack(side='right', padx=5)

        self.new_file_button = tk.Button(self.toolbar_frame, image=self.new_file_icon,
                                 bd=0, command=self.add_tab)
        self.new_file_button.pack(side='left', padx=2, ipadx=3, ipady=0)

        self.open_file_button = tk.Button(self.toolbar_frame,
                                  image=self.open_file_icon, bd=0, command=self.open_file)
        self.open_file_button.pack(side='left', padx=2, ipadx=3, ipady=0)

        self.save_button = tk.Button(self.toolbar_frame,
                             image=self.save_icon, bd=0, command=self.save_file)
        self.save_button.pack(side='left', padx=2, ipadx=3, ipady=0)

        self.cut_button = tk.Button(self.toolbar_frame, image=self.cut_icon, bd=0, command=self.cut)
        self.cut_button.pack(side='left', padx=2, ipadx=3, ipady=0)

        self.paste_button = tk.Button(self.toolbar_frame,
                              image=self.paste_icon, bd=0, command=self.paste)
        self.paste_button.pack(side='left', padx=2, ipadx=3, ipady=0)

        self.copy_button = tk.Button(self.toolbar_frame, image=self.copy_icon, bd=0, command=self.copy)
        self.copy_button.pack(side='left', padx=2, ipadx=3, ipady=0)

        self.undo_button = tk.Button(self.toolbar_frame, image=self.undo_icon, bd=0, command=self.undo)
        self.undo_button.pack(side='left', padx=2, ipadx=3, ipady=0)

        self.redo_button = tk.Button(self.toolbar_frame, image=self.redo_icon, bd=0, command=self.redo)
        self.redo_button.pack(side='left', padx=2, ipadx=3, ipady=0)

        self.select_all_button = tk.Button(self.toolbar_frame,
                                   image=self.select_all_icon, bd=0, command=self.select_all)
        self.select_all_button.pack(side='left', padx=2, ipadx=3, ipady=0)

        self.search_button = tk.Button(self.toolbar_frame,
                               image=self.search_icon, bd=0, command=self.find)
        self.search_button.pack(side='left', padx=2, ipadx=3, ipady=0)

        self.replace_button = tk.Button(self.toolbar_frame,
                                image=self.replace_icon, bd=0, command=self.replace)
        self.replace_button.pack(side='left', padx=2, ipadx=3, ipady=0)

        self.font_decrease_button = tk.Button(self.toolbar_frame,
                                      image=self.font_decrease_icon, bd=0, command=self.decrease_font)
        self.font_decrease_button.pack(side='left', padx=2, ipadx=3, ipady=0)

        self.font_increase_button = tk.Button(self.toolbar_frame,
                                      image=self.font_increase_icon, bd=0, command=self.increase_font)
        self.font_increase_button.pack(side='left', padx=2, ipadx=3, ipady=0)

        # list of all toolbar button's for disable when all tabs are closed
        self.button_list = [self.save_button, self.cut_button, self.paste_button,
                            self.copy_button, self.undo_button, self.redo_button, self.select_all_button,
                            self.search_button, self.replace_button, self.font_decrease_button,
                            self.font_increase_button
                            ]

toolbar_obj = Toolbar()
