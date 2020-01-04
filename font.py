from all_functions import CommonTask
import tkinter as tk
from tkinter import ttk


class Font(CommonTask):
    """Perform increase, decrease font size, change font style operations"""

    def increase_font(self, event=None):
        """Increase font of the editor and line number"""
        if self.font_size < 40:
            self.font_size += 1
            self.customFont.config(size=self.font_size)
            self.lineFont.config(size=self.font_size)
            # self.get_current().config(font=self.customFont)
            if self.pady < 30:  # for control top padding of line number
                self.pady += 1
                self.canvas.pack_configure(pady=(self.pady, 0))
            self.canvas.update()

    def decrease_font(self, event=None):
        """Decrease font of the editor and line number"""
        if self.font_size > 10:
            self.font_size -= 1
            self.customFont.config(size=self.font_size)
            self.lineFont.config(size=self.font_size)
            # self.get_current().config(font=self.customFont)
            if self.pady > 1:
                self.pady -= 1
                self.canvas.pack_configure(pady=(self.pady, 0))
            self.canvas.update()
        # print(self.font_size)

    def font_reset(self, event=None):
        """Reset the font size of editor and line number"""
        self.font_size = 12
        self.canvas.pack_configure(pady=2)
        self.customFont.configure(size=self.font_size)
        self.lineFont.config(size=self.font_size)
        # self.get_current().config(font=self.customFont)

    def change_font(self, event=None):
        """Change the font preference of the editor"""
        font_win = tk.Toplevel()
        font_win.title('CodeEdit Font Preferences')
        font_win.geometry('540x410')
        w = 540
        h = 410
        ws = font_win.winfo_screenwidth()
        hs = font_win.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        font_win.geometry(f"{w}x{h}+{int(x)}+{int(y)}")
        font_win.focus_force()
        font_win.grab_set()
        # font_win.resizable(0, 0)

        ttk.Label(font_win, text='Font:').grid(row=0, column=0)
        ttk.Label(font_win, text='Font Style:').grid(row=0, column=1)
        ttk.Label(font_win, text='Font Size:').grid(row=0, column=2)

        # frame2 = tk.Frame(font_win, width=200).grid(row=1, column=1, padx=(12, 0))
        # frame2 = tk.Frame(font_win, width=200).grid(row=1, column=1, padx=(12, 0))

        padx = 10
        font_style = ttk.Entry(font_win, width=30, state='disabled')
        font_style.grid(row=1, column=0, padx=(padx, 0))

        font_weight = ttk.Entry(font_win, width=16)
        font_weight.grid(row=1, column=1, padx=(padx, 0))

        font_size = ttk.Entry(font_win, width=18)
        font_size.grid(row=1, column=2, padx=(padx, 0))

        frame1 = tk.Frame(font_win, width=0, bg='red')
        frame1.grid(row=2, column=0, padx=(padx, 0))
        frame2 = tk.Frame(font_win, width=0, bg='red')
        frame2.grid(row=2, column=1, padx=(padx, 0))
        frame3 = tk.Frame(font_win, width=0, bg='red')
        frame3.grid(row=2, column=2, padx=(padx, 0))

        # list of all supported fonts
        font_list = ['Consolas', 'Terminal', 'Fixedsys', 'Modern', 'Roman', 'Script', 'Courier',
                     'MS Sans Serif', 'Small Fonts', 'Arial',
                     'Arabic Transparent', 'Arial Baltic', 'Arial CE', 'Arial CYR',
                     'Arial Greek', 'Arial TUR', 'Arial Black', 'Bahnschrift Light',
                     'Bahnschrift SemiLight', 'Bahnschrift', 'Bahnschrift SemiBold',
                     'Bahnschrift Light SemiCondensed', 'Bahnschrift SemiLight SemiConde',
                     'Bahnschrift SemiCondensed', 'Bahnschrift SemiBold SemiConden',
                     'Bahnschrift Light Condensed', 'Bahnschrift SemiLight Condensed',
                     'Bahnschrift Condensed', 'Bahnschrift SemiBold Condensed', 'Calibri',
                     'Calibri Light', 'Cambria', 'Candara', 'Candara Light',
                     'Comic Sans MS', 'Constantia', 'Corbel', 'Corbel Light',
                     'Courier New', 'Courier New Baltic', 'Courier New CE', 'Courier New CYR',
                     'Courier New Greek', 'Courier New TUR', 'Ebrima', 'Franklin Gothic Medium',
                     'Gabriola', 'Gadugi', 'Georgia', 'Impact', 'Ink Free',
                     'Leelawadee UI', 'Leelawadee UI Semilight', 'Lucida Console',
                     'Malgun Gothic', '@Malgun Gothic', 'Malgun Gothic Semilight', ]

        font_lstbx1 = ttk.Treeview(frame1, show='tree', selectmode='browse')
        v_scrollbar = ttk.Scrollbar(frame1, orient='vertical', command=font_lstbx1.yview)
        font_lstbx1.configure(yscrollcommand=v_scrollbar.set)
        v_scrollbar.pack(side='right', fill='y')
        font_lstbx1.pack()
        font_lstbx1.column("#0", minwidth=0, width=170)

        for font in font_list:  # insert all the font names to treeview
            font_lstbx1.insert('', 'end', text=font, tags=font, iid=font)
            font_lstbx1.tag_configure(font, font=(font, 10, 'normal'))

        def on_font_select(event=None):
            """Callback function when user select font"""
            font = change_entry_value(font_lstbx1, font_style)
            sample_lbl.config(font=(font, font_lstbx3.selection(), font_lstbx2.selection()))
            for style in ('normal', 'italic', 'bold'):
                font_lstbx2.tag_configure(style, font=(font, 10, style))

        font_lstbx2 = ttk.Treeview(frame2, show='tree', selectmode='browse')
        font_lstbx2.column("#0", minwidth=0, width=100)
        font_lstbx2.pack()
        for style in ('normal', 'italic', 'bold'):  # insert all the font names to treeview
            font_lstbx2.insert('', 'end', text=style.capitalize(), tags=style, iid=style)
            font_lstbx2.tag_configure(style, font=(self.font_style, 10, style))

        font_lstbx3 = ttk.Treeview(frame3, show='tree', selectmode='browse')
        font_lstbx3.column("#0", minwidth=0, width=100)

        v_scrollbar = ttk.Scrollbar(frame3, orient='vertical', command=font_lstbx3.yview)
        font_lstbx3.configure(yscrollcommand=v_scrollbar.set)
        v_scrollbar.pack(side='right', fill='y')
        font_lstbx3.pack()

        for size in range(10, 41):  # insert all the font size to treeview
            font_lstbx3.insert('', 'end', text=size, iid=size)

        # For select current font preferences
        font_lstbx1.selection_set(self.font_style)
        font_lstbx1.see(self.font_style)

        font_lstbx2.selection_set(self.font_weight)

        font_lstbx3.selection_set(self.font_size)
        font_lstbx3.see(self.font_size)

        def change_entry_value(treeview, entry):
            """Insert current selected font preference to disabled entry boxes"""
            font = treeview.item(treeview.selection()[0])['text']
            entry.config(state='normal')
            entry.delete(0, 'end')
            entry.insert(0, font)
            entry.config(state='disabled')
            return font

        def on_weight_select(event=None):
            """Callback function when user select font weight"""
            font = change_entry_value(font_lstbx2, font_weight)
            sample_lbl.config(font=(font_lstbx1.selection()[0], font_lstbx3.selection()[0], font.lower()))

        def on_size_select(event=None):
            """Callback function when user select font size"""
            size = change_entry_value(font_lstbx3, font_size)
            sample_lbl.config(font=(font_lstbx1.selection()[0], size, font_lstbx2.selection()[0]))

        l_f = ttk.LabelFrame(font_win, text='Sample')
        sample_lbl = ttk.Label(l_f, text='ABCDEF')
        sample_lbl.pack()
        l_f.grid(row=3, column=1, columnspan=2)
        font_win.grid_rowconfigure(3, minsize=100)

        def on_ok_btn_press():
            self.font_style = font_lstbx1.selection()[0]
            self.font_weight = font_lstbx2.selection()[0]
            self.font_size = int(font_lstbx3.selection()[0])
            # print(self.font_weight)
            try:
                self.customFont.config(family=self.font_style, size=self.font_size, weight=self.font_weight,
                                       slant='roman')
            except:
                self.customFont.config(family=self.font_style, size=self.font_size, slant=self.font_weight)
            # self.get_current().config(font=self.customFont)
            self.lineFont.config(size=self.font_size)
            self.pady = int(self.font_size) - 10
            self.canvas.pack_configure(pady=(self.pady, 0))
            self.canvas.update()
            font_win.destroy()

        ok_btn = ttk.Button(font_win, text='Ok', command=on_ok_btn_press)
        ok_btn.grid(row=4, column=1)
        cancel_btn = ttk.Button(font_win, text='Cancel', command=font_win.destroy)
        cancel_btn.grid(row=4, column=2)

        font_lstbx1.bind('<<TreeviewSelect>>', on_font_select)
        font_lstbx2.bind('<<TreeviewSelect>>', on_weight_select)
        font_lstbx3.bind('<<TreeviewSelect>>', on_size_select)
