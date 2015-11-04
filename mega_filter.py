__author__ = 'UriA12'
import os
import re
import time
import csv
from parse_super_detect import get_res
import numpy as np
DEBUG = False



def filter_it(color_a, points, red_points, green_points, density, coloc_a, size, files_path, dest_path, source, name):
    MAX = 1000000.
    MIN = -1.

    color = color_a
    coloc = coloc_a

    # get the source details
    tot_points = []
    tot_red = []
    tot_green = []
    with open(source, "r") as f:
        f = csv.reader(f, delimiter=',')
        next(f)
        for row in f:
            tot_points.append(int(row[1]))
            tot_red.append(int(row[2]))
            tot_green.append(int(row[3]))


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

    all_unclustered_points_per_f = []

    # open clusters file
    clusters_file = open(os.path.normcase(os.path.join(dest_path, "filtered_clusters_{}_{}.csv".format(name, time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())))), "w")
    csv_clusters_titles = "color,#points,#red points,#green points,sphere score,angle_x,angle_y,size,density,colocalized,from file\n"
    clusters_file.write(csv_clusters_titles)

    for a_file in files_path:
        if not re.findall(r".*?\.csv", a_file, re.DOTALL):
            return 1
    if dest_path == "": return 2
    for a_file in files_path:
        with open(a_file) as csvfile:
            if DEBUG: print("opened")
            points_counter = [0,0,0]
            reader = csv.DictReader(csvfile)
            for row in reader:
                str_row = ""
                if DEBUG: print(row)
                if color != "both":
                    if row['color'] != color:
                        points_counter[0] += int(row['#points'])
                        points_counter[1] += int(row['#red points'])
                        points_counter[2] += int(row['#green points'])
                        continue
                if float(row['#points']) > points_max or float(row['#points']) < points_min:
                        points_counter[0] += int(row['#points'])
                        points_counter[1] += int(row['#red points'])
                        points_counter[2] += int(row['#green points'])
                        continue
                if float(row['#red points']) > red_points_max or float(row['#red points']) < red_points_min:
                        points_counter[0] += int(row['#points'])
                        points_counter[1] += int(row['#red points'])
                        points_counter[2] += int(row['#green points'])
                        continue
                if float(row['#green points']) > green_points_max or float(row['#green points']) < green_points_min:
                        points_counter[0] += int(row['#points'])
                        points_counter[1] += int(row['#red points'])
                        points_counter[2] += int(row['#green points'])
                        continue
                if float(row['density']) > density_max or float(row['density']) < density_min:
                        points_counter[0] += int(row['#points'])
                        points_counter[1] += int(row['#red points'])
                        points_counter[2] += int(row['#green points'])
                        continue
                if coloc != "all":
                    if row['colocalized'] == '0' and coloc == 'yes':
                        points_counter[0] += int(row['#points'])
                        points_counter[1] += int(row['#red points'])
                        points_counter[2] += int(row['#green points'])
                        continue
                    if row['colocalized'] == '1' and coloc == 'no':
                        points_counter[0] += int(row['#points'])
                        points_counter[1] += int(row['#red points'])
                        points_counter[2] += int(row['#green points'])
                        continue
                if float(row['size']) > size_max or float(row['size']) < size_min:
                        points_counter[0] += int(row['#points'])
                        points_counter[1] += int(row['#red points'])
                        points_counter[2] += int(row['#green points'])
                        continue
                # if color == "green" and row['color'] == "green":  green_list_dicts.append(row)
                red_list_dicts.append(row)

                # write the cluster to the clusters file
                str_row = row['color'] + ","+\
                       row['#points'] +","+\
                       row['#red points'] +","+\
                       row['#green points'] +","+\
                       row['sphere score'] +","+\
                       row['angle_x'] +","+\
                       row['angle_y'] +","+\
                       row['size'] +","+\
                       row['density'] +","+\
                       row['colocalized'] +","+ get_name(a_file) + "\n"
                clusters_file.write(str_row)
            all_unclustered_points_per_f.append(points_counter)

    # close the clusters file
    clusters_file.close()

    xs_bin = [[],[]] # -20  red, green
    s_bin = [[],[]] # 20-300
    m_bin = [[],[]] # 300-500
    l_bin = [[],[]] # 500-

    for dic in red_list_dicts:
        this_color = dic['color']
        this_size = float(dic['size'])
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
        if this_color == "green":
            green_list.append(line)
            if this_size <= 20: xs_bin[1].append(line)
            elif this_size <=300: s_bin[1].append(line)
            elif this_size <= 500: m_bin[1].append(line)
            else: l_bin[1].append(line)

        else:
            red_list.append(line)
            if this_size <= 20: xs_bin[0].append(line)
            elif this_size <=300: s_bin[0].append(line)
            elif this_size <= 500: m_bin[0].append(line)
            else: l_bin[0].append(line)

    # total_number_of_points = b_list[0]
    # total_number_of_red_points = b_list[1]
    # total_number_of_green_points = b_list[2]
    # total_number_of_clustered_points = b_list[3]
    # total_number_of_unclustered_points = b_list[4]
    # total_number_of_clustered_red_points = b_list[5]
    # total_number_of_clustered_green_points = b_list[6]
    # relative_clustered_points = b_list[7]
    # relative_unclustered_points = b_list[8]
    # relative_red_clustered_points = b_list[9]
    # relative_green_clustered_points = b_list[10]

    n = len(tot_points)
    rel_clustered = ["NaN" for i in range(n)]
    rel_unclustered = ["NaN" for i in range(n)]
    rel_red_clust = ["NaN" for i in range(n)]
    rel_green_clust = ["NaN" for i in range(n)]
    rel_red_green = ["NaN" for i in range(n)]

    b_list = ["NaN" for i in range(12)]
    bla_list = ["NaN" for i in range(12)]

    for i in range(n):
        all_points = tot_points[i]
        all_red_points = tot_red[i]
        all_green_points = tot_green[i]
        unclustered_points = all_unclustered_points_per_f[i][0]
        unclustered_reds = all_unclustered_points_per_f[i][1]
        unclustered_greens = all_unclustered_points_per_f[i][2]
        rel_clustered[i] = float(all_points - unclustered_points)/all_points
        rel_unclustered[i] = float(unclustered_points)/all_points
        rel_red_clust[i] = float(all_red_points - unclustered_reds)/all_red_points
        rel_green_clust[i] = float(all_green_points - unclustered_greens)/all_green_points
        rel_red_green[i] = float(all_red_points)/all_green_points

    b_list[0] = np.mean(rel_red_green)
    b_list[1] = np.std(rel_red_green, ddof=1)
    b_list[2] = np.mean(rel_clustered)
    b_list[3] = np.std(rel_clustered, ddof=1)
    b_list[4] = np.mean(rel_unclustered)
    b_list[5] = np.std(rel_unclustered, ddof=1)
    b_list[6] = np.mean(rel_red_clust)
    b_list[7] = np.std(rel_red_clust, ddof=1)
    b_list[8] = np.mean(rel_green_clust)
    b_list[9] = np.std(rel_green_clust, ddof=1)
    b_list[10] = "////"

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
    xs_line = get_res(xs_bin[0], xs_bin[1], "0->20", filters, bla_list)
    s_line = get_res(s_bin[0], s_bin[1], "20->300", filters, bla_list)
    m_line = get_res(m_bin[0], m_bin[1], "300->500", filters, bla_list)
    l_line = get_res(l_bin[0], l_bin[1], "500->inf", filters, bla_list)

    out_file = open(os.path.normcase(os.path.join(dest_path, "filtered_summary_{}_{}.csv".format(name, time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())))), "w")
    csv_titles = "test#,red_green_ratio,_std,rel_clustered_pts,_std,rel_unclustered_pts,_std,rel_red_clustered,_std,rel_green_clustered,_std,----,\
    #clusters,#red clusters,#green clusters,avg green in red clusters,std green in red clusters,avg red in green clusters,\
    std red in green clusters,avg red sphericity,std red sphericity,avg green sphericity,std green sphericity,\
    avg red Xangl,std red Xangl,avg red Yangl,std red Yangl,avg green Xangl,std green Xangl,avg green Yangl,\
    std green Yangl,avg red size,std red size,avg green size,std green size,sample density,avg red density,std red density,\
    avg green density,std green density,red median size,green median size,\
    avg red pts size,std red pts size,avg green pts size,std green pts size,colocalization %green in red,colocalization %red in green,test name\n"
    out_file.write(csv_titles)
    out_file.write(avgd_line)
    out_file.write(xs_line)
    out_file.write(s_line)
    out_file.write(m_line)
    out_file.write(l_line)
    # out_file.write("#Test")
    # for i in range(n):
    #     line = ""
    out_file.close()
    return 0

    if DEBUG: print("done")


def get_name(file_name):
    """
    :param file_name: the path of the file containing the name of the test
    :param cntr:  default return if not successful
    :return: the name of the test clean of unrelevant info and file path
    """
    pre = file_name.split('/')[-2]
    name = str(0)
    if pre is not None:
        name = pre
    return name