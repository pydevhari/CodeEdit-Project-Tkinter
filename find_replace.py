import tkinter as tk
from tkinter import ttk
from all_functions import Methods


class Find(Methods):
    """Perform find/search related operation"""
    def search_words(self, event=None, findword=None, chkbtn1=None,
                     chkbtn2=None, label=None, replaceword=None):
        """Main search logic method for both Find and Replace class"""
        text_area = self.get_current()  # object of the current tabs's text widget
        text_area.tag_delete('highlight', "1.0", 'end')
        if chkbtn1.instate(['selected']):  # return True if check button is selected otherwise False
            check_case = 0  # search will case sensitive
        else:
            check_case = 1  # search will not case sensitive
        if chkbtn2.instate(['selected']):
            pattern = rf'\y{findword}\y'  # match the exact word using regular expression
        else:
            pattern = findword
        start_index = "1.0"
        match = 0
        while True:
            countVar = tk.IntVar()
            start_index = text_area.search(pattern, start_index, 'end', count=countVar, nocase=check_case,
                                           regexp=True)
            if start_index:
                end_index = text_area.index('%s+%dc' % (start_index, countVar.get()))
                text_area.tag_add('highlight', start_index,
                                  '%s+%dc' % (start_index, countVar.get()))  # add tag to k
                text_area.tag_config('highlight', background='yellow', foreground='red')  # and color it with v
                if countVar.get() == 0:
                    break
                else:
                    if replaceword:
                        text_area.replace(start_index, '%s+%dc' % (start_index, countVar.get()), replaceword)
                    start_index = end_index
                    text_area.see('%s+%dc' % (start_index, countVar.get()))
                    match += 1
            else:
                break
        label.config(text=f'Matches Found: {match}')
        return match

    def find(self, event=None, replace=False, words=None):
        """Method for find/search words in the current tab's text area"""
        find_win = tk.Tk()
        w = 600
        h = 200
        ws = find_win.winfo_screenwidth()
        hs = find_win.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        find_win.geometry(f"{w}x{h}+{int(x)}+{int(y)}")  # set the window in center of the screen
        find_win.resizable(0, 0)
        find_win.title("Find")
        f_entry = ttk.Entry(find_win, width=50)
        f_entry.pack()

        chk_btn = ttk.Checkbutton(find_win, text='Match Case')
        chk_btn.pack()
        chk_btn.invoke()  # check
        chk_btn.invoke()  # uncheck

        chk_btn2 = ttk.Checkbutton(find_win, text='Match Exact Word')
        chk_btn2.pack()
        chk_btn2.invoke()
        chk_btn2.invoke()

        match_lbl = ttk.Label(find_win, text='Matches Found -')
        match_lbl.pack()

        try:
            txt = self.get_current().selection_get()  # get the selected text[if available] from text widget
            f_entry.insert(0, txt)  # insert the selected text to search box
            f_entry.event_generate('<<SelectAll>>')
        except:
            pass

        def on_checkbtn_select():
            self.search_words(findword=f_entry.get(), chkbtn1=chk_btn, chkbtn2=chk_btn2, label=match_lbl)

        chk_btn.config(command=on_checkbtn_select)
        chk_btn2.config(command=on_checkbtn_select)
        f_entry.focus_force()

        def search(event=None):
            self.search_words(findword=f_entry.get(), chkbtn1=chk_btn, chkbtn2=chk_btn2, label=match_lbl)

        find_win.bind('<KeyPress>', search)
        search()
        find_win.mainloop()


class Replace(Find):
    """Perform replace operation"""
    def replace(self, event=None):
        """Replace the matched word(s)"""
        replace_win = tk.Tk()
        w = 600
        h = 200
        ws = replace_win.winfo_screenwidth()
        hs = replace_win.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        replace_win.geometry(f"{w}x{h}+{int(x)}+{int(y)}")  # set the window in center of the screen
        replace_win.resizable(0, 0)
        replace_win.title("Find")
        f_entry = ttk.Entry(replace_win, width=50)
        f_entry.pack()

        chk_btn = ttk.Checkbutton(replace_win, text='Match Case')
        chk_btn.pack()
        chk_btn.invoke()  # check
        chk_btn.invoke()  # uncheck

        chk_btn2 = ttk.Checkbutton(replace_win, text='Match Exact Word')
        chk_btn2.pack()
        chk_btn2.invoke()
        chk_btn2.invoke()

        try:
            txt = self.get_current().selection_get()  # get the selected text[if available] from text widget
            f_entry.insert(0, txt)  # insert the selected text to search box
            f_entry.event_generate('<<SelectAll>>')
        except:
            pass

        match_lbl = tk.Label(replace_win, text='Matches Found -')
        match_lbl.pack()

        r_entry = ttk.Entry(replace_win, width=50)
        r_entry.pack()

        def replace_words():
            match = self.search_words(findword=f_entry.get(), chkbtn1=chk_btn,
                                      chkbtn2=chk_btn2, label=match_lbl)
            if match:
                self.search_words(findword=f_entry.get(), chkbtn1=chk_btn,
                                  chkbtn2=chk_btn2, label=match_lbl,
                                  replaceword=r_entry.get())

        r_btn = ttk.Button(replace_win, text='Replace', command=replace_words)
        r_btn.pack()

        f_entry.focus_force()

        def search(event=None):
            self.search_words(findword=f_entry.get(), chkbtn1=chk_btn, chkbtn2=chk_btn2, label=match_lbl)

        def on_checkbtn_select():
            self.search_words(findword=f_entry.get(), chkbtn1=chk_btn, chkbtn2=chk_btn2, label=match_lbl)

        chk_btn.config(command=on_checkbtn_select)
        chk_btn2.config(command=on_checkbtn_select)

        replace_win.bind('<KeyPress>', search)
        search()
        replace_win.mainloop()
