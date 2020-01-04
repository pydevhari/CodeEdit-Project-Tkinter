from project_explorer import ProjectExplorer
from find_replace import Replace
from font import Font
import tkinter as tk
import tkinter.ttk as ttk


class Toolbar(Replace, ProjectExplorer, Font):
    """Provide a toolbar from on the top of the main window."""
    
    # Access all the icons from the image folder.
    new_file_icon = tk.PhotoImage(file='images/new_file_icon2.png')
    open_file_icon = tk.PhotoImage(file='images/open_file_icon2.png')
    new_pro_icon = tk.PhotoImage(file='images/new_project.png')
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
        self.close_btn = tk.Button(self.toolbar_frame, relief='flat', text='x', font=(None, 10),  fg='black',
                              command=self.show_hide_toolbar, bd=0)
        self.close_btn.pack(side='right', padx=5)

        self.new_tab_btn = ttk.Button(self.toolbar_frame, image=self.new_file_icon,
                                      command=self.add_tab)
        self.new_tab_btn.pack(side='left', padx=2, ipadx=1, ipady=0)

        self.new_pro_btn = ttk.Button(self.toolbar_frame, image=self.new_pro_icon,
                                     command=self.create_project)
        self.new_pro_btn.pack(side='left', padx=2, ipadx=1, ipady=0)

        self.open_file_btn = ttk.Button(self.toolbar_frame,
                                  image=self.open_file_icon,  command=self.open_file)
        self.open_file_btn.pack(side='left', padx=2, ipadx=1, ipady=0)

        self.save_btn = ttk.Button(self.toolbar_frame,
                             image=self.save_icon,  command=self.save_file)
        self.save_btn.pack(side='left', padx=2, ipadx=1, ipady=0)

        self.cut_btn = ttk.Button(self.toolbar_frame, image=self.cut_icon,  command=self.cut)
        self.cut_btn.pack(side='left', padx=2, ipadx=1, ipady=0)

        self.paste_btn = ttk.Button(self.toolbar_frame,
                              image=self.paste_icon,  command=self.paste)
        self.paste_btn.pack(side='left', padx=2, ipadx=1, ipady=0)

        self.copy_btn = ttk.Button(self.toolbar_frame, image=self.copy_icon,  command=self.copy)
        self.copy_btn.pack(side='left', padx=2, ipadx=1, ipady=0)

        self.undo_btn = ttk.Button(self.toolbar_frame, image=self.undo_icon,  command=self.undo)
        self.undo_btn.pack(side='left', padx=2, ipadx=1, ipady=0)

        self.redo_btn = ttk.Button(self.toolbar_frame, image=self.redo_icon,  command=self.redo)
        self.redo_btn.pack(side='left', padx=2, ipadx=1, ipady=0)

        # self.select_all_btn = tk.Button(self.toolbar_frame,
        #                            image=self.select_all_icon,  command=self.select_all, bd=0)
        # self.select_all_btn.pack(side='left', padx=2, ipadx=1, ipady=0)

        self.search_btn = ttk.Button(self.toolbar_frame,
                               image=self.search_icon,  command=self.find)
        self.search_btn.pack(side='left', padx=2, ipadx=1, ipady=0)

        self.replace_btn = ttk.Button(self.toolbar_frame,
                                image=self.replace_icon,  command=self.replace)
        self.replace_btn.pack(side='left', padx=2, ipadx=1, ipady=0)

        self.font_decrease_btn = ttk.Button(self.toolbar_frame,
                                      image=self.font_decrease_icon,  command=self.decrease_font)
        self.font_decrease_btn.pack(side='left', padx=2, ipadx=1, ipady=0)

        self.font_increase_btn = ttk.Button(self.toolbar_frame,
                                      image=self.font_increase_icon,  command=self.increase_font)
        self.font_increase_btn.pack(side='left', padx=2, ipadx=1, ipady=0)

        # list of all toolbar btn's for disable when all tabs are closed
        self.button_list = [self.save_btn, self.cut_btn, self.paste_btn,
                            self.copy_btn, self.undo_btn, self.redo_btn,
                            self.search_btn, self.replace_btn, self.font_decrease_btn,
                            self.font_increase_btn
                            ]

toolbar_obj = Toolbar()
