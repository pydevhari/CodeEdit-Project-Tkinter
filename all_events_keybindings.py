# from variables import V
# from all_functions import Methods
from syntax_highlight import Highlighting
# from variables import Variables
from find_replace import Replace
from project_explorer import ProjectExplorer
from font import Font
from formatting import yview


class Events_and_Keys(Replace, Font, ProjectExplorer):

    def keypress_func2(self, event=None):
        self.get_mini_map_text()
        Highlighting().highlight()
        # Highlighting().highlight()

    new_y = 0
    old_y = 0
    def __init__(self):
        # self.main_window.bind('<KeyPress>', self.keypress_func)
        self.main_window.bind('<KeyRelease>', self.keypress_func2)
        self.main_window.bind('<KeyPress>', self.keypress_func)
        self.main_window.bind('<Configure>', self.get_cursor_pos)
        self.main_window.bind('<Control-w>', self.add_tab)
        self.text.bind('<Button-3>', self.popup)
        self.main_window.bind('<Configure>', self.line_counter)
        self.main_window.bind('<Control - f>', self.find)
        self.main_window.bind('<Control - r>', self.replace)
        self.main_window.bind('<Control-d>', self.change_theme)

        self.text.bind("<<Change>>", self.line_counter)

        self.main_window.bind('<Control - =>', self.increase_font)
        self.main_window.bind('<Control - +>', self.increase_font)
        self.main_window.bind('<Control - minus>', self.decrease_font)
        self.main_window.bind("<Control-Shift-r>", self.font_reset)

        self.text.bind("<ButtonRelease>", self.get_cursor_pos)
        self.text.bind("<Control-Shift-R>", self.font_reset)
        self.text.bind("<<Modified>>", self.modified_flag)
        self.main_window.bind('<Control-s>', self.save_file)
        self.main_window.bind('<Control-o>', self.open_project)
        # self.open_directory()
        # self.create_project()
        self.text.bind('<Control-a>', self.select_all)
        self.main_window.protocol('WM_DELETE_WINDOW', self.on_main_win_close)
        # self.main_window.bind('<Control-w>', self.show_hide_toolbar)

        self.main_window.bind("<Control-n>", self.add_tab)
        self.main_window.bind("<Control-N>", self.add_tab)
        def paste2(event):
            self.paste(func=Highlighting().highlight2)
            return "break"
        self.text.bind("<Control-v>", paste2)

        self.nb.bind('<<NotebookTabChanged>>', self.get_mini_map_text)

        self.nb.bind('<ButtonRelease-1>', self.on_tab_close)

        # Auto bracketing
        self.main_window.bind('<(>', self.auto_complete)
        self.main_window.bind('<{>', self.auto_complete)
        self.main_window.bind('<[>', self.auto_complete)
        self.main_window.bind('<">', self.auto_complete)
        self.main_window.bind("<'>", self.auto_complete)



        # self.tree.bind("<Button-1>", self.disableEvent)
        self.tree.bind('<Double-1>', self.get_selected_file_path)
        self.tree.bind('<Button-3>', self.tree_right_click)
        self.tree.bind('<<TreeviewOpen>>', self.open_node)

        # self.tree.bind('<Control-c>', self.copy_file)

        text = self.text
        text._orig = text._w + "_orig"
        text.tk.call("rename", text._w, text._orig)
        text.tk.createcommand(text._w, self.proxy)


        def call(event):
            self.mini_map_text.scan_dragto(0, int(-event.y/2))
            self.text.yview_moveto(self.y_scrollbar.get()[1])
            # self.text.scan_dragto(0, int(-event.y/2))
            self.old_y = self.new_y
            self.new_y = event.y
            if self.new_y < self.old_y:  #up
                self.mini_map_text.scan_dragto(0, int(-event.y / 2))
                self.text.yview_moveto(self.y_scrollbar.get()[0])
            else:  #down
                self.mini_map_text.scan_dragto(0, int(-event.y / 2))
                self.text.yview_moveto(self.y_scrollbar.get()[1])
                # print('down...')
            #     self.mini_map_text.yview("scroll", 5, "units")
            #     a, b = self.y_scrollbar.get()
            #     # self.text.yview("scroll", -10, "units")
            #     self.y_scrollbar2.set(a, b)
            #     self.text.yview_moveto(b)
                # self.text.yview("scroll", 10, "units")
            # print(self.new_y-self.old_y)
            # print(int(event.y / 5), event.y)
            # print()
            # print(int(event.y / 5), event.y)
            # self.text.yview("scroll", int(event.y / 20), "units")
            # # print('dragging..')
            # print(event)

        self.mini_map_text.bind('<B1-Motion>', call)
        def config(event):
            self.tree.update()
            self.y_scrollbar.update()
            self.mini_map_text.update()
        self.tree.bind('<Configure>', config)

keys = Events_and_Keys()

