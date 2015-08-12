from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from parse_detect_files import go

fields = ('Session Name', 'Epsilon', 'Minimum Neighbors', 'Data Type')
def gogo(entries):
   name = (entries['Session Name'].get())
   epsilon = (int(entries['Epsilon'].get()))
   min_neighbors = (int(entries['Minimum Neighbors'].get()))
   d_type = (entries['Data Type'].get())
   path = filedialog.askdirectory()
   print(path)
   messagebox.showinfo("Work in progress", "Please wait till' it's done... You'll get a message (for now just click OK).")
   go(name, epsilon, min_neighbors, d_type, path)
   messagebox.showinfo("Work is DONE!", "You may now enter another session folder.")

def makeform(root, fields):
   entries = {}
   cntr = 0
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=22, text=field+": ", anchor='w')
      ent = Entry(row)
      ent.insert(0,"0")
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries[field] = ent
      cntr += 1
   return entries

if __name__ == '__main__':
   root = Tk()
   ents = makeform(root, fields)
   b2 = Button(root, text='GO!', command=(lambda e=ents: gogo(e)))
   b2.pack(side=LEFT, padx=5, pady=5)
   root.mainloop()