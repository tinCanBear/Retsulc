__author__ = 'UriA12'
import os
import re
from parse_main import main
#-----------------------FILL__INFO------------------------------------------#
def go(nam, eps, min_ngbs, d_type, pth):
    print(nam, eps, min_ngbs, d_type, pth)
    data_type = d_type # "2d", etc.
    epsilon = eps
    minimum_neighbors = min_ngbs

    final_particles_files = []
    main_folder = pth    # where all the sub_folders are at #should be session folder
    session_name = nam




    # for root, dirs, files in os.walk(main_folder, topdown=True):
    #     for name in dirs:
    #         direrctories.append(os.path.join(root, name))
    # print(direrctories)
    #
    particles_filess = []
    cntr = 0
    filess = []
    final_red_files = []
    final_green_files = []
    final_file_directory = []
    final_particles_folders = []
    green_filess = []
    red_filess = []

    for root, dirs, files in os.walk(main_folder, topdown=True):
        for name in files:
            if re.findall(r".*?green.*?.csv", name, re.DOTALL):
                green_filess.append(os.path.join(root, name))
                print("halllellellel")
            if re.findall(r".*?red.*?.csv", name, re.DOTALL):
                red_filess.append(os.path.join(root, name))
            if re.findall(r"particles.csv", name):
                if not os.path.join(root, name) in final_particles_files:
                  final_particles_files.append(os.path.join(root, name))

    session_data = open(main_folder + '/' + session_name + "_summary.csv", "w")
    session_data.write("test#, avg green in red clusters,avg red in green clusters,avg red sphericity,\
    avg green sphericity, avg red Xangl,avg red Yangl, avg green Xangl,avg green Yangl,\
    avg red size, avg green size, avg red density, avg green density\n")


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
                    file_directory = main_folder + "/analysis{}".format(cntr) + "/"
                    print(file_directory)
                    green_file_name = green_name
                    red_file_name = red_name
                    proj_name = "test_m{}".format(cntr)

                    return_list = main(data_type, epsilon, minimum_neighbors, green_file_name, red_file_name, proj_name, file_directory)

                    # average_percentage_of_points_in_clusters = 0.0

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

                    red_list = return_list[0]
                    green_list = return_list[1]

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
                    session_data.write(avgd_line)
                    print("END A FILE")

    # for file in final_particles_files:
    #     print(file)
    #     #main("raw_2d", epsilon, minimum_neighbors, final_green_files[i], final_red_files[i], name, final_file_directory[i])

    session_data.close()
    print("END")

