from project_explorer import ProjectExplorer
from find_replace import Replace
from font import Font
from toolbar_top_frame import Toolbar  # for enable toolbar frame
from parallel_scroll import yview


class EventsAndKeyBindings(ProjectExplorer, Replace, Font):
    """Bind all shortcut keys and other events"""
    def __init__(self):
        self.main_window.bind('<KeyRelease>', self.keypress_func)
        self.main_window.bind('<KeyPress>', self.keypress_func)
        self.main_window.bind('<Configure>', self.get_cursor_pos)
        self.text_area.bind('<Button-3>', self.txt_area_popup_menu)
        self.main_window.bind('<Configure>', self.line_counter)
        self.main_window.bind('<Control - f>', self.find)
        self.main_window.bind('<Control - F>', self.find)
        self.main_window.bind('<Control - r>', self.replace)
        self.main_window.bind('<Control - R>', self.replace)
        self.main_window.bind('<Control-d>', self.change_theme)

        self.text_area.bind("<<Change>>", self.line_counter)

        self.main_window.bind('<Control - =>', self.increase_font)
        self.main_window.bind('<Control - +>', self.increase_font)
        self.main_window.bind('<Control - minus>', self.decrease_font)
        self.main_window.bind("<Control-Shift-r>", self.font_reset)

        self.text_area.bind("<ButtonRelease>", self.get_cursor_pos)
        self.text_area.bind("<Control-Shift-R>", self.font_reset)
        self.text_area.bind("<<Modified>>", self.modified_flag)
        self.main_window.bind('<Control-s>', self.save_file)
        self.main_window.bind('<Control-S>', self.save_file)
        self.main_window.bind('<Control-o>', self.open_project)
        self.main_window.bind('<Control-O>', self.open_project)
        self.main_window.bind('<Control-g>', self.go_to_line)
        self.main_window.bind('<Control-G>', self.go_to_line)
        # self.open_directory()
        # self.create_project()
        self.text_area.bind('<Control-a>', self.select_all)
        self.text_area.bind('<Control-A>', self.select_all)
        self.main_window.protocol('WM_DELETE_WINDOW', self.on_main_win_close)

        self.main_window.bind("<Control-n>", self.add_tab)
        self.main_window.bind("<Control-N>", self.add_tab)
        self.text_area.bind("<Control-v>", self.paste2)
        self.text_area.bind("<Control-V>", self.paste2)

        self.nb.bind('<<NotebookTabChanged>>', self.get_mini_map_text)

        self.nb.bind('<ButtonRelease-1>', self.on_tab_close)

        # Auto bracketing
        self.main_window.bind('<(>', self.auto_complete)
        self.main_window.bind('<{>', self.auto_complete)
        self.main_window.bind('<[>', self.auto_complete)
        self.main_window.bind('<">', self.auto_complete)
        self.main_window.bind("<'>", self.auto_complete)

        self.tree.bind('<Double-1>', self.get_selected_file_path)
        self.tree.bind('<Button-3>', self.tree_right_click)
        self.tree.bind('<<TreeviewOpen>>', self.open_node)

        text = self.text_area
        text._orig = text._w + "_orig"
        text.tk.call("rename", text._w, text._orig)
        text.tk.createcommand(text._w, self.proxy)
        self.text_area.bind("<<Selection>>", self.count_selected_chars)


