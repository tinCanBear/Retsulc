from tkinter import *
from tkinter import Tk
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import messagebox
from parse_detect_files import go
pic_path = "openclust.jpg"
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
      if cntr == 0:
         ent.config(fg="gray")
         ent.insert(0, "Enter a name.....")
      elif cntr == 1:
         ent.insert(0, "100")
      elif cntr == 2:
         ent.insert(0, "10")
      elif cntr == 3:
         ent.insert(0, "2d")
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries[field] = ent
      cntr += 1
   return entries

if __name__ == '__main__':
   root = Tk()
   root.wm_title("Retsulc (ver 0.1) - Get clusters!")
   img = Image.open(pic_path)
   photo = ImageTk.PhotoImage(img)
   panel = Label(root, image = photo)
   panel.pack(side = "bottom", fill = "both", expand = "yes")
   ents = makeform(root, fields)
   b2 = Button(root, text='GO!', command=(lambda e=ents: gogo(e)))
   b2.pack(side=LEFT, padx=5, pady=5)
   root.mainloop()
