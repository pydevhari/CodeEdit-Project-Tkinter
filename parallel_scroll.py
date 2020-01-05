from variables import Variables as v

def yview(*args):
    v.mini_map_text.yview(*args)
    v.text_area.yview(*args)

v.y_scrollbar2.config(command=yview)
v.y_scrollbar.config(command=yview)
