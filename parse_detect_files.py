__author__ = 'UriA12'
import os
import re
import statistics
import math
import numpy as np
from parse_main import main

# main function, get info from "main_with_gui"

def go(nam, eps, min_ngbs, d_type, pth):
    print(nam, eps, min_ngbs, d_type, pth)
    data_type = d_type # "2d", etc.
    epsilon = eps
    minimum_neighbors = min_ngbs

    main_folder = pth    # where all the sub_folders are at #should be session folder
    session_name = nam




    # for root, dirs, files in os.walk(main_folder, topdown=True):
    #     for name in dirs:
    #         direrctories.append(os.path.join(root, name))
    # print(direrctories)
    #
    particles_filess = []
    cntr = 0
    green_filess = []
    red_filess = []
    raw_green_filess = []
    raw_red_filess = []

    nrm_cntr = 0
    raw_cntr = 0
    prtcls_cntr = 0
    for root, dirs, files in os.walk(main_folder, topdown=True):
        for name in files:
            if re.findall(r".*?green\.csv", name, re.DOTALL):  # changed from 'r".*?green.*?.csv"'
                green_filess.append(os.path.join(root, name))
                nrm_cntr += 1
                print("normal counter: {}".format(nrm_cntr))
            if re.findall(r".*?red\.csv", name, re.DOTALL):  # changed from 'r".*?red.*?.csv"'
                red_filess.append(os.path.join(root, name))
            if re.findall(r".*?green_r[ao]w\.csv", name, re.DOTALL):
                raw_green_filess.append(os.path.join(root, name))
                raw_cntr += 1
                print("raw counter: {}".format(raw_cntr))
            if re.findall(r".*?red_r[ao]w\.csv", name, re.DOTALL):
                raw_red_filess.append(os.path.join(root, name))
            if re.findall(r"particles\.csv", name):
                if not os.path.join(root, name) in final_particles_files:
                    particles_filess.append(os.path.join(root, name))
                    prtcls_cntr += 1
                    print("particles counter: {}".format(prtcls_cntr))

    session_data = open(main_folder + '/' + session_name + "_summary.csv", "w")
    session_data.write("test#, avg green in red clusters,avg red in green clusters,avg red sphericity,\
    avg green sphericity, avg red Xangl,avg red Yangl, avg green Xangl,avg green Yangl,\
    avg red size, avg green size, avg red density, avg green density\n")

    if len(green_filess) > 0:
        for green_name in green_filess:
            for red_name in red_filess:
                g = green_name.find('green.csv')
                r = red_name.find('red.csv')
                green_str = green_name[:g]
                red_str = red_name[:r]
                if green_str == red_str:
                    cntr += 1
                    print(cntr)
                    file_directory = main_folder + "/analysis{}".format(get_name(green_name, cntr)) + "/"
                    print(file_directory)
                    green_file_name = green_name
                    red_file_name = red_name
                    proj_name = "test_m{}".format(cntr)

                    return_list = main(data_type, epsilon, minimum_neighbors, green_file_name, red_file_name, proj_name, file_directory)
                    red_list = return_list[0]
                    green_list = return_list[1]
                    avgd_line = get_res(red_list, green_list, cntr)
                    session_data.write(avgd_line)
                    print("END A FILE")
    if len(raw_green_filess) > 0:
        for green_name in raw_green_filess:
            for red_name in raw_red_filess:
                g = max(green_name.find("green_raw.csv"), green_name.find("green_row.csv"))
                r = max(red_name.find("red_raw.csv"), red_name.find("red_row.csv"))
                green_str = green_name[:g]
                red_str = red_name[:r]
                if green_str == red_str:
                    cntr += 1
                    print(cntr)
                    file_directory = main_folder + "/raw_analysis{}".format(get_name(green_name,cntr)) + "/"
                    print(file_directory)
                    green_file_name = green_name
                    red_file_name = red_name
                    proj_name = "test_m{}".format(cntr)

                    return_list = main(data_type, epsilon, minimum_neighbors, green_file_name, red_file_name, proj_name, file_directory)
                    red_list = return_list[0]
                    green_list = return_list[1]
                    avgd_line = get_res(red_list, green_list, cntr)
                    session_data.write(avgd_line)
                    print("END A FILE")

    session_data.close()
    print("END")


# ("color, #points, #red points, #green points, sphere score, angle_x, angle_y, size, density\n")
def get_res(red_list, green_list, cntr):
    len_r = len(red_list)
    len_g = len(green_list)
    for i in range(len_r):
        red_list[i] = red_list[i].split(",")[2:] # now we got: #red points, #green points, sphere score, angle_x, angle_y, size, density
        for j in range(len(red_list[i])):
            red_list[i][j] = float(red_list[i][j])
    for i in range(len_g):
        green_list[i] = green_list[i].split(",")[2:] # now we got: #red points, #green points, sphere score, angle_x, angle_y, size, density
        for j in range(len(green_list[i])):
            green_list[i][j] = float(green_list[i][j])

    # RED CLUSTERS
    g_in_r_list = []
    for a_list in red_list:
        g_in_r_list.append(a_list[1]/(a_list[0]+a_list[1]))
    avg_per_green_in_red = np.mean(g_in_r_list)
    std_per_green_in_red = statistics.stdev(g_in_r_list)

    red_average_sphere_score = np.mean(zip(*red_list)[2])
    red_std_sphere_score = statistics.stdev(zip(*red_list)[2])

    red_average_angle_x = np.mean(zip(*red_list)[3])
    red_std_angle_x = statistics.stdev(zip(*red_list)[3])

    red_average_angle_y = np.mean(zip(*red_list)[4])
    red_std_angle_y = statistics.stdev(zip(*red_list)[4])

    red_average_size = np.mean(zip(*red_list)[5])
    red_std_size = statistics.stdev(zip(*red_list)[5])

    red_avg_naive_density = np.mean(zip(*red_list)[6])
    red_std_naive_density = statistics.stdev(zip(*red_list)[6])

    # GREEN CLUSTERS
    r_in_g_list = []
    for a_list in green_list:
        r_in_g_list.append(a_list[0]/(a_list[0]+a_list[1]))
    avg_per_red_in_green = np.mean(r_in_g_list)
    std_per_red_in_green = statistics.stdev(r_in_g_list)

    green_average_sphere_score = np.mean(zip(*green_list)[2])
    green_std_sphere_score = statistics.stdev(zip(*green_list)[2])

    green_average_angle_x = np.mean(zip(*green_list)[3])
    green_std_angle_x = statistics.stdev(zip(*green_list)[3])

    green_average_angle_y = np.mean(zip(*green_list)[4])
    green_std_angle_y = statistics.stdev(zip(*green_list)[4])

    green_average_size = np.mean(zip(*green_list)[5])
    green_std_size = statistics.stdev(zip(*green_list)[5])

    green_avg_naive_density = np.mean(zip(*green_list)[6])
    green_std_naive_density = statistics.stdev(zip(*green_list)[6])

    avgd_line = "{},{},{},{},{},{},{},{},{},{},{},{},{},\
                {},{},{},{},{},{},{},{},{},{},{},{}\n".format(cntr\
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
                                                                  , red_avg_naive_density\
                                                                  , red_std_naive_density\
                                                                  , green_avg_naive_density\
                                                                  , green_std_naive_density)

    return avgd_line


def get_name(file_name, cntr):
    pre = file_name.split('/')[-1]
    pre = pre.split('\\')[-1]
    name = str(cntr)
    if pre is not None:
        ind_bott = pre.rfind('_')
        pre = pre[:ind_bott] if ind_bott != -1 else pre
        if pre.find("green") != -1:
            ind_bott = pre.rfind('_')
            pre = pre[:ind_bott] if ind_bott != -1 else pre
        name = pre
    return name

