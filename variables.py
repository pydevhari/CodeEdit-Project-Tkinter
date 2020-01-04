from custom_notebook import CustomNotebook
import tkinter.font as tkFont
from tkinter import ttk
import tkinter as tk


class Variables:
    """Container for all required variables which will use across multiple classes."""
    main_window = tk.Tk()
    paned_win = tk.PanedWindow(main_window, relief='flat', borderwidth=0, bd=0, sashrelief='sunken',
                            opaqueresize=False, orient='horizontal', sashpad=2, sashwidth=3)
    left_frame = tk.Frame(paned_win, bd=0, borderwidth=0, highlightthickness=0)
    right_frame = tk.Frame(paned_win, bd=0, borderwidth=0, highlightthickness=0)
    # Add logo of project at here on canvas

    paned_win.add(left_frame, width=200)
    paned_win.add(right_frame)
    # For removing the border from treeview
    style = ttk.Style()
    style.layout("Treeview", [('Treeview.treearea', {'border': 0})])
    # style.configure("CustomNotebook.Tab", background='red', foreground='red')

    tree = ttk.Treeview(left_frame, style='Treeview')
    ysb = tk.Scrollbar(left_frame, orient='vertical', command=tree.yview, width=12)
    xsb = tk.Scrollbar(left_frame, orient='horizontal', command=tree.xview, width=12)
    tree.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
    tree.heading('#0', text='Open Project', anchor='w')
    tree.column('#0', minwidth=300, width=300, stretch=True)
    ysb.pack(side='right', fill='y')
    xsb.pack(side='bottom', fill='x')
    tree.pack(fill='both', expand=1)

    # -------------------------------------------------
    main_frame = tk.Frame(right_frame, width=0, highlightthickness=0,
                       borderwidth=0, bd=0, relief='flat', pady=0)
    # sc = Scrollbar(right_frame
    line_num_frame = tk.Frame(main_frame, width=0)
    toolbar_frame = tk.Frame(main_window, height=0)
    working_area = tk.Frame(main_frame, width=0)
    code_minimap_frame = tk.Frame(main_frame)
    line_num_frame.pack(fill='y', side='left')
    working_area.pack(fill='both', side='left', expand=True)
    # code_minimap_frame.pack(fill='both', side='left', pady=(22, 0))
    main_frame.pack(fill='both', expand=1)
    # --------------------------------------------------------

    on_off_project_hierarchy = tk.Frame(main_window, highlightbackground='gray', highlightthickness=0)
    # on_off_project_hierarchy.pack(fill)
    statusbar_frame = tk.Frame(main_window, height=0)


    #--------------------- ------Default font configuration --------------------------
    font_style = "Consolas"
    font_size = 12
    font_weight = 'normal'
    # Global font objects
    customFont = tkFont.Font(family=font_style, size=font_size, weight=font_weight)
    lineFont = tkFont.Font(family='Consolas', size=font_size)
    # ----------------------------------------------------------------------------------


    # ------------------Code Minimap Configuration-------------------
    tab_width = customFont.measure(' ')
    mini_map_text = tk.Text(code_minimap_frame, width=70, state='disabled',
                         cursor='arrow', font=("Consolas", 2), wrap="none", bd=0, tabs=tab_width)
    y_scrollbar = ttk.Scrollbar(code_minimap_frame, orient="vertical")
    mini_map_text.config(yscrollcommand=y_scrollbar.set)
    y_scrollbar.pack(side='right', fill='y')
    mini_map_text.pack(fill='y', expand=1)
    mini_map_text.bindtags((str(mini_map_text), str(code_minimap_frame), "all"))
    # -----------------------------End-------------------------------

    project_lbl = tk.Label(on_off_project_hierarchy)

    # widgets of the Application

    cursor_pos_lbl = tk.Label(statusbar_frame, text='Ln: 1, Col: 1')
    cursor_pos_lbl.pack(fill='x', side='right', padx=(0, 180))

    selected_chars_lbl = tk.Label(statusbar_frame, text='--------------')
    selected_chars_lbl.pack(fill='x', side='right', padx=(0, 100))

    # New Skeleton

    # nb = ttk.Notebook(working_area, width=0)
    nb = CustomNotebook(working_area, style="TNotebook.Tab")
    nb.pack(fill='both', expand=True)
    canvas = tk.Canvas(line_num_frame, bd=0, highlightthickness=0)
    pady = 1
    canvas.pack(fill='both', side='left', pady=2)



    # Tab
    tab1 = tk.Frame(nb)
    tab_width = customFont.measure('    ')

    text_area = tk.Text(tab1, font=customFont, wrap='none', width=0,
                     undo=True, padx=2, tabs=tab_width, relief='flat')

    # Vertical Scrollbar on text area
    y_scrollbar2 = ttk.Scrollbar(tab1, orient='vertical')
    text_area.config(yscrollcommand=y_scrollbar2.set)
    y_scrollbar2.config(command=text_area.yview)
    y_scrollbar2.pack(side='right', fill='y')

    # Horizontal Scrollbar on text area
    x_scrollbar = tk.Scrollbar(tab1, orient='horizontal', width=12)
    text_area.config(xscrollcommand=x_scrollbar.set)
    x_scrollbar.config(command=text_area.xview)
    x_scrollbar.pack(side='bottom', fill='x')

    text_area.pack(fill='both', expand=1)

    text_area.modified = 0
    nb.add(tab1, text='Untitled')
    # Rename the tab
    # nb.tab(tab1, text='hello')
    text_area.focus_force()

    # tk.Menu bar configuration
    main_menu = tk.Menu(main_window)
    main_window.config(menu=main_menu)
    File = tk.Menu(main_menu, tearoff=0, bd=0, borderwidth=0)
    Edit = tk.Menu(main_menu, tearoff=0)
    Toolbars = tk.Menu(main_menu, tearoff=0)
    Format = tk.Menu(main_menu, tearoff=0)
    View = tk.Menu(main_menu, tearoff=0)
    Help = tk.Menu(main_menu, tearoff=0)
    # text.peer_create()

    wrap = tk.IntVar()
    wrap.set(0)



    msg = tk.Label(right_frame, text='Ctrl+N: New Tab', font=('Arial Rounded MT', 15, 'normal'))
    logo_img = tk.PhotoImage(file='images/desc_logo.png')
    logo_canvas = tk.Label(right_frame, image=logo_img)

    # Right click popup menu
    popup_menu = tk.Menu(working_area, tearoff=0)

    # Right click menu for treeview's file and folder
    popup_for_file = tk.Menu(tree, tearoff=0)
    popup_for_folder = tk.Menu(tree, tearoff=0)

    # list which contains the status of all tabs means which file is opened or not
    file_list = [None]

    # highlight = None
