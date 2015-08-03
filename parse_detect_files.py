__author__ = 'UriA12'
import os
import re
from parse_main import main
#-----------------------FILL__INFO------------------------------------------#
data_type = "2d"
epsilon = 100
minimum_neighbors = 10
final_particles_files = []
main_folder = "D:/Gilad/new_data/"    # where all the sub_folders are at
direrctories = []
for root, dirs, files in os.walk(main_folder, topdown=True):
    for name in dirs:
        direrctories.append(os.path.join(root, name))
print(direrctories)

particles_filess = []
for director in direrctories:
    cntr = 0
    filess = []
    final_red_files = []
    final_green_files = []
    final_file_directory = []
    final_particles_folders = []
    green_filess = []
    red_filess = []

    for root, dirs, files in os.walk(director, topdown=True):

        for name in files:
            if re.findall(r".*?green.*?.csv", name, re.DOTALL):
                green_filess.append(os.path.join(root, name))
            if re.findall(r".*?red.*?.csv", name, re.DOTALL):
                red_filess.append(os.path.join(root, name))
            if re.findall(r"particles.csv", name):
                if not os.path.join(root, name) in final_particles_files:
                  final_particles_files.append(os.path.join(root, name))
        if len(green_filess) > 0:
            for green_name in green_filess:
                for red_name in red_filess:
                    g = green_name.find('green')
                    r = red_name.find('red')
                    slesh = green_name.rfind('/')
                    green_str = green_name[:g]
                    red_str = red_name[:r]
                    if green_str == red_str:
                        if green_name.find('row') > 0:
                            if red_name.find('row') < 0:
                                continue  # do not enter loop
                        cntr += 1
                        print(cntr)
                        file_directory = director + "/analysis{}".format(cntr) + "/"
                        final_file_directory.append(file_directory)
                        print(file_directory)
                        green_file_name = green_name
                        red_file_name = red_name
                        if not green_file_name in final_green_files:
                            final_green_files.append(green_file_name)
                        if not red_file_name in final_red_files:
                            final_red_files.append(red_file_name)
                        name = "test1"
        for i in range(len(final_green_files)):
            print(final_green_files[i])
            main(data_type, epsilon, minimum_neighbors, final_green_files[i], final_red_files[i], name, final_file_directory[i])

        for file in final_particles_files:
            print(file)
            #main("raw_2d", epsilon, minimum_neighbors, final_green_files[i], final_red_files[i], name, final_file_directory[i])

