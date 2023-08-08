import tkinter as tk

parent = tk.Tk()

menubar = tk.Menu(parent)
show_all = tk.BooleanVar()
show_all.set(True)
show_done = tk.BooleanVar()
show_not_done = tk.BooleanVar()

view_menu = tk.Menu(menubar)
view_menu.add_checkbutton(label="Show All", onvalue=1, offvalue=0, variable=show_all)
view_menu.add_checkbutton(label="Show Done", onvalue=1, offvalue=0, variable=show_done)
view_menu.add_checkbutton(label="Show Not Done", onvalue=1, offvalue=0, variable=show_not_done)
menubar.add_cascade(label='View', menu=view_menu)
parent.config(menu=menubar)

parent.mainloop()