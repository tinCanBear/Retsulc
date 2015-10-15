__author__ = 'UriA12'
__author__ = 'UriA12'
from tkinter import *
from tkinter import Tk
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import csv
import os
import math
import time
DEBUG = False
import numpy as np
pic_path = "fornax.jpg"

sample_length = 20000.0
fields = ('t', 'destination')

def dist(p1, p2):
    a = (p1[0] - p2[0])**2
    b = (p1[1] - p2[1])**2
    return math.sqrt(a+b)

def rip_it(the_t, files_path, dest_path):
    t = int(the_t)
    list_of_all_points_a = []
    out_file = open(os.path.normcase(os.path.join(dest_path, "ripleys_t_{}_{}.csv".format(t, time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())))), "w")
    csv_titles = "color,total_number_of_points,t,Ripleys_K,Ripleys_L,file_name\n"
    out_file.write(csv_titles)
    cnt = 0
    for a_file in files_path:
        points_a = []
        with open(a_file) as f:
            color_green = "green" if re.findall(r".*?green\.csv", a_file, re.DOTALL) or re.findall(r".*?green_r[ao]w\.csv", a_file, re.DOTALL)\
                else "red"
            f = csv.reader(f, delimiter=',')
            next(f, None)  # skip the headers
            f_cnt = 0
            for row in f:
                p = (float(row[16]), float(row[17]))
                points_a.append(p)
                list_of_all_points_a.append(p)
                f_cnt += 1
                cnt += 1
            points = np.array(points_a)
            rip_cnt = 0
            n = len(points)
            inv_avg = (sample_length**2)/n
            for i in range(n):
                if DEBUG and i%1000 == 0: print("The color is {} and the i is:\t{}".format(color_green, i))
                for j in range(n):
                    if i >= j: continue
                    elif math.hypot(points[i][0] - points[j][0], points[i][1] - points[j][1]) < t:
                            rip_cnt += 1
            rip_k_estim = inv_avg*(rip_cnt/n)
            rip_l_estim = math.sqrt(rip_k_estim/math.pi)
            out_file.write("{},{},{},{},{},{}\n".format(color_green, n, t, rip_k_estim, rip_l_estim, a_file))
    list_of_all_points = np.array(list_of_all_points_a)
    rip_cnt = 0
    n = len(list_of_all_points)
    inv_avg = (sample_length**2)/n
    for i in range(n):
        if DEBUG and i%500 == 0: print("The color is \"all\" and the i is:\t{}".format(i))
        for j in range(n):
            if i >= j: continue
            elif math.hypot(list_of_all_points[i][0] - list_of_all_points[j][0], list_of_all_points[i][1] - list_of_all_points[j][1]) < t:
                rip_cnt += 1
    rip_k_estim = inv_avg*(rip_cnt/n)
    rip_l_estim = math.sqrt(rip_k_estim/math.pi)
    out_file.write("{},{},{},{},{},{}\n".format("all", n, t, rip_k_estim, rip_l_estim, a_file))
    out_file.close()
    return 0






def go(entries, listbox):
   files_path = listbox.get(0, END) # a list of all the files
   the_t = (entries['t'].get())
   dest_path = (entries['destination'].get())
   print(files_path)
   if len(files_path) == 0:
        messagebox.showinfo("Give us something to work with!", "The little people who work in this program are lost without" +
                            " some proper file paths.\nPlease help them find some files. (tip: Add Files)")
   result = rip_it(the_t, files_path, dest_path)
   if result == 0:
      listbox.delete(0, END)
      messagebox.showinfo("Work here is DONE!",\
          "If you wish choose another folder.")
   elif result == 1:
      messagebox.showinfo("You tried to trick us!",\
          "One or more of the files you selected isn't a \".csv\" file.\nChoose again (more carefully).\nThanks,\n\tThe little people.")
   elif result == 2:
      messagebox.showinfo("Nowhere to put it!",\
          "You didn't provide a destination for the little people's work.\nThey won't work for nothing! (tip: add a destination folder)")


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
      row.pack(side=TOP, fill=Y, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, fill=X)
      entries[field] = ent
      cntr += 1
   return entries

if __name__ == '__main__':
   root = Tk()
   root.wm_title("Retsulc (ver 0.2) - Rip(leys) it!")

   lab = Label(root, width=40, text="Add file/s and Go!", anchor='w', justify=LEFT)
   lab.pack(side=TOP)

   right_panel = Frame(root)
   left_panel = Frame(root)
   row_of_buttons = Frame(right_panel)

#left panel
   lab = Label(left_panel, width=40, text="Choose a destination", anchor='w', justify=LEFT)
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
   b_add = Button(row_of_buttons, text='Add File', command=(lambda e=ents: add_files(e)))
   b_delete = Button(row_of_buttons, text="Remove Selected",command=lambda lb=listbox: lb.delete(ANCHOR))
   b_add.pack(side=RIGHT, padx=5, pady=5)
   b_delete.pack(side=LEFT, padx=5, pady=5)
   row_of_buttons.pack(side=BOTTOM, padx=5, pady=5)
   left_panel.pack(side = LEFT)
   right_panel.pack(side = RIGHT, expand = "yes")

   b_go = Button(left_panel, text='GO!', command=(lambda e=ents: go(e, listbox)))
   b_go.pack(side=BOTTOM, padx=5, pady=5)

   root.iconbitmap(r'blue_flower2.ico') # the icon
   root.mainloop()

