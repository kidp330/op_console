import json
import requests
import tkinter as tk

address = "http://localhost:8080/radios/"

root = tk.Tk()
# Don't forget to change this
root.title('Konsola Operatorska pinkman z.o.o.')
# Test on windows
root.iconphoto(False, tk.PhotoImage(file='window_icon.png'))
root.geometry('768x300')

# basically just a dict
class user(dict):
  def __init__(self, *args, **kwargs):
    super(user, self).__init__(*args, **kwargs)
  
def update_data() -> tuple:
  try:
    data = json.loads(requests.get(address).text)
  except Exception as e:
    return ([], {})
  data = [user(d) for d in data]
  coordinates = {}
  for u in data:
    if 'Position' in u:
      coordinates[u['Id']] = u['Position']
      del u['Position']
  return (data, coordinates)

def list_to_img(filenames: list) -> list:
  return [tk.PhotoImage(file=fname) for fname in filenames]
def dict_to_img(filenames: dict) -> dict:
  return {key : tk.PhotoImage(file=filenames[key]) for key in filenames}


class App:
  coordinates: dict
  header_labels: list
  user_labels: list = []
  table: tk.Frame

  headers = ('Id', 'Name', 'Type', 'Serial Number', 'Strength', 'Battery Level', 'Working Mode')
  bijection = {'Id': 'Id',
             'Name': 'Name',
             'Type': 'Type',
             'Serial Number': 'SerialNumber',
             'SerialNumber': 'Serial Number',
             'Strength': 'Strength',
             'Battery Level': 'BatteryLevel',
             'BatteryLevel': 'Battery Level',
             'Working Mode': 'WorkingMode',
             'WorkingMode': 'Working Mode',}
  

  signal_img = list_to_img(["icons/signal/sig{}-scaled.png".format(i) for i in range(6)])
  battery_img = list_to_img(["icons/battery/battery{}-scaled.png".format(i) for i in range(5)])
  type_img = dict_to_img({key : "icons/type/{}-scaled.png".format(key) for key in ['Car', 'Portable', 'BaseStation']})
  state_img = dict_to_img({key : "icons/state/{}-scaled.png".format(key) for key in ['Idle', 'Voice', 'Data']})

  def load_users(self, cmp=lambda u: u['Id']) -> list:
    (users, new_coords) = update_data()
    if new_coords:
      self.coordinates = new_coords
    users.sort(key=cmp)
    return users

  # Sets up the static widgets
  def make_table(self):
    self.table = tk.Frame(root)
    self.header_labels = [tk.Label(self.table, text=key, padx=5, pady=5) for key_idx, key in enumerate(self.headers)]

  # Places static widgets
  def place_table(self):
    self.table.grid(row=0, column=0)
    for c, l in enumerate(self.header_labels):
      l.grid(row=0, column=c)

  # Fills table with user entries, subroutine of reload_table
  def place_users(self, users: list):
    self.user_labels = [[tk.Label(self.table, text=U[key], padx=5, pady=5) for key in U] for user_idx, U in enumerate(users)]
    for r in range(len(users)):
      for c, l in enumerate(self.user_labels[r]):
        l.grid(row=r+1, column=c)
  
  # Clears user entries, subroutine of reload_table
  def destroy_users(self):
    for row in self.user_labels:
      for l in row:
        l.destroy()

  # takes cmp, a function used to sort requested users
  # clears user entries and refills it
  def reload_table(self, cmp=lambda u: u['Id']):
    users = []
    while not users:
      users = self.load_users(cmp)
    self.destroy_users()
    self.place_users(users)
    self.load_icons()

  # Changes plaintext to preprocessed icons
  def load_icons(self):
    type_col = 2
    signal_col = 4
    battery_col = 5
    state_col = 6

    for row in self.user_labels:
      row[type_col]['image'] = self.type_img[row[type_col]['text']]
      row[type_col]['text'] = ''
      slevel = int(row[signal_col]['text'])
      row[signal_col]['image'] = self.signal_img[slevel//2]
      row[signal_col]['text'] = ''
      blevel = int(row[battery_col]['text'])
      row[battery_col]['image'] = self.battery_img[blevel//25]
      row[battery_col]['text'] = '' 
      row[state_col]['image'] = self.state_img[row[state_col]['text']]
      row[state_col]['text'] = ''


  def __init__(self):
    users = self.load_users()
    self.make_table()
    self.place_table()
    self.place_users(users)
    self.load_icons()


Console = App()
current_criterion = tk.StringVar(root, Console.headers[0])

def refresh(A: App, single_use: bool) -> None:
  A.reload_table(cmp=lambda u : u[A.bijection[current_criterion.get()]])
  if not single_use:
    root.after(5000, refresh, A, single_use)

def sort_callback(*args) -> None:
  refresh(Console, single_use=True)

current_criterion.trace_add('write', sort_callback)

sortby_frame = tk.Frame(Console.table, padx=5)
sortby_frame.config(relief='groove')
print(sortby_frame.keys())
sortby_label = tk.Label(sortby_frame, text = 'Sort by: ')
sortby_menu  = tk.OptionMenu(sortby_frame, current_criterion, *Console.headers)

sortby_frame.grid(row=0, column=10, columnspan=2)
sortby_label.grid(row=0, column=10)
sortby_menu.grid(row=0, column=11)

sortby_frame.rowconfigure(0, weight=1)

refresh(Console, single_use=False)

root.mainloop()
