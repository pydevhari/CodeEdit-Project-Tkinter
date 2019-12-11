from custom_notebook import CustomNotebook
import tkinter.font as tkFont
from tkinter import ttk
from tkinter import *


class Variables:
    """Container for all required variables which will use across multiple classes."""
    main_window = Tk()
    paned_win = PanedWindow(main_window, relief='flat', borderwidth=0, bd=0, sashrelief='sunken')
    left_frame = Frame(paned_win, bd=0, borderwidth=0, highlightthickness=0)
    right_frame = Frame(paned_win, bd=0, borderwidth=0, highlightthickness=0)
    # Add logo of project at here on canvas

    paned_win.add(left_frame, width=200)
    paned_win.add(right_frame)
    # For removing the border from treeview
    style = ttk.Style()
    style.layout("Treeview", [('Treeview.treearea', {'border': 0})])
    style.configure("CustomNotebook.Tab", background='red', foreground='red')


    tree = ttk.Treeview(left_frame)
    ysb = ttk.Scrollbar(left_frame, orient='vertical', command=tree.yview)
    xsb = ttk.Scrollbar(left_frame, orient='horizontal', command=tree.xview)
    tree.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
    tree.heading('#0', text='Open Project', anchor='w')
    tree.column('#0', minwidth=300, width=300, stretch=True)
    ysb.pack(side='right', fill='y')
    xsb.pack(side='bottom', fill='x')
    tree.pack(fill='both', expand=1)


    # -------------------------------------------------
    main_frame = Frame(right_frame, width=0, highlightthickness=0,
                       borderwidth=0, bd=0, relief='flat', pady=0)
    line_num_frame = Frame(main_frame, width=0)
    toolbar_frame = Frame(main_window, height=0)
    working_area = Frame(main_frame, width=0)
    code_minimap_frame = Frame(main_frame)
    line_num_frame.pack(fill='y', side='left')
    working_area.pack(fill='both', side='left', expand=True)
    code_minimap_frame.pack(fill='both', side='left', pady=(22, 0))
    main_frame.pack(fill='both', expand=1)
    # --------------------------------------------------------

    on_off_project_hierarchy = Frame(main_window, highlightbackground='gray', highlightthickness=0)
    # on_off_project_hierarchy.pack(fill)
    statusbar_frame = Frame(main_window, bg='gray', height=0)


    # ------------------Code Minimap Configuration-------------------
    mini_map_text = Text(code_minimap_frame, width=70, state='disabled',
                         cursor='arrow', font=("Consolas", 2), wrap="none", bd=0)
    y_scrollbar = ttk.Scrollbar(code_minimap_frame, orient="vertical")
    mini_map_text.config(yscrollcommand=y_scrollbar.set)
    y_scrollbar.pack(side='right', fill='y')
    mini_map_text.pack(fill='y', expand=1)
    mini_map_text.bindtags((str(mini_map_text), str(code_minimap_frame), "all"))
    # -----------------------------End-------------------------------

    project_lbl = Label(on_off_project_hierarchy)

    # widgets of the Application

    cursor_pos_lbl = Label(statusbar_frame, bg='gray', fg='black', text='Ln: 1, Col: 1')
    cursor_pos_lbl.pack(fill='x', side='right', padx=(0, 155))

    file_type_lbl = Label(statusbar_frame, bg='gray', fg='black', text='Plain Text')
    file_type_lbl.pack(fill='x', side='right', padx=(0, 100))



    # New Skeleton

    # nb = ttk.Notebook(working_area, width=0)
    nb = CustomNotebook(working_area, style="TNotebook.Tab")
    nb.pack(fill='both', expand=True)
    canvas = Canvas(line_num_frame, bd=0, highlightthickness=0)
    pady = 1
    canvas.pack(fill='both', side='left', pady=2)

    font_style = "Consolas"
    font_size = 12
    customFont = tkFont.Font(family=font_style, size=font_size)

    # Tab
    tab1 = Frame(nb)
    tab_width = customFont.measure('    ')
    # tab_width2 = customFont.measure(' ')
    mini_map_text.config(tabs=tab_width)

    text = Text(tab1, font=customFont, wrap='none', width=0,
                undo=True, padx=2, tabs=tab_width, relief='flat')

    # Vertical Scrollbar on text area
    y_scrollbar2 = ttk.Scrollbar(tab1, orient='vertical')
    text.config(yscrollcommand=y_scrollbar2.set)
    y_scrollbar2.config(command=text.yview)
    y_scrollbar2.pack(side='right', fill='y')

    # Horizontal Scrollbar on text area
    x_scrollbar = ttk.Scrollbar(tab1, orient='horizontal')
    text.config(xscrollcommand=x_scrollbar.set)
    x_scrollbar.config(command=text.xview)
    x_scrollbar.pack(side='bottom', fill='x')


    text.pack(fill='both', expand=1)
    text.modified = 0
    nb.add(tab1, text='Untitled')
    # Rename the tab
    # nb.tab(tab1, text='hello')
    text.focus_force()

    # Menu bar configuration
    main_menu = Menu(main_window, background='#212121', foreground='white')
    main_window.config(menu=main_menu)
    File = Menu(main_menu, tearoff=0, bd=0, borderwidth=0)
    Edit = Menu(main_menu, tearoff=0)
    Toolbars = Menu(main_menu, tearoff=0)
    Format = Menu(main_menu, tearoff=0)
    View = Menu(main_menu, tearoff=0)
    Help = Menu(main_menu, tearoff=0)
    # text.peer_create()

    # Right click popup menu
    popup_menu = Menu(working_area, tearoff=0)

    # Right click menu for treeview's file and folder
    popup_for_file = Menu(tree, tearoff=0)
    popup_for_folder = Menu(tree, tearoff=0)

    # a list which contains the status of all tabs
    file_list = [None]
