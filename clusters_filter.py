__author__ = 'UriA12'
import os
import re
import time
import csv
from parse_super_detect import get_res
DEBUG = False



def filter_it(color_a, points, red_points, green_points, density, coloc_a, size, files_path, dest_path):
    MAX = 1000000.
    MIN = -1.

    color = color_a
    coloc = coloc_a
    if DEBUG: print(points)
    points_lst = points.split(";")
    if DEBUG: print(points_lst)

    points_min = MIN if points_lst[0] == 'MIN' else float(points_lst[0])
    points_max = MAX if points_lst[1] == "MAX" else float(points_lst[1])
    if DEBUG: print(red_points)

    red_points_lst = red_points.split(";")
    red_points_min = MIN if red_points_lst[0] == "MIN" else float(red_points_lst[0])
    red_points_max = MAX if red_points_lst[1] == "MAX" else float(red_points_lst[1])

    if DEBUG: print(green_points)
    green_points_lst = green_points.split(";")
    green_points_min = MIN if green_points_lst[0] == "MIN" else float(green_points_lst[0])
    green_points_max = MAX if green_points_lst[1] == "MAX" else float(green_points_lst[1])

    if DEBUG: print(density)
    density_lst = density.split(";")
    density_min = MIN if density_lst[0] == "MIN" else float(density_lst[0])
    density_max = MAX if density_lst[1] == "MAX" else float(density_lst[1])
    if DEBUG: print(size)

    size_lst = size.split(";")
    size_min = MIN if size_lst[0] == "MIN" else float(size_lst[0])
    size_max = MAX if size_lst[1] == "MAX" else float(size_lst[1])
    #
    # points_min_f = float(points_min)
    # points_max_f = float(points_max)
    #
    # red_points_min_f = float(red_points_min)
    # red_points_max_f = float(red_points_min)
    #
    # green_points_min_f = float(green_points_min)
    # green_points_max_f = float(green_points_min)
    #
    # density_min_f = float(density_min)
    # density_max_f = float(density_min)
    #
    # size_min_f = float(size_min)
    # size_max_f = float(size_max)

    red_list_dicts = []
    green_list_dicts = []
    red_list = []
    green_list = []

    for a_file in files_path:
        if not re.findall(r".*?\.csv", a_file, re.DOTALL):
            return 1
    if dest_path == "": return 2
    for a_file in files_path:
        with open(a_file) as csvfile:
            if DEBUG: print("opened")
            reader = csv.DictReader(csvfile)
            for row in reader:
                if DEBUG: print(row)
                if color != "both":
                    if row['color'] != color: continue
                if float(row['#points']) > points_max or float(row['#points']) < points_min: continue
                if float(row['#red points']) > red_points_max or float(row['#red points']) < red_points_min: continue
                if float(row['#green points']) > green_points_max or float(row['#green points']) < green_points_min: continue
                if float(row['density']) > density_max or float(row['density']) < density_min: continue
                if coloc != "all":
                    if row['colocalized'] == '0' and coloc == 'yes': continue
                    if row['colocalized'] == '1' and coloc == 'no': continue
                if float(row['size']) > size_max or float(row['size']) < size_min: continue
                if color == "green" and row['color'] == "green":  green_list_dicts.append(row)
                else: red_list_dicts.append(row)

    for dic in red_list_dicts:
        this_color = dic['color']
        line = dic['color'] + ","+\
               dic['#points'] +","+\
               dic['#red points'] +","+\
               dic['#green points'] +","+\
               dic['sphere score'] +","+\
               dic['angle_x'] +","+\
               dic['angle_y'] +","+\
               dic['size'] +","+\
               dic['density'] +","+\
               dic['colocalized'] + "\n"
        if this_color == "green": green_list.append(line)
        else: red_list.append(line)

    b_list = ["NaN" for i in range(12)]
    filters = "points@{}:{}::red_points@{}:{}::green_points@{}:{}::density@{}:{}::size@{}:{}::color@{}::colocalization@{}::".format(points_min,\
                                                                            points_max,\
                                                                            red_points_min,\
                                                                            red_points_max,\
                                                                            green_points_min,\
                                                                            green_points_max,\
                                                                            density_min,\
                                                                            density_max,\
                                                                            size_min,\
                                                                            size_max,\
                                                                            color,\
                                                                            coloc)
    avgd_line = get_res(red_list, green_list, 0, filters, b_list)

    out_file = open(os.path.normcase(os.path.join(dest_path, "filtered_summary_{}.csv".format(time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())))), "w")
    csv_titles = "test#,total_number_of_points,total_number_of_red_points,total_number_of_green_points,total_number_of_clustered_points,\
    total_number_of_unclustered_points,total_number_of_clustered_red_points,total_number_of_clustered_green_points,\
    relative_clustered_points,relative_unclustered_points,relative_red_clustered_points,relative_green_clustered_points,\
    #clusters,#red clusters,#green clusters,avg green in red clusters,std green in red clusters,avg red in green clusters,\
    std red in green clusters,avg red sphericity,std red sphericity,avg green sphericity,std green sphericity,\
    avg red Xangl,std red Xangl,avg red Yangl,std red Yangl,avg green Xangl,std green Xangl,avg green Yangl,\
    std green Yangl,avg red size,std red size,avg green size,std green size,sample density,avg red density,std red density,\
    avg green density,std green density,red median size,green median size,\
    avg red pts size,std red pts size,avg green pts size,std green pts size,colocalization %green in red,colocalization %red in green,test name\n"
    out_file.write(csv_titles)
    out_file.write(avgd_line)
    out_file.close()
    return 0

    if DEBUG: print("done")

