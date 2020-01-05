# from tkinter import filedialog as fd
from tkinter import messagebox as mb
from common_tasks import CommonTask
from PIL import ImageTk as itk
from PIL import Image
from tkinter import filedialog as fd
from small_window import ToplevelWindow
from tkinter import ttk
import tkinter as tk
import imghdr
import os


class ProjectExplorer(CommonTask):
    """Provide callback methods for treeview related events such as
     open directory, open file, open image etc."""

    def create_project(self):
        """Method for create the  project directory"""
        win = tk.Toplevel()
        win.geometry('500x150')
        win.title('Create Project')
        win.grab_set()
        win.resizable(0, 0)
        small_win = ToplevelWindow()
        small_win.center_toplevel_window(win)
        pro_name_lbl = ttk.Label(win, text='Project Name: ')
        pro_name_lbl.grid(row=0, column=0, sticky='w', padx=(20, 0), pady=(20, 0))
        pro_name_entry = ttk.Entry(win, width=50)
        pro_name_entry.grid(row=0, column=1, pady=(20, 0))
        pro_name_entry.focus_force()
        pro_name_war_lbl = ttk.Label(win, text='')
        pro_name_war_lbl.grid(row=4, column=1, sticky='w', pady=(20, 0))

        pro_loc_lbl = ttk.Label(win, text='Project Location: ')
        pro_loc_lbl.grid(row=1, column=0, sticky='w', padx=(20, 0))
        pro_loc_entry = ttk.Entry(win, width=50)
        pro_loc_entry.insert(0, 'C:\\CodeEdit\\Projects')
        pro_loc_entry.grid(row=1, column=1)
        pro_loc_browse_btn = ttk.Button(win, text='Browse')
        pro_loc_browse_btn.grid(row=1, column=2, sticky='w')

        pro_fold_lbl = ttk.Label(win, text='Project Folder: ')
        pro_fold_lbl.grid(row=2, column=0, sticky='w', padx=(20, 0))
        pro_fold_entry = ttk.Entry(win, width=50)
        pro_fold_entry.insert(0, 'C:\\CodeEdit\\Projects\\')
        pro_fold_entry.config(state='disabled')
        pro_fold_entry.grid(row=2, column=1)

        # Create project button
        create_pro_btn = ttk.Button(win, text='Create Project', state='disabled')
        create_pro_btn.grid(row=3, column=1, sticky='w', ipadx=35, padx=2)
        # Cancel button
        close_btn = ttk.Button(win, text='Cancel', command=win.destroy)
        close_btn.grid(row=3, column=1, sticky='e', ipadx=35, padx=2)

        def validate_fold_name(event):
            pro_name = pro_name_entry.get()
            pro_loc = pro_loc_entry.get()
            flag1 = self.file_folder_name_validator(pro_name)
            flag2 = self.file_folder_name_validator(pro_loc[pro_loc.rindex('\\') + 1:])
            if flag1 and flag2:
                pro_name_war_lbl.config(text='')
                create_pro_btn.config(state='normal')
            else:
                if not flag1:
                    pro_name_war_lbl.config(text='Enter a valid Project Name!!', foreground='red')
                else:
                    pro_name_war_lbl.config(text='Enter a valid Project Location!!', foreground='red')
                create_pro_btn.config(state='disabled')
            get_path = pro_loc_entry.get()
            pro_fold_entry.config(state='normal')
            pro_fold_entry.delete(0, 'end')
            pro_fold_entry.insert(0, get_path + '\\' + pro_name)
            pro_fold_entry.icursor('end')
            pro_fold_entry.config(state='disabled')

        def browse():
            dir_name = fd.askdirectory(title='Choose Project Location')
            if not dir_name:
                return
            pro_loc_entry.delete(0, 'end')
            pro_loc_entry.insert(0, dir_name.replace('/', '\\'))
            pro_fold_entry.config(state='normal')
            pro_name = pro_name_entry.get()
            pro_fold_entry.delete(0, 'end')
            pro_fold_entry.insert(0, dir_name.replace('/', '\\') + '\\' + pro_name)
            pro_fold_entry.config(state='disabled')
            pro_loc_entry.focus_force()

        def create_pro(event=None):
            try:
                pro_path = pro_fold_entry.get()
                os.makedirs(pro_path)
                self.open_project(pro_path=pro_path)
                win.destroy()
            except FileExistsError:
                mb.showerror('Project Name Already Exist', 'Please choose another Project name.\nIt is already exist.')
                win.focus_force()
            except Exception as e:
                mb.showerror('Exception', e)
                win.focus_force()

        pro_loc_browse_btn.config(command=browse)
        create_pro_btn.config(command=create_pro)
        win.bind('<Return>', create_pro)
        win.bind('<KeyPress>', validate_fold_name)

    def open_project(self, event=None, pro_path=''):
        """For open the project"""
        if not pro_path:
            path = fd.askdirectory(title="Choose project")
            if not path:
                return
        else:
            path = pro_path

        # path = r'C:\Users\hp\OneDrive\Desktop\icons'

        abspath = os.path.abspath(path=path)
        self.insert_node('', abspath, abspath)
        self.tree.heading('#0', text=os.path.basename(path))
        self.main_window.title(f'{os.path.basename(path)} [{path}] -CodeEdit')
        return "break"

    img = itk.PhotoImage(file='images/folder.png')
    img2 = itk.PhotoImage(file='images/file.png')
    img3 = itk.PhotoImage(file='images/icons8-image-file-16.png')
    img4 = itk.PhotoImage(file='images/python.png')

    nodes = dict()

    def insert_node(self, parent, text, abspath, index='end', indirect=0):
        """Inserts nodes to treeview"""
        if os.path.isdir(abspath):
            node = self.tree.insert(parent, index, text=text, open=False, image=self.img)
        elif imghdr.what(abspath):
            node = self.tree.insert(parent, index, text=text, open=False, image=self.img3)
        elif abspath.endswith('.py'):
            node = self.tree.insert(parent, index, text=text, open=False, image=self.img4)
        else:
            node = self.tree.insert(parent, index, text=text, open=False, image=self.img2)
        if indirect:
            self.tree.selection_set(node)
            self.tree.see(node)
            return
        if os.path.isdir(abspath):
            self.nodes[node] = abspath
            self.tree.insert(node, 'end')  # an empty node to activate expand/collapse button

    def open_node(self, event=None):
        """This method is invoke when user expand the folder/node"""
        node = self.tree.focus()
        abspath = self.nodes.pop(node, None)
        if abspath:
            self.tree.delete(self.tree.get_children(node))
            dirlist = [dir for dir in os.listdir(abspath) if
                       os.path.isdir(abspath + '\\' + dir)]  # get list of all directoies
            filelist = [file for file in os.listdir(abspath) if
                        not os.path.isdir(abspath + '\\' + file)]  # get list of all files
            filelist.extend(dirlist)  # merge both lists
            for item in filelist:
                self.insert_node(node, item, os.path.join(abspath, item))

    def get_selected_file_path(self, event=None, opentab=1):
        """Return the parent of parent of parent and so on.
        Means return the full path of selected item of treeview"""
        if self.tree.parent(self.tree.selection()):
            parent = self.tree.parent(self.tree.selection())
        else:
            return self.tree.item(self.tree.selection())['text']  # return the full path of the project
        file_path = [self.tree.item(self.tree.selection())['text']]
        # file_path.append(self.tree.item(self.tree.parent(self.tree.selection()))['text'])
        file_path.insert(0, self.tree.item(self.tree.parent(self.tree.selection()))['text'])
        while True:
            if self.tree.parent(parent):
                # file_path.append(self.tree.item(self.tree.parent(parent))['text'])
                file_path.insert(0, self.tree.item(self.tree.parent(parent))['text'])
                parent = self.tree.parent(parent)
            else:
                break
        # file_path.reverse()
        file_path = '\\'.join(file_path)
        if opentab:
            if not os.path.isdir(file_path):
                try:
                    if imghdr.what(file_path):
                        self.open_image(img=file_path)
                        return
                    else:
                        self.add_tab(file=file_path, open_file=1)
                        return
                except Exception as e:
                    mb.showerror('Error', e)
        else:
            return file_path  # return the full file path of selected item of the treeview

    def tree_right_click(self, event):
        if self.tree.identify_row(event.y):
            # self.tree.selection_remove(self.tree.selection())  # Remove previous selected items from treeview
            self.tree.selection_set(self.tree.identify_row(event.y))  # select the currently right clicked treeview item
            file_path = self.get_selected_file_path(opentab=0)
            if os.path.isdir(file_path):
                try:
                    self.popup_for_folder.post(event.x_root, event.y_root)
                finally:
                    self.popup_for_folder.grab_release()
            else:
                try:
                    self.popup_for_file.post(event.x_root, event.y_root)
                finally:
                    self.popup_for_file.grab_release()

    def delete_file_folder(self):
        import shutil
        try:
            if os.path.isdir(self.get_selected_file_path(opentab=0)):
                if mb.askyesno('Confirm on delete', 'Do you want to delete this folder?'):
                    for i in self.file_list:
                        if i:
                            if i.__contains__(self.get_selected_file_path(opentab=0)):
                                mb.showerror("Can't delete", 'This folder is used in currently.\nClose the openned '
                                                             'files and try again.')
                                return
                    shutil.rmtree(self.get_selected_file_path(opentab=0))
                    self.tree.heading('#0', text='Open Project')
                    self.main_window.title('CodeEdit')

                else:
                    return
            else:
                if mb.askyesno('Confirm on delete', 'Do you want to delete this file?'):
                    if self.get_selected_file_path(opentab=0) in self.file_list:
                        child_list = self.nb.winfo_children()
                        self.tab_close(self.nb.index('current'), child_list)
                    os.remove(self.get_selected_file_path(opentab=0))
                else:
                    return
            self.tree.delete(self.tree.selection())
        except Exception as e:
            mb.showerror("Error", e)

    def file_folder_name_validator(self, file_dir_name):
        """File and Folder name validator. If name is valid then return True otherwise return False."""
        if not len(file_dir_name) is 0 and not file_dir_name.isspace():
            for i in '\\/?<>*|':
                if i in file_dir_name:
                    return False
            return True
        else:
            return False

    def new_folder(self):
        """Callback for create new directory"""

        def create_directory(event=None):
            """Directory creation logic"""
            dir_path = self.get_selected_file_path(opentab=0)
            dir_name = small_win.entry.get()
            if self.file_folder_name_validator(dir_name):
                try:
                    self.tree.item(self.tree.selection(), open=True)  # First, open the node
                    self.open_node()
                    os.mkdir(dir_path + '\\' + dir_name)
                    dirlist = [dir for dir in os.listdir(dir_path) if
                               os.path.isdir(dir_path + '\\' + dir)]  # get list of all directories
                    filelist = [file for file in os.listdir(dir_path) if
                                not os.path.isdir(dir_path + '\\' + file)]  # get list of all files
                    filelist.extend(dirlist)  # merge both lists

                    self.insert_node(self.tree.selection(), text=dir_name,
                                     index=f'{filelist.index(dir_name)}',
                                     abspath=dir_path + '\\' + dir_name, indirect=1)
                    small_win.win.destroy()
                except FileExistsError:
                    mb.showerror('Directory already exists', 'Choose another directory name')
                    small_win.entry.focus_force()
                except Exception as e:
                    mb.showerror('Error', e)
                    small_win.entry.focus_force()
            else:
                mb.showerror('Error', 'Enter valid directory name'.center(5, ' '))
                small_win.entry.focus_force()

        small_win = ToplevelWindow()
        small_win.create_win(title='Create New Folder', btn_text='Create Folder', callback=create_directory)

    def new_file(self):
        """Callback for create new file"""

        def create_file(event=None):
            """File creation logic"""
            dir_path = self.get_selected_file_path(opentab=0)
            file_name = small_win.entry.get()
            if self.file_folder_name_validator(file_name):
                if '.' in file_name and len(file_name[file_name.rindex('.') + 1:]) > 0:
                    try:
                        self.tree.item(self.tree.selection(), open=True)  # First open the node
                        self.open_node()
                        open(dir_path + '\\' + file_name, mode='x').close()  # Create a new file
                        filelist = [file for file in os.listdir(dir_path) if
                                    not os.path.isdir(dir_path + '\\' + file)]  # get list of all files
                        filelist.append(file_name)
                        filelist.sort(key=str.lower)
                        # id = self.tree.insert(self.tree.selection(), f'{filelist.index(file_name)}', text=file_name, image=self.img2)  # insert the item
                        self.insert_node(self.tree.selection(), text=file_name, index=f'{filelist.index(file_name)}',
                                         abspath=dir_path + '\\' + file_name, indirect=1)
                        small_win.win.destroy()
                        self.add_tab(file=dir_path + '\\' + file_name, open_file=1)
                    except FileExistsError:
                        ans = mb.askyesno('File already exists', 'Do you want to replace this file?')
                        if ans:
                            open(dir_path + '\\' + file_name, "w").close()
                            small_win.win.destroy()
                            child = self.tree.get_children(self.tree.selection())
                            for item in child:
                                if self.tree.item(item)['text'] == file_name:
                                    self.tree.selection_set(item)
                                    self.add_tab(file=dir_path + '\\' + file_name, open_file=1)
                        else:
                            small_win.entry.focus_force()
                    except Exception as e:
                        mb.showerror('Error', e)
                else:
                    try:
                        self.tree.item(self.tree.selection(), open=True)  # First open the
                        self.open_node()
                        open(dir_path + '\\' + file_name + '.txt', mode='x').close()
                        filelist = [file for file in os.listdir(dir_path) if
                                    not os.path.isdir(dir_path + '\\' + file)]  # get list of all files
                        filelist.append(file_name)
                        filelist.sort(key=str.lower)
                        # id = self.tree.insert(self.tree.selection(), f'{filelist.index(file_name)}', text=file_name+'.txt', image=self.img2)  # insert the item
                        self.insert_node(self.tree.selection(), text=file_name + '.txt',
                                         index=f'{filelist.index(file_name)}',
                                         abspath=dir_path + '\\' + file_name + '.txt', indirect=1)
                        small_win.win.destroy()
                        self.add_tab(file=dir_path + '\\' + file_name + '.txt', open_file=1)
                    except FileExistsError:
                        ans = mb.askyesno('File already exists', 'Do you want to replace this file?')
                        if ans:
                            open(dir_path + '\\' + file_name + '.txt', "w").close()
                            child = self.tree.get_children(self.tree.selection())
                            for item in child:
                                if self.tree.item(item)['text'] == file_name + '.txt':
                                    self.tree.item(self.tree.selection(), open=True)
                                    self.tree.selection_set(item)
                                    self.add_tab(file=dir_path + '\\' + file_name + '.txt', open_file=1)
                            small_win.win.destroy()
                        else:
                            small_win.entry.focus_force()
                    except Exception as e:
                        mb.showerror('Error', e)

            else:
                mb.showerror('Error', 'Enter valid file name'.center(5, ' '))
                small_win.entry.focus_force()

        small_win = ToplevelWindow()
        small_win.create_win(title='New File', btn_text='Create File', callback=create_file)

    def rename_file_folder(self):
        """Rename file or folder"""
        small_win = ToplevelWindow()
        small_win.create_win(title='', btn_text='', callback='')
        file_or_folder_path = self.get_selected_file_path(opentab=0)
        old_file_name = os.path.basename(file_or_folder_path)
        small_win.entry.insert(0, old_file_name)
        if not os.path.isdir(file_or_folder_path):
            small_win.entry.selection_range(0, old_file_name.rindex('.'))
            small_win.entry.icursor(old_file_name.rindex('.'))
            action_id = "File"
        else:
            action_id = "Folder"
        small_win.win.title(f'Rename {action_id}')

        def rename_file_folder(event=None):
            """Rename the selected file or folder"""

            def rename():
                """rename logic for code reusability"""
                global new_name
                new_name = file_or_folder_path.replace(os.path.basename(file_or_folder_path), '') \
                           + new_file_folder_name
                os.rename(file_or_folder_path, new_name)

            selection = self.tree.selection()
            try:
                global new_name
                new_file_folder_name = small_win.entry.get()
                if self.file_folder_name_validator(new_file_folder_name):
                    if os.path.isdir(file_or_folder_path):
                        rename()
                        self.nodes[selection[0]] = new_name  # update the nodes dictionary
                        if not self.tree.parent(selection):  # rename for project{parent of treeview}
                            self.tree.item(selection, text=new_name)
                            self.tree.heading('#0', text=os.path.basename(new_name))

                        else:
                            self.tree.item(selection, text=new_file_folder_name)
                        small_win.win.destroy()
                    else:
                        # global selection
                        if '.' in new_file_folder_name \
                                and len(new_file_folder_name[new_file_folder_name.rindex('.') + 1:]) > 0 \
                                and len(new_file_folder_name[new_file_folder_name.index('.')::-1]) - 1:
                            rename()
                            if file_or_folder_path in self.file_list:
                                tab_index = self.file_list.index(file_or_folder_path)
                                self.nb.tab(tab_index, text=os.path.basename(new_name))
                                self.file_list[tab_index] = new_name

                            self.tree.item(selection, text=new_file_folder_name)
                            small_win.win.destroy()
                        else:
                            mb.showerror('Error', 'Enter a valid file name')
                            small_win.entry.focus_force()
                else:
                    mb.showerror('Error', f"Enter valid {action_id} name")
                    small_win.entry.focus_force()
            except FileExistsError:
                mb.showerror('Error', f'{action_id} already exist. Enter another {action_id} name.')
                small_win.entry.focus_force()
            except Exception as e:
                mb.showerror('Error', e)

        small_win.btn.config(text=f'Rename {action_id}', command=rename_file_folder)
        small_win.win.bind('<Return>', rename_file_folder)

    def copy_folder_path(self):
        """Append selected folder's path to clipboard"""
        self.main_window.clipboard_clear()
        self.main_window.clipboard_append(self.get_selected_file_path(opentab=0))

    def copy_file_path(self):
        """Append selected files's path to clipboard"""
        self.main_window.clipboard_clear()
        self.main_window.clipboard_append(self.get_selected_file_path(opentab=0))

    def open_image(self, img):
        # from PIL import ImageTk, Image
        win = tk.Toplevel()
        win.title(img + "   CodeEdit ImageViewer")
        win.focus_force()
        canvas = tk.Canvas(win, bg='black', width=400, height=400)
        canvas.pack(fill='both', expand=1)
        image = itk.PhotoImage(Image.open(img), master=win)

        def expand(event):
            canvas.delete('all')
            canvas.create_image(event.width / 2, event.height / 2, image=image, anchor='center')

        canvas.bind('<Configure>', expand)
        # win.mainloop()
