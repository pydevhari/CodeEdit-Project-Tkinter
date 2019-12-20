from all_events_keybindings import *
from toolbar_top_frame import Toolbar
from variables import *


class Main(ProjectExplorer):
    """
    This class is the main application class of the whole application.
    """

    def app(self):
        """Packing all the frames to the application"""
        self.main_window.title('CodeEdit')
        self.main_window.geometry("1100x510")

        self.statusbar_frame.pack(fill='x', side='bottom')
        self.toolbar_frame.pack(fill='x', side='top')

        self.on_off_project_hierarchy.pack(fill='y', side='left', ipadx=3)
        # self.main_frame.pack(fill='both', expand=1)

        self.paned_win.pack(fill='both', expand=1)
        f_icon = PhotoImage(file='images/folder2.png')
        self.project_lbl.config(image=f_icon,
                                compound='bottom', text='P\nr\no\nj\ne\nc\nt', bd=0)
        self.project_lbl.bind('<Button-1>', self.show_hide_project_hierarchy)
        self.project_lbl.pack()

        # -----------------
        # Menus
        # -----------------
        # File Menu
        self.main_menu.add_cascade(label=" File", menu=self.File)
        self.File.add_command(label="       New         Ctrl+N       ")
        self.File.add_command(label="       New Window        Ctrl+w       ")
        self.File.add_command(label="       Open Project        Ctrl+O       ", command=self.open_project)
        self.File.add_command(label="       Create Project        Ctrl+O       ", command=self.create_project)
        self.File.add_command(label="       Open File               ", command=self.open_file)
        self.File.add_separator()
        self.File.add_command(label="       Save        Ctrl+S       ", command=self.save_file)
        self.File.add_command(label="       Save as       ", command=self.save_as_file)
        self.File.add_separator()
        self.File.add_command(label="       Exit       ", command=exit)

        # # Edit Menu
        self.main_menu.add_cascade(label="  Edit", menu=self.Edit)
        self.Edit.add_command(label="       Cut              Ctrl+X        ")
        self.Edit.add_command(label="       Copy           Ctrl+C        ")
        self.Edit.add_command(label="       Paste           Ctrl+V        ")
        self.Edit.add_separator()
        self.Edit.add_command(label="       Undo           Ctrl+Z        ")
        self.Edit.add_command(label="       Redo           Ctrl+Y        ")
        self.Edit.add_command(label="       Find..          Ctrl+F        ")
        self.Edit.add_command(label="       Replace..     Ctrl+R        ")
        self.Edit.add_command(label="       Select All    Ctrl+A        ")
        self.Edit.add_separator()
        self.Edit.add_command(label="       Go To..        Ctrl+G        ")

        # Toolbar Menu
        self.main_menu.add_cascade(label=" Toolbar", menu=self.Toolbars)
        self.Toolbars.add_command(label="       Hide toolbar                ", command=self.show_hide_toolbar)

        # Format Menu
        self.main_menu.add_cascade(label="  Format", menu=self.Format)
        self.Format.add_command(label="       Font..       ")
        self.Format.add_command(label="       Font color       ")
        self.Format.add_command(label="       Set dark theme       ")
        self.Format.add_command(label="       Set default theme       ")
        # wrap1 = IntVar()
        # wrap1.set(0)
        self.Format.add_checkbutton(label="       Word Wrap       ", onvalue=1, offvalue=0)
        self.Format.add_separator()
        self.Format.add_command(label="       Date/Time       ")

        # View Menu
        self.zoom_menu = Menu(tearoff=0)
        self.zoom_menu.add_command(label="     Zoom In               Control+Plus")
        self.zoom_menu.add_command(label="     Zoom Out            Control+Minus")

        self.zoom_menu.add_command(label="     Zoom Reset         Control+Shift+R")
        self.main_menu.add_cascade(label="  View", menu=self.View)
        self.View.add_cascade(label="  Zoom   ", menu=self.zoom_menu)

        self.View.add_checkbutton(label="       Status Bar       ", onvalue=1, offvalue=0)

        # Help Menu
        self.main_menu.add_cascade(label="  Help", menu=self.Help)
        self.Help.add_command(label="       About       ")

        # Right click Menu for when user right click on inside the text area
        self.popup_menu.add_command(label='Undo               ', state='disabled', command=self.undo)
        self.popup_menu.add_command(label='Redo               ', state='disabled', command=self.redo)
        self.popup_menu.add_command(label='Cut                ', command=self.cut)
        self.popup_menu.add_command(label='Copy               ', command=self.copy)
        self.popup_menu.add_command(label='Paste              ', command=self.paste)
        self.popup_menu.add_command(label='Select All         ', command=self.select_all)

        # It will display when user right click on file on treeview
        self.popup_for_file.add_command(label='Rename File              ', command=self.rename_file_folder)
        self.popup_for_file.add_command(label='Delete              ', command=self.delete_file_folder)

        # It will display when user right click on folder on treeview
        self.popup_for_folder.add_command(label='New File              ', command=self.new_file)
        self.popup_for_folder.add_command(label='New Folder              ', command=self.new_folder)
        self.popup_for_folder.add_command(label='Rename Folder              ', command=self.rename_file_folder)
        self.popup_for_folder.add_command(label='Delete                ', command=self.delete_file_folder)

        self.main_window.mainloop()


if __name__ == '__main__':
    a = Main()
    a.app()
