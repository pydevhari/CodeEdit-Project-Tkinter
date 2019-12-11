# from tkinter import filedialog as fd
from tkinter import messagebox as mb
from all_functions import Methods
from PIL import ImageTk as itk
from tkinter import filedialog as fd
from tkinter import ttk
import tkinter as tk
import imghdr
import os


class ProjectExplorer(Methods):
    """Provide callback methods for treeview related events such as
     open directory, open file, open image etc."""

    def open_directory(self, event=None):
        """For open the project"""
        # path = fd.askdirectory(title="Choose project")
        path = r'C:\Users\hp\OneDrive\Desktop\icons'
        if not path:
            return
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
                    shutil.rmtree(self.get_selected_file_path(opentab=0))
                else:
                    return
            else:
                if mb.askyesno('Confirm on delete', 'Do you want to delete this file?'):
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

    def new_dir(self):
        """Callback for create new directory"""
        win = tk.Tk()
        self.center_small_window(win)
        win.resizable(0, 0)
        win.title('Create New Folder')
        win.geometry('300x100')
        entry = ttk.Entry(win, font=('Consolas', 12))
        entry.focus_force()
        entry.pack(fill='x', pady=(10, 0), padx=5)

        def create_directory(event=None):
            """Directory creation logic"""
            dir_path = self.get_selected_file_path(opentab=0)
            dir_name = entry.get()
            if self.file_folder_name_validator(dir_name):
                try:
                    os.mkdir(dir_path + '\\' + dir_name)
                    filelist = [file for file in os.listdir(dir_path)
                                if not os.path.isdir(dir_path + '\\' + file)]  # get list of all files
                    dirlist = [dir for dir in os.listdir(dir_path)
                               if os.path.isdir(dir_path + '\\' + dir)]  # get list of all directoies
                    filelist.extend(dirlist)  # merge both lists
                    self.tree.item(self.tree.selection(), open=True)
                    self.open_node()
                    id = self.tree.insert(parent=self.tree.selection(), index=f'{filelist.index(dir_name)}',
                                          text=dir_name, image=self.img)  # insert the item
                    self.tree.selection_set(id)  # select the item
                    win.destroy()
                except FileExistsError:
                    mb.showerror('Directory already exists', 'Choose another directory name')
                    entry.focus_force()
                except Exception as e:
                    mb.showerror('Error', e)
                    entry.focus_force()
            else:
                mb.showerror('Error', 'Enter valid directory name'.center(5, ' '))
                entry.focus_force()

        entry.bind('<Return>', create_directory)
        btn = ttk.Button(win, text='Create File', command=create_directory, width=23)
        btn.pack(pady=(20, 0), ipady=2, side='left', expand=True, padx=5)
        btn2 = ttk.Button(win, text='Cancel', command=win.destroy, width=23)
        btn2.pack(pady=(20, 0), ipady=2, side='left', expand=True, padx=5)

        def destroy(event):
            win.destroy()

        btn2.bind('<Return>', destroy)

    def new_file(self):
        """Callback for create new file"""
        win = tk.Tk()
        self.center_small_window(win)
        win.resizable(0, 0)
        win.title('Create New File')
        win.geometry('300x100')
        entry = ttk.Entry(win, font=('Consolas', 12))
        entry.focus_force()
        entry.pack(fill='x', pady=(10, 0), padx=5)

        def create_file(event=None):
            """File creation logic"""
            dir_path = self.get_selected_file_path(opentab=0)
            file_name = entry.get()
            if self.file_folder_name_validator(file_name):
                if '.' in file_name and len(file_name[file_name.rindex('.') + 1:]) > 0:
                    try:
                        open(dir_path + '\\' + file_name, mode='x').close()  # Create a new file
                        filelist = [file for file in os.listdir(dir_path) if
                                    not os.path.isdir(dir_path + '\\' + file)]  # get list of all files
                        filelist.append(file_name)
                        filelist.sort(key=str.lower)
                        # id = self.tree.insert(self.tree.selection(), f'{filelist.index(file_name)}', text=file_name, image=self.img2)  # insert the item
                        self.tree.item(self.tree.selection(), open=True)  # First open the node
                        self.insert_node(self.tree.selection(), text=file_name, index=f'{filelist.index(file_name)}',
                                         abspath=dir_path + '\\' + file_name, indirect=1)
                        win.destroy()
                        self.add_tab(file=dir_path + '\\' + file_name, open_file=1)
                    except FileExistsError:
                        ans = mb.askyesno('File already exists', 'Do you want to replace this file?')
                        if ans:
                            open(dir_path + '\\' + file_name, "w").close()
                            win.destroy()
                            child = self.tree.get_children(self.tree.selection())
                            for item in child:
                                if self.tree.item(item)['text'] == file_name:
                                    self.tree.selection_set(item)
                                    self.add_tab(file=dir_path + '\\' + file_name, open_file=1)
                        else:
                            entry.focus_force()
                    except Exception as e:
                        mb.showerror('Error', e)
                else:
                    try:
                        open(dir_path + '\\' + file_name + '.txt', mode='x').close()
                        self.tree.item(self.tree.selection(), open=True)  # First open the node
                        filelist = [file for file in os.listdir(dir_path) if
                                    not os.path.isdir(dir_path + '\\' + file)]  # get list of all files
                        filelist.append(file_name)
                        filelist.sort(key=str.lower)
                        # id = self.tree.insert(self.tree.selection(), f'{filelist.index(file_name)}', text=file_name+'.txt', image=self.img2)  # insert the item
                        self.insert_node(self.tree.selection(), text=file_name + '.txt',
                                         index=f'{filelist.index(file_name)}',
                                         abspath=dir_path + '\\' + file_name + '.txt', indirect=1)
                        win.destroy()
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
                            win.destroy()
                        else:
                            entry.focus_force()
                    except Exception as e:
                        mb.showerror('Error', e)

            else:
                mb.showerror('Error', 'Enter valid file name'.center(5, ' '))
                entry.focus_force()

        # except:
        #     mb.showerror('Error', 'File aready exist')
        #     win.focus_force()

        entry.bind('<Return>', create_file)
        btn = ttk.Button(win, text='Create File', command=create_file, width=23)
        btn.pack(pady=(20, 0), ipady=2, side='left', expand=True, padx=5)
        btn2 = ttk.Button(win, text='Cancel', command=win.destroy, width=23)
        btn2.pack(pady=(20, 0), ipady=2, side='left', expand=True, padx=5)

        def destroy(event):
            win.destroy()

        btn2.bind('<Return>', destroy)
        # win.mainloop()

    def center_small_window(self, win):
        """Display small windows in the central area of main window"""
        w = 600
        h = 200
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        win.geometry(f"{w}x{h}+{int(x)}+{int(y)}")  # set the window in center of the screen

    def rename_file_folder(self):
        win = tk.Tk()
        self.center_small_window(win)
        win.resizable(0, 0)
        win.geometry('300x100')
        entry = ttk.Entry(win, font=('Consolas', 12))
        entry.focus_force()
        entry.pack(fill='x', pady=(10, 0), padx=5)

        file_or_folder_path = self.get_selected_file_path(opentab=0)
        old_file_name = os.path.basename(file_or_folder_path)
        entry.insert(0, old_file_name)
        if not os.path.isdir(file_or_folder_path):
            entry.selection_range(0, old_file_name.rindex('.'))
            entry.icursor(old_file_name.rindex('.'))
            id = "File"
        else:
            id = "Folder"

        win.title(f'Rename {id}')

        def rename_file_folder():
            """Rename the selected file or folder"""

            def rename():
                """rename logic for code reusability"""
                global new_name
                new_name = file_or_folder_path.replace(os.path.basename(file_or_folder_path), '') \
                           + new_file_folder_name
                os.rename(file_or_folder_path, new_name)

            try:
                new_file_folder_name = entry.get()
                if self.file_folder_name_validator(new_file_folder_name):
                    if os.path.isdir(file_or_folder_path):
                        rename()
                        self.nodes[self.tree.selection()[0]] = new_name  # update the nodes dictionary
                        self.tree.item(self.tree.selection(), text=new_file_folder_name)
                        win.destroy()
                    else:
                        if '.' in new_file_folder_name \
                                and len(new_file_folder_name[new_file_folder_name.rindex('.') + 1:]) > 0 \
                                and len(new_file_folder_name[new_file_folder_name.index('.')::-1])-1:
                            rename()
                            if file_or_folder_path in self.file_list:
                                tab_index = self.file_list.index(file_or_folder_path)
                                self.nb.tab(tab_index, text=os.path.basename(new_name))
                                self.file_list[tab_index] = new_name
                            self.tree.item(self.tree.selection(), text=new_file_folder_name)
                            win.destroy()
                        else:
                            mb.showerror('Error', 'Enter a valid file name')
                            entry.focus_force()
                else:
                    mb.showerror('Error', f"Enter valid {id} name")
                    entry.focus_force()
            except FileExistsError:
                mb.showerror('Error', f'{id} already exist. Enter another {id} name.')
                entry.focus_force()
            except Exception as e:
                mb.showerror('Error', e)
        entry.bind('<Return>', rename_file_folder)
        btn = ttk.Button(win, text=f'Rename {id}', width=23, command=rename_file_folder)
        btn.pack(pady=(20, 0), ipady=2, side='left', expand=True, padx=5)
        btn2 = ttk.Button(win, text='Cancel', command=win.destroy, width=23)
        btn2.pack(pady=(20, 0), ipady=2, side='left', expand=True, padx=5)

        def destroy(event):
            win.destroy()

        btn2.bind('<Return>', destroy)

    def open_image(self, img):
        from PIL import ImageTk, Image
        win = tk.Tk()
        canvas = tk.Canvas(win, bg='black', width=400, height=400)
        canvas.pack(fill='both', expand=1)
        image = ImageTk.PhotoImage(Image.open(img), master=win)

        def expand(event):
            canvas.delete('all')
            canvas.create_image(event.width / 2, event.height / 2, image=image, anchor='center')

        canvas.bind('<Configure>', expand)
        win.mainloop()
