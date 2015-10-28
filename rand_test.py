__author__ = 'guloo'

import random
import csv
import ntpath # ntpath.basename("a/b/c")
from tkinter import *
from tkinter import Tk
from tkinter import filedialog

"""create random files in a couple of methods"""

def go(entries, listbox_green, listbox_red):
    green_files = listbox_green.get(0, END) # a list of all the files
    red_files = listbox_red.get(0, END) # a list of all the files
    dest = entries.get() + '/'
    print("Green Files:")
    print(green_files)
    print("Red Files:")
    print(red_files)

    row_points = []
    assert len(green_files) == len(red_files)

    for i in range(len(red_files)):

        red_points = 0
        green_points = 0
        the_list = []
        headers = ""
        with open(green_files[i]) as g:
               # g = csv.reader(g, delimiter=',')
            for row in g:
                if green_points == 0:
                    headers = row
                    green_points += 1
                    continue
                row_points.append(row)
                the_list.append("green")
                green_points += 1

        with open(red_files[i]) as r:
             #   r = csv.reader(r, delimiter=',')
            for row in r:
                if red_points == 0:
                    red_points += 1
                    continue
                row_points.append(row)
                the_list.append("red")
                red_points += 1
        green_points -= 1
        red_points -= 1
        # shuffle the_list
        random.shuffle(the_list)
    #--1nd part--# random by color change

        # open to write new randomed files
        green_file_path = dest + "{}_randcol_green.csv".format(ntpath.basename(green_files[i]).split('.')[0])
        g_rand_file = open(green_file_path,"w")
        red_file_path = dest + "{}_randcol_red.csv".format(ntpath.basename(red_files[i]).split('.')[0])
        r_rand_file = open(red_file_path, "w")
        # write the headers
        g_rand_file.write(headers)
        r_rand_file.write(headers)
        # write the new files
        for j in range(len(the_list)):
            color = the_list[j]
            if color == "green": g_rand_file.write(row_points[j])
            else: r_rand_file.write(row_points[j])
        # close files
        g_rand_file.close()
        r_rand_file.close()

    #--2nd part--# random by position change

        # open to write new randomed files - random in location
        green_old = ntpath.basename(green_files[i]).split('.')[0]
        green_old.replace("green", "")
        green2_file_path = dest + "{}_randpos_green.csv".format(green_old)
        g2_rand_file = open(green2_file_path,"w")
        red_old = ntpath.basename(red_files[i]).split('.')[0]
        red_old.replace("red", "")
        red2_file_path = dest + "{}_randpos_red.csv".format(red_old)
        r2_rand_file = open(red2_file_path, "w")
        # write the headers
        g2_rand_file.write(headers)
        r2_rand_file.write(headers)
        # write the new files
        for k in range(green_points):
            line = "n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,{},{},0,n,n,n\n".format(random.randint(-20000,20000),random.randint(-20000,20000))
            g2_rand_file.write(line)
        for l in range(red_points):
            line = "n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,{},{},0,n,n,n\n".format(random.randint(-20000,20000),random.randint(-20000,20000))
            r2_rand_file.write(line)
        # close files
        g2_rand_file.close()
        r2_rand_file.close()

        # ...and that's it.
    return

fields = ('destination')




def add_files(entries, color):
    path = filedialog.askopenfilenames()
    for name in path:
        if color == 'green':
            listbox_green.insert(END, name)
        else:
            listbox_red.insert(END, name)


def choose_dest(entries):
    path = filedialog.askdirectory()
    if path != "":
       entries.delete(0, END)
       entries.insert(0,path)



if __name__ == '__main__':
   root = Tk()
   root.wm_title("Retsulc (ver 0.2) - RandomRandom clusters!")

   lab = Label(root, width=40, text="Add file, change the filter parameters and Go!", anchor='w', justify=LEFT)
   lab.pack(side=TOP)

   right_panel = Frame(root)
   left_panel = Frame(root)
   row_of_buttons = Frame(left_panel)

#left panel
   row = Frame(left_panel)
   lab = Label(row, width=22, text='Destination'+": ", anchor='w', justify=LEFT)
   ent = Entry(row)
   row.pack(side=TOP, fill=Y, padx=5, pady=5)
   lab.pack(side=LEFT)
   ent.pack(side=RIGHT, fill=X)
   b_dest = Button(left_panel, text='Choose destination', command=(lambda e=ent: choose_dest(e)))
   b_dest.pack()
#right panel
   listbox_green = Listbox(right_panel, width = 100, height = 30)
   listbox_green.pack(fill=BOTH)
   listbox_red = Listbox(right_panel, width = 100, height = 30)
   listbox_red.pack()
   listbox_red.pack()


  # low_panel = Frame(lef)
# buttons
   b_add_green = Button(row_of_buttons, text='Add green File', command=(lambda e=ent: add_files(e, 'green')))
   b_add_red = Button(row_of_buttons, text='Add red File', command=(lambda e=ent: add_files(e, 'red')))

   b_add_green.pack(side=BOTTOM, padx=5, pady=5)
   b_add_red.pack(side=BOTTOM, padx=5, pady=5)

   row_of_buttons.pack(side=BOTTOM, padx=5, pady=5)

   left_panel.pack(side = LEFT)
   right_panel.pack(side = RIGHT, expand = "yes")

   b_go = Button(left_panel, text='GO!', command=(lambda e=ent: go(e, listbox_green, listbox_red)))
   b_go.pack(side=BOTTOM, padx=5, pady=5)

   root.iconbitmap(r'blue_flower2.ico') # the icon
   root.mainloop()