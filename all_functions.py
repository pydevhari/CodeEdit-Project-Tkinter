import imghdr
import os
from tkinter import filedialog as fd
from tkinter import messagebox as mb

from variables import *


class Methods(Variables):
    """Contain all functions for application"""

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

    def get_current(self, event=None) -> Text:
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
                                            font=self.customFont, width=0)
                text_length = self.canvas.bbox('all')  # returns a tuple in the form of (x1, y1, x2, y2)
                width = text_length[2] - text_length[0]  # x2-x1
                self.canvas.config(width=width + 15)
                i = text_area.index("%s+1line" % i)
                # print(self.cursor_pos.cget('pady'), self.statusbar_frame.cget('pady'), )
        except:
            self.canvas.delete('all')


    tab_counter = 0

    def add_tab(self, event=None, file=None, open_file=0):
        """Add a new tab to Notebook widget"""

        tab1 = Frame(self.nb, width=0, bd=0, borderwidth=0, highlightthickness=0)
        tab_width = self.customFont.measure('    ')
        text = Text(tab1, font=self.customFont, wrap='none', width=0, undo=True,
                    tabs=tab_width, padx=2, relief='flat')  # tabs=tab_width
        #     # Horizontal Scrollbar on text area
        y_scrollbar = Scrollbar(tab1, orient='vertical', command=text.yview,
                                width=13, relief='flat')
        text.config(yscrollcommand=y_scrollbar.set)
        # y_scrollbar.config(command=text.yview)
        y_scrollbar.pack(side='right', fill='y')

        x_scrollbar = Scrollbar(tab1, orient=HORIZONTAL, width=13)
        text.config(xscrollcommand=x_scrollbar.set)
        x_scrollbar.config(command=text.xview)
        x_scrollbar.pack(side=BOTTOM, fill=X)

        if file and open_file == 1:
            f = ''
            if file not in self.file_list:
                try:
                    filename = os.path.basename(file)
                    f = open(file)
                    text.insert("1.0", f.read())
                    self.nb.add(tab1, text=filename)
                    self.nb.select(tab1)
                    self.file_list.append(file)
                    text.edit_modified(arg=False)
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
                text.insert("1.0", f.read())
                self.file_list.append(file)
                # f.close()
                self.nb.add(tab1, text=filename)
                self.nb.select(tab1)
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
        text.bind("<ButtonRelease>", self.get_cursor_pos)
        text.bind('<Control-z>', self.undo)
        text.bind('<Control-Z>', self.undo)
        text.bind('<Control-y>', self.redo)
        text.bind('<Control-Y>', self.redo)
        text.bind('<Control-a>', self.select_all)
        text.bind('<Control-A>', self.select_all)
        text.bind("<<Change>>", self.line_counter)
        text.bind("<<Modified>>", self.modified_flag)
        text.bind('<Button-3>', self.popup)  # For display right click popup menu inside the text area
        text.modified = 0
        # ------------------------------------------------------------

        text._orig = text._w + "_orig"
        text.tk.call("rename", text._w, text._orig)
        text.tk.createcommand(text._w, self.proxy)
        text.pack(fill='both', expand=1)

        text.focus_force()
        text.edit('reset')
        text.edit_modified(arg=False)
        self.get_cursor_pos()
        print(self.file_list)

        if len(self.file_list) == 1:  # Repack the working area
            self.main_frame.pack(fill='both', side='left', expand=1)
            self.main_window.bind('<Configure>', self.line_counter)
            self.main_window.bind('<KeyPress>', self.keypress_func)
            self.nb.bind('<<NotebookTabChanged>>', self.get_mini_map_text)
            self.file_type_lbl['text'] = 'Plain Text'
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
        self.mini_map_text.config(state=NORMAL)
        self.mini_map_text.delete('1.0', 'end')
        self.mini_map_text.insert('1.0', data)
        self.mini_map_text.config(state=DISABLED)
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
        except: pass

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
        textArea.see('insert')

    def select_all(self, event=None):
        """Select the all text of text area"""
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
                              filetypes=[("Text(default)", "*.txt"), ("Python", "*.py"),
                                         ("Java", "*.java"), ("JavaScript", "*.js"),
                                         ("HTML", "*.html"), ("CSS", "*.css"),
                                         ("All files", "*.*")])
        if file is None:
            return
        else:
            if imghdr.what(file.name):  # if file is image return image type otherwise return None if file is not an image type
                from project_explorer import ProjectExplorer
                ProjectExplorer().open_image(file.name)
            else:
                self.add_tab(file=file.name, open_file=1)

    def save_file(self, event=None):
        """Save the content of the current opened tab."""
        try:
            text_area = self.get_current()
        except:
            print('error at save_file')
            return
        current_tab = self.nb.index('current')
        if self.file_list[current_tab] == None:
            file = fd.asksaveasfile(title="Save file", defaultextension=".txt",
                                    filetypes=[("Text(default)", "*.txt"), ("Python", "*.py"),
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
                return True
        else:
            file = open(self.file_list[current_tab], "w+")
            file.write(text_area.get("1.0", "end-1c"))
            file.close()
            print("save_file() already")
            print(self.file_list[current_tab], 'saved')
            text_area.edit_modified(arg=False)
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

    def popup(self, event):
        """Display the popup menu when user right click inside the text area"""
        try:
            text = self.get_current()
            state1 = 'disabled'
            state2 = 'disabled'
            if text.modified:
                state1 = 'normal'
            if text.count('sel.first', 'sel.last', 'chars')[0] != 'None':
                state2 = 'normal'
            self.popup_menu.entryconfigure(0, state=state1)
            self.popup_menu.entryconfigure(1, state=state1)
            # print(text.)
            self.popup_menu.entryconfigure(2, state=state2)
            self.popup_menu.entryconfigure(3, state=state2)
            # self.popup_menu.entryconfigure(0, state='normal')
            # self.popup_menu.entryconfigure(0, state='normal')
            # self.popup_menu.entryconfigure(0, state='normal')
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
        except: pass

        if len(self.file_list) == 0:  # unpack the working area when no one tab is remain in notebook
            self.main_frame.pack_forget()
            self.main_window.unbind('<Configure>')
            self.main_window.unbind('<KeyPress>')
            self.nb.unbind('<<NotebookTabChanged>>')
            self.cursor_pos_lbl['text'] = ''
            self.file_type_lbl['text'] = ''
            from toolbar_top_frame import toolbar_obj
            for button in toolbar_obj.button_list:
                button.config(state='disabled')

        # print(self.file_list)

    def keypress_func(self, event=None):
        self.get_cursor_pos()
        self.get_mini_map_text()


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
        self.file_type_lbl.config(bg='#212121', fg='white')


    def on_main_win_close(self):
        """Confirm for all opened unsaved files on main window close."""
        child_list = self.nb.winfo_children()
        for i in range(len(self.nb.winfo_children())):
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
