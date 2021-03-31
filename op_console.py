import json
import requests
import tkinter as tk
import tkinter.messagebox
from godclass_n_aux import *

# address = "http://localhost:8080/radios/"

root = tk.Tk()
root.title('Konsola Operatorska Pinkman Inc')
root.iconphoto(False, tk.PhotoImage(file='icons/window/window.png'))
root.geometry('835x300')

# Object with internal methods for refreshing user entries
# and processing icons
Console = App(root)
# stringvar holding current sorting criterion
current_criterion = tk.StringVar(root, Console.headers[0])
# frame holding sorting and entrybox elements
controls = tk.Frame(Console.table, padx=5)

sort_frame = tk.Frame(controls)
entry_frame = tk.Frame(controls)

sortby_label = tk.Label(sort_frame, text = 'Sort by: ')
sortby_menu  = tk.OptionMenu(sort_frame, current_criterion, *Console.headers)
# By default sorting disabled until data is fetched
sortby_menu['state'] = 'disabled'

# entrybox using custom class that changes foreground colour on focus
url_entry = UrlEntry(entry_frame, fg='grey')
url_entry.insert(tk.END, 'Your url address')
url_entry.bind("<FocusIn>", url_entry.handle_focus_in)

url_button = tk.Button(entry_frame, text='Get user list')

# Function calls reload_table and handles failed json requests
# to avoid multiple refresh() threads
def refresh(A: App, single_use: bool) -> None:
  succeeded = A.reload_table(cmp=lambda u : u[A.mapping[current_criterion.get()]])
  if not succeeded:
    Console.working = False
    single_use = True
    sortby_menu['state'] = 'disabled'
    tkinter.messagebox.showwarning(title='Error', message='Failed to fetch users from given url, please try again.')
  if not single_use and Console.working:
    root.after(5000, refresh, A, single_use)

# Single reload on changing sorting criterion
def sort_callback(*args) -> None:
  refresh(Console, single_use=True)

# 'Get user list' callback
def get_url() -> None:
  Console.url = url_entry.get()
  single_use = Console.working
  Console.working = True
  sortby_menu['state'] = 'normal'
  refresh(Console, single_use=single_use)

# adds tracer that calls sort_callback() anytime current_criterion changes value
current_criterion.trace_add('write', sort_callback)
# assigning get_url() to url_button
url_button['command'] = get_url

# Placing controls widgets
controls.grid(row=0, column=10, rowspan=2, columnspan=2)
sort_frame.grid(row=0, column=10, columnspan=2)
entry_frame.grid(row=1, column=10, columnspan=2)
sortby_label.grid(row=0, column=10)
sortby_menu.grid(row=0, column=11)
url_entry.grid(row=1, column=10)
url_button.grid(row=1, column=11)

root.mainloop()
