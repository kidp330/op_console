import json
import requests
import tkinter as tk
import tkinter.messagebox

class user(dict):
  def __init__(self, *args, **kwargs):
    super(user, self).__init__(*args, **kwargs)

def update_data(url: str) -> list:
  try:
    data = json.loads(requests.get(url).text)
  except Exception as e:
    return []
  data = [user(d) for d in data]
  for u in data:
    u.pop('Position', None)
  return data

def list_to_img(filenames: list) -> list:
  return [tk.PhotoImage(file=fname) for fname in filenames]
def dict_to_img(filenames: dict) -> dict:
  return {key : tk.PhotoImage(file=filenames[key]) for key in filenames}

class App:
  header_labels: list
  user_labels: list = []
  # Main frame
  table: tk.Frame
  # Boolean value, used to avoid overflowing the event queue 
  # when spamming url button
  working: bool = False

  headers = ('Id', 'Name', 'Type', 'Serial Number', 'Strength', 'Battery Level', 'Working Mode')
  mapping = {'Id': 'Id',
             'Name': 'Name',
             'Type': 'Type',
             'Serial Number': 'SerialNumber',
             'SerialNumber': 'Serial Number',
             'Strength': 'Strength',
             'Battery Level': 'BatteryLevel',
             'BatteryLevel': 'Battery Level',
             'Working Mode': 'WorkingMode',
             'WorkingMode': 'Working Mode',}
  
  # These hold PhotoImage objects corresponding to their
  # respective icons
  signal_img: list = []
  battery_img: list = []
  type_img: dict = {}
  state_img: dict = {}

  # Returns list of processed and sorted user objects from json file
  # cmp used to sort users
  def load_users(self, cmp=lambda u: u['Id']) -> list:
    users = update_data(self.url)
    users.sort(key=cmp)
    return users

  # Sets up the static widgets
  def make_table(self, root):
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
    if not self.user_labels:
      return
    for row in self.user_labels:
      for l in row:
        l.destroy()

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

  # Used to fill table with user entries, reusable
  # If json request fails, leaves current table,
  # othws. clears table and refills it w/ new values
  # Return value: True if json request suceeds, False othws.
  def reload_table(self, cmp=lambda u: u['Id']) -> bool:
    users = self.load_users(cmp)
    if not users:
      return False
    self.destroy_users()
    self.place_users(users)
    self.load_icons()
    return True  

  # Places static widgets, processes image files
  # root is the tk parent widget
  def __init__(self, root):
    self.make_table(root)
    self.place_table()

    self.signal_img = list_to_img(["icons/signal/sig{}-scaled.png".format(i) for i in range(6)])
    self.battery_img = list_to_img(["icons/battery/battery{}-scaled.png".format(i) for i in range(5)])
    self.type_img = dict_to_img({key : "icons/type/{}-scaled.png".format(key) for key in ['Car', 'Portable', 'BaseStation']})
    self.state_img = dict_to_img({key : "icons/state/{}-scaled.png".format(key) for key in ['Idle', 'Voice', 'Data']})

# Subclass of tk.Entry w/ default greyed out string that clears upon
# user input
# Thanks to Reblochon Masque from https://stackoverflow.com/questions/51781651/showing-a-greyed-out-default-text-in-a-tk-entry
# for the idea
class UrlEntry(tk.Entry):
  def handle_focus_in(self, _):
    if self['fg'] == 'grey':
      self.delete(0, 'end')
    self['fg'] = 'black'
