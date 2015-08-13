__author__ = 'UriA12'
import os
import re
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
                slesh = green_name.rfind('/')
                green_str = green_name[:g]
                red_str = red_name[:r]
                if green_str == red_str:
                    if green_name.find('row') > 0:
                        if red_name.find('row') < 0:
                            continue  # do not enter loop
                    cntr += 1
                    print(cntr)
                    pre_name = get_name(green_name, cntr)
                    file_directory = main_folder + "/analysis{}".format(pre_name) + "/"
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
        print("something exists")
        for green_name in raw_green_filess:
            for red_name in raw_red_filess:
                g = max(green_name.find("green_row.csv") ,green_name.find("green_raw.csv"))  ###HERE!!!!!
                print(g)
                r = max(green_name.find("red_row.csv") ,red_name.find("red_raw.csv"))  ###HERE!!!!!
                slesh = green_name.rfind('/')
                green_str = green_name[:g]
                red_str = red_name[:r]
                if green_str == red_str:
                    cntr += 1
                    print(cntr)
                    file_directory = main_folder + "/raw_analysis{}".format(cntr) + "/"
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
    # for file in particles_filess:
    #     print(file)
    #     #main("raw_2d", epsilon, minimum_neighbors, final_green_files[i], final_red_files[i], name, final_file_directory[i])

    session_data.close()
    print("END")

def get_res(red_list, green_list, cntr):
    avg_per_green_in_red = 0.0
    red_average_sphere_score = 0.0
    red_average_angle_x = 0.0
    red_average_angle_y = 0.0
    red_average_size = 0.0
    red_avg_naive_density = 0.0

    avg_per_red_in_green = 0.0
    green_average_sphere_score = 0.0
    green_average_angle_x = 0.0
    green_average_angle_y = 0.0
    green_average_size = 0.0
    green_avg_naive_density = 0.0

    number_of_red_clusters = len(red_list)
    for line in red_list:
        break_line = line.split(",")
        avg_per_green_in_red += float(break_line[3])/(float(break_line[2]) +\
            float(break_line[3]))
        red_average_sphere_score += float(break_line[4])
        red_average_angle_x += float(break_line[5])
        red_average_angle_y += float(break_line[6])
        red_average_size += float(break_line[7])
        red_avg_naive_density += float(break_line[8])
    avg_per_green_in_red /= number_of_red_clusters
    red_average_sphere_score /= number_of_red_clusters
    red_average_angle_x /= number_of_red_clusters
    red_average_angle_y /= number_of_red_clusters
    red_average_size /= number_of_red_clusters
    red_avg_naive_density /= number_of_red_clusters


    number_of_green_clusters = len(green_list)
    for line in green_list:
        break_line = line.split(",")
        avg_per_red_in_green += float(break_line[2])/(float(break_line[3]) +\
            float(break_line[2]))
        green_average_sphere_score += float(break_line[4])
        green_average_angle_x += float(break_line[5])
        green_average_angle_y += float(break_line[6])
        green_average_size += float(break_line[7])
        green_avg_naive_density += float(break_line[8])
    avg_per_red_in_green /= number_of_green_clusters
    green_average_sphere_score /= number_of_green_clusters
    green_average_angle_x /= number_of_green_clusters
    green_average_angle_y /= number_of_green_clusters
    green_average_size /= number_of_green_clusters
    green_avg_naive_density /= number_of_green_clusters

    # write to summary file

    avgd_line = "{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(cntr\
                                                                  , avg_per_green_in_red\
                                                                  , avg_per_red_in_green\
                                                                  , red_average_sphere_score\
                                                                  , green_average_sphere_score\
                                                                  , red_average_angle_x\
                                                                  , red_average_angle_y\
                                                                  , green_average_angle_x\
                                                                  , green_average_angle_y\
                                                                  , red_average_size\
                                                                  , green_average_size\
                                                                  , red_avg_naive_density\
                                                                  , green_avg_naive_density)
    return avgd_line

def get_name(file_name, cntr):
    pre = file_name.split('/')[-1]
    pre = pre.split('\\')[-1]
    name = str(cntr)
    if pre is not None:
        pre_bott = pre.rfind("_")
        name = pre[:pre_bott]
    return name
