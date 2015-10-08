__author__ = 'UriA12'
from tkinter import *
from tkinter import Tk
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
#from clusters_filter import filter_it
pic_path = "fireworks.jpg"


fields = ('color', '#points', '#red points', '#green points', 'density', 'colocalized', 'files type', 'destination')

def go(entries):
   color = (entries['color'].get())
   points = (entries['#points'].get())
   red_points = (entries['#red points'].get())
   green_points = (entries['#green points'].get())
   density = (entries['density'].get())
   coloc = (entries['colocalized'].get())
   f_type = (entries['color'].get())
   path = "" #(entries['path'].get())
   dest_path = (entries['destination'].get())
   if path == "":
         messagebox.showinfo("Give us something to work with!", "The little people who work in this program are lost without" +
                            " some proper file paths.\nPlease help them find some files. (tip: Add Files)")
 #  filter_it(color, points, red_points, green_points, density, coloc, f_type, path, dest_path)
   messagebox.showinfo("Work here is DONE!", "If you wish choose another folder.")


def add_files(entries):
    path = filedialog.askopenfilenames()
    for name in path:
       listbox.insert(END, name)

def choose_dest(entries):
    path = filedialog.askdirectory()
    entries['destination'].insert(0,path)

def makeform(root, fields):
   entries = {}
   cntr = 0
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=22, text=field+": ", anchor='w', justify=LEFT)
      ent = Entry(row)
      if cntr == 0:
         ent = ttk.Combobox(row)
         ent['values'] = ('red', 'green', 'both')
         ent.insert(0, 'both')
      if cntr == 6:
         ent = ttk.Combobox(row)
         ent['values'] = ('pre', 'final', 'all')
         ent.insert(0, 'all')
      if cntr == 5:
         ent = ttk.Combobox(row)
         ent['values'] = ('yes', 'no', 'all')
         ent.insert(0, 'all')
      else:
         if cntr != 7 and cntr != 0 and cntr != 5 and cntr != 6:
            ent.insert(0, "MIN;MAX")

      row.pack(side=TOP, fill=Y, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, fill=X)
      entries[field] = ent
      cntr += 1
   return entries

if __name__ == '__main__':
   root = Tk()
   root.wm_title("Retsulc (ver 0.2) - Filter clusters!")

   lab = Label(root, width=40, text="Add file, change the filter parameters and Go!", anchor='w', justify=LEFT)
   lab.pack(side=TOP)

   right_panel = Frame(root)
   left_panel = Frame(root)
#left panel
   lab = Label(left_panel, width=40, text="Set the desired filters", anchor='w', justify=LEFT)
   lab.pack(side=TOP)
   img = Image.open(pic_path) # the photo
   photo = ImageTk.PhotoImage(img)
   panel = Label(left_panel, image = photo)
   panel.pack(side = "bottom", fill = "both", expand = "yes")
   ents = makeform(left_panel, fields)
   b_dest = Button(left_panel, text='Choose destination', command=(lambda e=ents: choose_dest(e)))
   b_dest.pack()
#right panel
   listbox = Listbox(right_panel, width = 100, height = 30)
   listbox.pack(fill=BOTH)

  # low_panel = Frame(lef)
# buttons
   b1 = Button(right_panel, text='Add File', command=(lambda e=ents: add_files(e)))
   b1 = Button(right_panel, text='Add File', command=(lambda e=ents: add_files(e)))

   b2 = Button(left_panel, text='GO!', command=(lambda e=ents: go(e)))
   b1.pack(side=BOTTOM, padx=5, pady=5)

   left_panel.pack(side = LEFT)
   right_panel.pack(side = RIGHT, expand = "yes")
   b2.pack(side=BOTTOM, padx=5, pady=5)

   root.iconbitmap(r'big_flower.ico') # the icon
   root.mainloop()
