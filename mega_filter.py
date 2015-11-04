__author__ = 'UriA12'
import os
import re
import time
import csv
#from parse_super_detect import get_res
import numpy as np
import statistics
import math
DEBUG = False
debug=False


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
    avgd_line = get_res(red_list, green_list, 0, filters, b_list, div_by=n, div_red=n, div_green=n)
    re_line = avgd_line.split(',')
    print("n is:\t{}".format(n))
    print("re_line[12-14]:{},{},{}".format(re_line[12],re_line[13],re_line[14]))
    xs_line = get_res(xs_bin[0], xs_bin[1], "0->20", filters, bla_list, div_by = float(re_line[12])*n, div_red = float(re_line[13])*n, div_green = float(re_line[14])*n)
    s_line = get_res(s_bin[0], s_bin[1], "20->300", filters, bla_list, div_by = float(re_line[12])*n, div_red = float(re_line[13])*n, div_green = float(re_line[14])*n)
    m_line = get_res(m_bin[0], m_bin[1], "300->500", filters, bla_list, div_by = float(re_line[12])*n, div_red = float(re_line[13])*n, div_green = float(re_line[14])*n)
    l_line = get_res(l_bin[0], l_bin[1], "500->inf", filters, bla_list, div_by = float(re_line[12])*n, div_red = float(re_line[13])*n, div_green = float(re_line[14])*n)

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

# ("color, #points, #red points, #green points, sphere score, angle_x, angle_y, size, density\n")
def get_res(red_list, green_list, cntr, proj_name, b_list, div_by=1, div_red=1, div_green=1):
    len_r = len(red_list)
    len_g = len(green_list)

    for i in range(len_r):
        red_list[i] = red_list[i].split(",")[1:] # now we got:#points,  #red points, #green points, sphere score, angle_x, angle_y, size, density
        for j in range(len(red_list[i])):
            red_list[i][j] = float(red_list[i][j])
    for i in range(len_g):
        green_list[i] = green_list[i].split(",")[1:] # now we got:#points,  #red points, #green points, sphere score, angle_x, angle_y, size, density
        for j in range(len(green_list[i])):
            green_list[i][j] = float(green_list[i][j])

    # RED CLUSTERS
    g_in_r_list = []
    for a_list in red_list:
        g_in_r_list.append(a_list[2]/(a_list[1]+a_list[2]))
    # if len(g_in_r_list) < 2:
    #     avgd_line = "{},N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N\n".format(cntr)
    #     return avgd_line

    avg_per_green_in_red = np.mean(g_in_r_list) if len(g_in_r_list) > 2 else 0
    std_per_green_in_red = statistics.stdev(g_in_r_list) if len(g_in_r_list) > 2 else 0

    # Easier handling numpy arrays
    red_array = np.array(red_list)
    # print if in DEBUG:
    if debug:
        print(red_array)
    red_means = np.mean(red_array, axis=0)
    red_check = True if red_array.size else False # True if check is good
    if debug:
        print(red_means)

    red_stds = np.std(red_array, ddof=1, axis=0)
    red_medians = np.median(red_array, axis = 0)
    # Sphere score
    red_average_sphere_score = red_means[3] if red_check else 0
    red_std_sphere_score = red_stds[3] if red_check else 0
    # X angle
    red_average_angle_x = red_means[4] if red_check else 0
    red_std_angle_x = red_stds[4] if red_check else 0
    # Y angle
    red_average_angle_y = red_means[5] if red_check else 0
    red_std_angle_y = red_stds[5] if red_check else 0
    # Size
    red_average_size = red_means[6] if red_check else 0
    red_std_size = red_stds[6] if red_check else 0
    # Density
    red_avg_naive_density = red_means[7] if red_check else 0
    red_std_naive_density = red_stds[7] if red_check else 0
    # median Size
    red_average_med_size = red_medians[6] if red_check else 0
    # size  in points
    red_avg_size_pts = red_means[0] if red_check else 0
    red_std_size_pts = red_stds[0] if red_check else 0
    # colocalization percentage
    sum_of_coloc_r = np.sum(red_array[:,8]) if len(red_array) > 7 else 0
    per_g_in_r_col = sum_of_coloc_r/len(red_array) if len(red_array) > 0 else 0

    # GREEN CLUSTERS
    r_in_g_list = []
    for a_list in green_list:
        r_in_g_list.append(a_list[1]/(a_list[1]+a_list[2]))
    # if len(r_in_g_list) < 2:
    #     avgd_line = "{},N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N\n".format(cntr)
    #     return avgd_line

    avg_per_red_in_green = np.mean(r_in_g_list) if len(r_in_g_list) > 2 else 0
    std_per_red_in_green = statistics.stdev(r_in_g_list) if len(r_in_g_list) > 2 else 0

    # Transform to numpy
    green_array = np.array(green_list)
    green_means = np.mean(green_array, axis=0)   # calculates the avg of all the columns of the array
    green_check = True if green_array.size else False # True if check is good

    green_stds = np.std(green_array, ddof=1, axis=0)  # calculates the std (sample; ddof =1) of all the columns of the array
    green_medians = np.median(green_array, axis=0)
    # Sphere score
    green_average_sphere_score = green_means[3] if green_check else 0
    green_std_sphere_score = green_stds[3] if green_check else 0
    # X angle
    green_average_angle_x = green_means[4] if green_check else 0
    green_std_angle_x = green_stds[4] if green_check else 0
    # Y angle
    green_average_angle_y = green_means[5] if green_check else 0
    green_std_angle_y = green_stds[5] if green_check else 0
    # Size
    green_average_size = green_means[6] if green_check else 0
    green_std_size = green_stds[6] if green_check else 0
    # Density
    green_avg_naive_density = green_means[7] if green_check else 0
    green_std_naive_density = green_stds[7] if green_check else 0
    # median Size
    green_average_med_size = green_medians[6] if green_check else 0
    # size  in points
    green_avg_size_pts = green_means[0] if green_check else 0
    green_std_size_pts = green_stds[0] if green_check else 0
    sum_of_coloc_g = np.sum(green_array[:,8]) if len(green_array) > 7 else 0
    per_r_in_g_col = sum_of_coloc_g/len(green_array) if len(green_array) > 0 else 0

    # How many clusters?
    number_red = len(red_list)/div_red
    number_green = len(green_list)/div_green
    total_clusters = (len(red_list) + len(green_list))/div_by

    # Sample density
    sample_size = float(2000*2000) # this is for 2d
    clstrs_tot = 0
    if green_array != []:
        for clst_size in green_array[:,6]: # the 'size' column of the array
            clstrs_tot += clst_size*(math.pi)
    if red_array != []:
        for clst_size in red_array[:,6]: # the 'size' column of the array
            clstrs_tot += clst_size*(math.pi)
    clstrs_tot /= sample_size # should be the sample density

    # basics stuff
    total_number_of_points = b_list[0]
    total_number_of_red_points = b_list[1]
    total_number_of_green_points = b_list[2]
    total_number_of_clustered_points = b_list[3]
    total_number_of_unclustered_points = b_list[4]
    total_number_of_clustered_red_points = b_list[5]
    total_number_of_clustered_green_points = b_list[6]
    relative_clustered_points = b_list[7]
    relative_unclustered_points = b_list[8]
    relative_red_clustered_points = b_list[9]
    relative_green_clustered_points = b_list[10]

    # create the line to be written to .csv file
    avgd_line = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},\
                {},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(cntr\
                                                                  , total_number_of_points\
                                                                  , total_number_of_red_points\
                                                                  , total_number_of_green_points\
                                                                  , total_number_of_clustered_points\
                                                                  , total_number_of_unclustered_points\
                                                                  , total_number_of_clustered_red_points\
                                                                  , total_number_of_clustered_green_points\
                                                                  , relative_clustered_points\
                                                                  , relative_unclustered_points\
                                                                  , relative_red_clustered_points\
                                                                  , relative_green_clustered_points\
                                                                  , total_clusters\
                                                                  , number_red\
                                                                  , number_green\
                                                                  , avg_per_green_in_red\
                                                                  , std_per_green_in_red\
                                                                  , avg_per_red_in_green\
                                                                  , std_per_red_in_green\
                                                                  , red_average_sphere_score\
                                                                  , red_std_sphere_score\
                                                                  , green_average_sphere_score\
                                                                  , green_std_sphere_score\
                                                                  , red_average_angle_x\
                                                                  , red_std_angle_x\
                                                                  , red_average_angle_y\
                                                                  , red_std_angle_y\
                                                                  , green_average_angle_x\
                                                                  , green_std_angle_x\
                                                                  , green_average_angle_y\
                                                                  , green_std_angle_y\
                                                                  , red_average_size\
                                                                  , red_std_size\
                                                                  , green_average_size\
                                                                  , green_std_size\
                                                                  , clstrs_tot\
                                                                  , red_avg_naive_density\
                                                                  , red_std_naive_density\
                                                                  , green_avg_naive_density\
                                                                  , green_std_naive_density\
                                                                  , red_average_med_size\
                                                                  , green_average_med_size\
                                                                  , red_avg_size_pts\
                                                                  , red_std_size_pts\
                                                                  , green_avg_size_pts\
                                                                  , green_std_size_pts\
                                                                  , per_g_in_r_col\
                                                                  , per_r_in_g_col\
                                                                  , proj_name)


    return avgd_line
