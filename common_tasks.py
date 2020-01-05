from tkinter import filedialog as fd
from tkinter import messagebox as mb
from variables import Variables
import tkinter as tk
from tkinter import ttk
import datetime
import imghdr
import os


class CommonTask(Variables):
    """Contains common functionality for application"""

    def get_cursor_pos(self, event=None):
        """  """
        try:
            text_area = self.get_current()
        except:
            print('error at get_cursor_pos')
            return
        text_area.tag_remove("highlight", '1.0', "end")
        row, col = text_area.index('insert').split('.')  # Get current position of the cursor
        self.cursor_pos_lbl.config(text=f'Ln: {int(row)}, Col: {int(col) + 1}')

    def proxy(self, *args):
        """Update line numbers when any text edited or copy, cut, paste, or any other event occur."""
        text_area = self.get_current()
        cmd = (text_area._orig,) + args
        try:
            result = text_area.tk.call(cmd)
        except:
            return
        if (args[0] in ("insert", "replace", "delete") or
                args[0:3] == ("mark", "set", "insert") or
                args[0:2] == ("xview", "moveto") or
                args[0:2] == ("xview", "scroll") or
                args[0:2] == ("yview", "moveto") or
                args[0:2] == ("yview", "scroll")
        ):
            text_area.event_generate("<<Change>>", when="tail")
            # return what the actual widget returned
        return result

    def get_current(self, event=None):
        """Return the object of the current tab's text widget"""
        childes = self.nb.winfo_children()  # return the list objects of child widgets of notebook[tab widget]
        return childes[self.nb.index('current')].winfo_children()[0]

    def line_counter(self, event=None):
        """Count lines of the text area and draw counted lines on canvas."""
        try:
            text_area = self.get_current()
            self.canvas.delete('all')
            i = text_area.index("@0,0")
            while True:
                dline = text_area.dlineinfo(i)
                if dline is None: break
                y = dline[1]
                linenum = str(i).split(".")[0]
                self.canvas.create_text(10, y + 28, anchor="w", text=linenum,
                                        font=self.lineFont, width=0)
                text_length = self.canvas.bbox('all')  # returns a tuple in the form of (x1, y1, x2, y2)
                width = text_length[2] - text_length[0]  # x2-x1
                self.canvas.config(width=width + 15)
                i = text_area.index("%s+1line" % i)
                # print(self.cursor_pos.cget('pady'), self.statusbar_frame.cget('pady'), )
        except:
            self.canvas.delete('all')

    tab_counter = 0

    def paste2(self, event):
        """Parse the all text of file when paste event occur"""
        from syntax_highlight import Highlighting
        self.paste(func=Highlighting().highlight2)
        return "break"

    def add_tab(self, event=None, file=None, open_file=0):
        """Add a new tab to Notebook widget"""

        tab1 = tk.Frame(self.nb, width=0, bd=0, borderwidth=0, highlightthickness=0)
        tab_width = self.customFont.measure('    ')
        text_area = tk.Text(tab1, font=self.customFont, wrap='none', width=0, undo=True,
                            tabs=tab_width, padx=2, relief='flat')  # tabs=tab_width
        #     # Horizontal tk.Scrollbar on text area
        y = ttk.Scrollbar(tab1, orient='vertical', command=text_area.yview)
        text_area.config(yscrollcommand=y.set)
        # y_scrollbar.config(command=text.yview)
        y.pack(side='right', fill='y')

        x_scrollbar = tk.Scrollbar(tab1, orient='horizontal', width=12)
        text_area.config(xscrollcommand=x_scrollbar.set)
        x_scrollbar.config(command=text_area.xview)
        x_scrollbar.pack(side='bottom', fill='x')

        if file and open_file == 1:
            f = ''
            if file not in self.file_list:
                try:
                    filename = os.path.basename(file)
                    f = open(file)
                    text_area.insert("1.0", f.read())
                    self.nb.add(tab1, text=filename)
                    self.nb.select(tab1)   # for select current tab
                    self.file_list.append(file)
                    text_area.edit_modified(arg=False)
                    from syntax_highlight import Highlighting
                    Highlighting().highlight2()
                except:
                    tab1.destroy()
                    mb.showerror('Error', "Can't open uneditable file")
                    return
                finally:
                    f.close()
            else:
                tab1.destroy()
                self.nb.select(self.file_list.index(file))
                self.get_current().focus_force()
                return
        elif file and open_file is 0:
            f = ''
            try:
                filename = os.path.basename(file)
                f = open(file)
                text_area.insert("1.0", f.read())
                self.file_list.append(file)
                # f.close()
                self.nb.add(tab1, text=filename)
                self.nb.select(tab1)
                from syntax_highlight import Highlighting
                Highlighting().highlight2()
            except Exception as e:
                print(e)
            finally:
                f.close()
        else:
            self.tab_counter += 1
            self.file_list.append(None)
            self.nb.add(tab1, text=f'Untitled -{self.tab_counter}')
            self.nb.select(tab1)

        # -------------Key binding for text widget------------------
        # text.bind('<Control - =>', Font().increase_font)
        # text.bind('<Control - minus>', Font().decrease_font)
        # text.bind("<Control-Shift-r>", Font().font_reset)
        # text.bind("<Control-Shift-R>", Font().font_reset)
        text_area.bind("<ButtonRelease>", self.get_cursor_pos)
        text_area.bind('<Control-z>', self.undo)
        text_area.bind('<Control-Z>', self.undo)
        text_area.bind('<Control-y>', self.redo)
        text_area.bind('<Control-Y>', self.redo)
        text_area.bind('<Control-a>', self.select_all)
        text_area.bind('<Control-A>', self.select_all)
        text_area.bind('<Control-v>', self.paste2)
        text_area.bind('<Control-V>', self.paste2)
        text_area.bind("<<Change>>", self.line_counter)
        text_area.bind("<<Modified>>", self.modified_flag)
        # from syntax_highlight import Highlighting
        # text_area.bind("<<Paste>>", Highlighting().highlight2)
        text_area.bind('<Button-3>',
                       self.txt_area_popup_menu)  # For display right click popup menu inside the text area
        text_area.bind("<<Selection>>", self.count_selected_chars)
        text_area.modified = 0
        # ------------------------------------------------------------

        text_area._orig = text_area._w + "_orig"
        text_area.tk.call("rename", text_area._w, text_area._orig)
        text_area.tk.createcommand(text_area._w, self.proxy)
        text_area.pack(fill='both', expand=1)

        text_area.focus_force()
        text_area.edit('reset')
        text_area.edit_modified(arg=False)
        self.get_cursor_pos()
        print(self.file_list)

        if len(self.file_list) == 1:  # Repack the working area
            self.msg.pack_forget()
            self.logo_canvas.pack_forget()
            self.main_frame.pack(fill='both', side='left', expand=1)
            self.main_window.bind('<Configure>', self.line_counter)
            self.main_window.bind('<KeyPress>', self.keypress_func)
            self.main_window.bind('<KeyRelease>', self.keypress_func)
            self.nb.bind('<<NotebookTabChanged>>', self.get_mini_map_text)
            self.main_window.bind('<Control-S>', self.save_file)
            self.main_window.bind('<Control-s>', self.save_file)
            self.File.entryconfigure(5, state='normal')
            self.File.entryconfigure(6, state='normal')
            for item in range(11):
                try:
                    self.Edit.entryconfigure(item, state='normal')
                except:
                    pass
            # self.File.entryconfigure(7, state='normal')
            self.Format.entryconfigure(1, state='normal')
            self.Format.entryconfigure(3, state='normal')
            from toolbar_top_frame import toolbar_obj
            for button in toolbar_obj.button_list:
                button.config(state='normal')
        # self.change_theme()

    def get_mini_map_text(self, event=None):
        """Get the text from current tab and insert it into mini map text area"""
        try:
            text_area = self.get_current()
        except Exception as e:
            print('error at get_mini_map_text', e)
            return
        data = text_area.get('1.0', 'end')
        self.mini_map_text.config(state='normal')
        self.mini_map_text.delete('1.0', 'end')
        self.mini_map_text.insert('1.0', data)
        self.mini_map_text.config(state='disabled')
        # self.nb.update_idletasks()

    def rename_tab(self, file):
        """Rename the tabs's name's text when file is saved"""
        lst = self.nb.winfo_children()  # return the list objects of child widgets of notebook[tab widget]
        self.nb.tab(lst[self.nb.index('current')], text=file)

    showing = True  # Flag for that toolbar frame is showing or not [Default is showing]

    def show_hide_toolbar(self):
        """Show or hide the toolbar frame on top of the working area."""
        if self.showing:  # hiding
            self.toolbar_frame.pack_forget()
            self.Toolbars.entryconfigure(1, label="       Show toolbar                ", command=self.show_hide_toolbar)
            self.showing = False
        else:  # displaying
            self.paned_win.pack_forget()
            self.on_off_project_hierarchy.pack_forget()
            self.statusbar_frame.pack_forget()

            self.statusbar_frame.pack(fill='x', side='bottom')
            self.toolbar_frame.pack(fill='x', side='top')
            self.on_off_project_hierarchy.pack(fill='y', side='left', ipadx=3)
            self.paned_win.pack(fill='both', expand=1)

            self.Toolbars.entryconfigure(1, label="       Hide toolbar                ")
            self.showing = True

    def undo(self, event=None):
        """Perform undo operation"""
        textArea = self.get_current()
        textArea.event_generate('<<Undo>>')

    def redo(self, event=None):
        """Perform redo operation"""
        try:
            textArea = self.get_current()
            textArea.event_generate('<<Redo>>')
        except:
            pass

    def cut(self, event=None):
        """Perform cut operation"""
        textArea = self.get_current()
        textArea.event_generate('<<Cut>>')

    def copy(self, event=None):
        """Perform copy operation"""
        textArea = self.get_current()
        textArea.event_generate('<<Copy>>')

    def paste(self, func=None, event=None):
        """Perform paste operation"""
        textArea = self.get_current()
        textArea.event_generate('<<Paste>>')
        if func:
            func()
        self.count_selected_chars()
        textArea.see('insert')

    def select_all(self, event=None):
        """Select the all text of text area"""
        print('select all')
        textArea = self.get_current()

        textArea.tag_add("sel", "1.0", "end-1c")
        return "break"  # Deleting default Control + a select event

    def auto_complete(self, event):
        """Auto complete the brackets."""
        text = self.get_current()
        # print(event)
        if event.char == '(':
            text.insert('insert', ')')
            text.mark_set('insert', 'insert-1c')
        elif event.char == '{':
            text.insert('insert', '}')
            text.mark_set('insert', 'insert-1c')
        elif event.char == '[':
            text.insert('insert', ']')
            text.mark_set('insert', 'insert-1c')
        elif event.char == '"':
            text.insert('insert', '"')
            text.mark_set('insert', 'insert-1c')
        elif event.char == "'":
            text.insert('insert', "'")
            text.mark_set('insert', 'insert-1c')

    # File related functions

    def open_file(self, event=None):
        """Open the file in new tab."""
        file = fd.askopenfile(title="Choose file to open",
                              filetypes=[("Python(default)", "*.py"), ("Text", "*.txt"),
                                         ("Java", "*.java"), ("JavaScript", "*.js"),
                                         ("HTML", "*.html"), ("CSS", "*.css"),
                                         ("All files", "*.*")])
        if file is None:
            return
        else:
            if imghdr.what(
                    file.name):  # if file is image return image type otherwise return None if file is not an image type
                from project_explorer import ProjectExplorer
                ProjectExplorer().open_image(file.name)
            else:
                self.add_tab(file=file.name, open_file=1)
                from syntax_highlight import Highlighting
                Highlighting().highlight2()

    def save_file(self, event=None):
        """Save the content of the current opened tab."""
        try:
            text_area = self.get_current()
        except:
            print('error at save_file')
            return
        current_tab = self.nb.index('current')
        from syntax_highlight import Highlighting
        if self.file_list[current_tab] == None:
            file = fd.asksaveasfile(title="Save file", defaultextension=".txt",
                                    filetypes=[("Python(default)", "*.py"), ("Text", "*.txt"),
                                               ("Java", "*.java"), ("JavaScript", "*.js"),
                                               ("HTML", "*.html"), ("CSS", "*.css"),
                                               ("All files", "*.*")])
            if file is None:
                return
            else:
                self.file_list[current_tab] = file.name
                # file = open(self.file_list[current_tab], mode='w+')
                file.write(text_area.get("1.0", "end-1c"))
                self.rename_tab(os.path.basename(self.file_list[current_tab]))
                file.close()
                print("save_file() first time")
                text_area.edit_modified(arg=False)
                # from syntax_highlight import Highlighting
                Highlighting().highlight2()
                return True
        else:
            file = open(self.file_list[current_tab], "w+")
            file.write(text_area.get("1.0", "end-1c"))
            file.close()
            print("save_file() already")
            print(self.file_list[current_tab], 'saved')
            text_area.edit_modified(arg=False)
            Highlighting().highlight2()
            return True

    def save_as_file(self, event=None):
        """Perform save as operation"""

        file = fd.asksaveasfile(title="Save as", defaultextension=".txt",
                                filetypes=[("Text(default)", "*.txt"), ("Python", "*.py"), ("Java", "*.java"),
                                           ("All files", "*.*")])
        if file == None:
            return
        else:
            # self.file_list.append(file.name)
            file.write(self.get_current().get('1.0', 'end-1c'))
            file.close()
            self.add_tab(file=file.name, open_file=1)
            from syntax_highlight import Highlighting
            Highlighting().highlight2()

    # ------------------------------------------------

    def txt_area_popup_menu(self, event=None):
        """Display the popup menu when user right click inside the text area"""
        try:
            text_area = self.get_current()
            state1 = 'disabled'
            state2 = 'disabled'
            if text_area.modified:
                state1 = 'normal'
            if text_area.count('sel.first', 'sel.last', 'chars')[0] != 'None':
                state2 = 'normal'
            self.popup_menu.entryconfigure(0, state=state1)
            self.popup_menu.entryconfigure(1, state=state1)
            self.popup_menu.entryconfigure(2, state=state2)
            self.popup_menu.entryconfigure(3, state=state2)
            self.popup_menu.post(event.x_root, event.y_root)
        finally:
            self.popup_menu.grab_release()

    def modified_flag(self, event):
        """Change the modified flag of text widget"""
        text = self.get_current()
        text.modified = 1

    i = 1

    def show_hide_project_hierarchy(self, event=None):
        """Show or hide the project hierarchy"""
        # self.project_btn['bg'] = 'gray'
        if self.i == 1:
            self.paned_win.remove(self.left_frame)
            self.i = 0
        else:
            self.paned_win.add(self.left_frame, before=self.right_frame, width=230)
            self.i = 1

    hided = 0

    def tab_close(self, index, child_list):
        """For close the current tab"""
        self.file_list.pop(index)
        child_list[index].destroy()
        self.nb.event_generate("<<NotebookTabClosed>>")

    def on_tab_close(self, event=None):
        """Callback on tab close"""
        if not self.nb.instate(['pressed']):
            return
        element = self.nb.identify(event.x, event.y)
        index = self.nb.index("@%d,%d" % (event.x, event.y))
        child_list = self.nb.winfo_children()
        # print(index, self.nb.index('current'))
        if "close" in element and self.nb._active == index:
            if self.get_current().edit_modified():  # return 1 if text widget is modified otherwise return 0
                ans = mb.askyesnocancel('Confirm on close', 'Do you want to save this file?')
                if ans:
                    if self.save_file():
                        self.tab_close(index, child_list)
                elif ans is False:
                    self.tab_close(index, child_list)
                else:
                    return
            else:
                self.tab_close(index, child_list)
        self.nb.state(["!pressed"])
        self.nb._active = None
        try:
            self.get_current().focus_force()  # For set focus on current tab
        except:
            pass

        if len(self.file_list) == 0:  # unpack the working area when no one tab is remain in notebook
            self.main_frame.pack_forget()
            self.logo_canvas.pack(pady=60)
            self.msg.pack()
            self.main_window.unbind('<Configure>')
            self.main_window.unbind('<KeyPress>')
            self.main_window.unbind('<KeyRelease>')
            self.nb.unbind('<<NotebookTabChanged>>')
            self.main_window.unbind('<Control-S>')
            self.main_window.unbind('<Control-s>')
            self.File.entryconfigure(5, state='disabled')
            for item in range(11):
                try:
                    self.Edit.entryconfigure(item, state='disabled')
                except:
                    pass
            self.File.entryconfigure(6, state='disabled')
            self.Format.entryconfigure(1, state='disabled')
            self.Format.entryconfigure(3, state='disabled')
            self.cursor_pos_lbl['text'] = ''
            self.selected_chars_lbl['text'] = ''
            from toolbar_top_frame import toolbar_obj
            for button in toolbar_obj.button_list:
                button.config(state='disabled')

        # print(self.file_list)

    def keypress_func(self, event=None):
        from syntax_highlight import Highlighting
        self.get_cursor_pos()
        self.get_mini_map_text()
        Highlighting().highlight()

    minimap_flag = 0

    def minimap_show_hide(self):
        """Display or hide minimap"""
        if self.minimap_flag == 0:
            self.code_minimap_frame.pack_forget()
            self.working_area.pack_forget()
            self.line_num_frame.pack(fill='y', side='left')
            self.working_area.pack(fill='both', side='left', expand=True)
            self.code_minimap_frame.pack(fill='both', side='left', pady=(22, 0))
            self.minimap_flag = 1
            self.View.entryconfigure(1, label='  Hide Code Minimap   ', command=self.minimap_show_hide)
        else:
            self.code_minimap_frame.pack_forget()
            self.minimap_flag = 0
            self.View.entryconfigure(1, label='Show Minimap')

    def change_theme(self, event=None):
        self.main_frame['background'] = '#212121'
        style = ttk.Style()
        style.configure("CustomNotebook", background='#212121')
        style.configure("Treeview", background='#212121', fieldbackground='red', foreground='white')
        self.nb.config(style='CustomNotebook')
        childes = self.nb.winfo_children()
        for i in childes:
            i.winfo_children()[0].config(bg='#272822', insertbackground='white', fg='white')
        self.mini_map_text.config(bg='#272822', fg='white', highlightbackground='white')
        self.statusbar_frame.config(bg='#212121')
        self.on_off_project_hierarchy.config(bg='#212121')
        self.project_lbl.config(bg='#212121', fg='white')
        self.canvas['bg'] = '#272822'
        self.cursor_pos_lbl.config(bg='#212121', fg='white')
        self.selected_chars_lbl.config(bg='#212121', fg='white')

    def on_main_win_close(self):
        """Confirm for all opened unsaved files on main window close."""
        child_list = self.nb.winfo_children()
        for i in range(len(child_list)):
            index = self.nb.index('current')
            if self.get_current().edit_modified():
                ans = mb.askyesnocancel('Confirm on close', 'Do you want to save this file?')
                if ans:
                    if self.save_file():
                        self.tab_close(index, child_list)
                    else:
                        return
                elif ans is False:
                    self.tab_close(index, child_list)
                else:
                    return
            else:
                self.tab_close(index, child_list)
        self.main_window.destroy()

    def go_to_line(self, event=None):
        """Set caret to entered line number"""
        go_to_window = tk.Toplevel()
        w = 300
        h = 100
        ws = go_to_window.winfo_screenwidth()
        hs = go_to_window.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        go_to_window.geometry(f"{w}x{h}+{int(x)}+{int(y)}")
        go_to_window.title("Go to Line")
        go_to_window.resizable(0, 0)
        go_to_window.grab_set()
        entry = ttk.Entry(go_to_window, font=(None, 14))
        entry.pack(ipadx=10)
        entry.focus_force()

        def go_to_line():
            textArea = self.get_current()
            line = entry.get()
            if not line:
                line = '1'
            if line.isdigit():
                textArea.mark_set('insert', float(line + ".0"))
                go_to_window.destroy()
                textArea.focus()
                textArea.see(f'{line}.0')
            else:
                mb.showinfo("Input Handling", "This text box takes only integer input!!")

        btn = ttk.Button(go_to_window, text="Go", command=go_to_line)
        btn.pack(ipadx=20)
        btn2 = ttk.Button(go_to_window, text="Cancel", command=go_to_window.destroy)
        btn2.pack(ipadx=20)
        go_to_window.bind('<Return>', go_to_line)
        go_to_window.mainloop()

    def get_date_time(self):
        """Insert current date and time into text area"""
        now = datetime.datetime.now()
        self.get_current().insert('insert', str(now.strftime("%I:%M %p  %d-%m-%Y")))

    def word_wrap(self):
        """Enable wrapping of text in current text area"""
        textArea = self.get_current()
        if self.wrap.get() == 0:
            textArea.config(wrap='none')
        elif self.wrap.get() == 1:
            textArea.config(wrap='word')

    def count_selected_chars(self, event=None):
        """Display number of selected chars and lines on status bar"""
        try:
            textArea = self.get_current()
            chars = textArea.count("sel.first", "sel.last")
            line_breaks = textArea.count("sel.first", "sel.last", "lines")
            if line_breaks:
                if line_breaks[0] == 1:
                    self.selected_chars_lbl.config(text=f"{chars[0]} chars, {line_breaks[0]} line break")
                elif line_breaks[0] > 1:
                    self.selected_chars_lbl.config(text=f"{chars[0]} chars, {line_breaks[0]} line breaks")
            else:
                if chars[0] == 1:
                    self.selected_chars_lbl.config(text=f"{chars[0]} char selected")
                else:
                    self.selected_chars_lbl.config(text=f"{chars[0]} chars selected")
        except:
            self.selected_chars_lbl.config(text="--------------")

    desc_logo = tk.PhotoImage(file='images/desc_logo.png')

    def about(self):
        """About window"""
        about_win = tk.Toplevel()
        w = 600
        h = 350
        ws = about_win.winfo_screenwidth()
        hs = about_win.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        about_win.geometry(f"{w}x{h}+{int(x)}+{int(y)}")
        about_win.focus_force()
        # about_win.geometry("600x350")
        about_win.resizable(0, 0)
        about_win.grab_set()
        frame = tk.Frame(about_win, bg='black')
        frame.pack(fill='both', expand=1)

        logo_lbl = tk.Label(frame, image=self.desc_logo)
        logo_lbl.grid(row=0, column=0, pady=25)

        desc_str = 'This Editor is developed for MCA Vth sem. Minor project purpose'

        description_lbl = tk.Label(frame, text=desc_str, fg='white',
                                   bg='black', font=('Consolas', 12, 'normal'))
        description_lbl.grid(row=1, column=0)

        # param = {}
        lbl1 = tk.Label(frame, text='Project Members', font=('Consolas', 12, 'normal'), fg='black', bg='white')
        lbl1.grid(row=2, column=0)

        mem_lbl = tk.Label(frame, text='Hari Shankar Suthar', font=('Consolas', 12, 'normal'), fg='white', bg='black')
        mem_lbl.grid(row=3, column=0, padx=200)
        mem_lbl = tk.Label(frame, text='Manish Khichi', font=('Consolas', 12, 'normal'), fg='white', bg='black')
        mem_lbl.grid(row=4, column=0, padx=200)
        mem_lbl = tk.Label(frame, text='Siddhant Katariya', font=('Consolas', 12, 'normal'), fg='white', bg='black')
        mem_lbl.grid(row=5, column=0, padx=200)
        mem_lbl = tk.Label(frame, text='tcl version: 8.6', font=('Consolas', 12, 'normal'), fg='black', bg='white')
        mem_lbl.grid(row=6, column=0, sticky='we', padx=200)
