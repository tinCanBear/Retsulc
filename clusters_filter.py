# __author__ = 'UriA12'
# __author__ = 'UriA12'
# import os
# import re
# import time
# import statistics
# import math
# import numpy as np
# from parse_main import main
# import warnings
#
#
# debug = False
# np.seterr(all='ignore')
# warnings.filterwarnings("ignore")
# # main function, get info from "main_with_gui"
#
# def go(eps, min_ngbs,mini_eps, mini_min_ngbs, d_type, pth):
#     print(eps, min_ngbs, mini_eps, mini_min_ngbs, d_type, pth)
#     data_type = d_type # "2d", etc.
#     epsilon = eps
#     minimum_neighbors = min_ngbs
#     mini_epsilon = mini_eps
#     mini_minimum_neighbors = mini_min_ngbs
#
#     main_folder = pth    # where all the sub_folders are at #should be session folder
#     directories = []
#
#
#
#
#
#             session_data = open(os.path.normcase(os.path.join(new_directory, session_name + "_final_summary.csv")), "w")
#             session_data_pre = open(os.path.normcase(os.path.join(new_directory, session_name + "_pre_summary.csv")), "w")
#             session_data_all = open(os.path.normcase(os.path.join(new_directory, session_name + "_all_summary.csv")), "w")
#             done_file = open(os.path.normcase(os.path.join(new_directory, "done.txt")), "w")
#             csv_titles = "test#,total_number_of_points,total_number_of_red_points,total_number_of_green_points,total_number_of_clustered_points,\
#             total_number_of_unclustered_points,total_number_of_clustered_red_points,total_number_of_clustered_green_points,\
#             relative_clustered_points,relative_unclustered_points,relative_red_clustered_points,relative_green_clustered_points,\
#             #clusters,#red clusters,#green clusters,avg green in red clusters,std green in red clusters,avg red in green clusters,\
#             std red in green clusters,avg red sphericity,std red sphericity,avg green sphericity,std green sphericity,\
#             avg red Xangl,std red Xangl,avg red Yangl,std red Yangl,avg green Xangl,std green Xangl,avg green Yangl,\
#             std green Yangl,avg red size,std red size,avg green size,std green size,sample density,avg red density,std red density,\
#             avg green density,std green density,red median size,green median size,\
#             avg red pts size,std red pts size,avg green pts size,std green pts size,colocalization %green in red,colocalization %red in green,test name\n"
#
#             session_data.write(csv_titles)
#             session_data_pre.write(csv_titles)
#             session_data_all.write(csv_titles)
#             done_file.write("This folder is done with.\n")
#             done_file.close()
#         # Filtered files:
#         if len(green_filess) > 0:
#             for green_name in green_filess:
#
#
#
#
# def get_name(file_name, cntr):
#     """
#     :param file_name: the path of the file containing the name of the test
#     :param cntr:  default return if not successful
#     :return: the name of the test clean of unrelevant info and file path
#     """
#     pre = file_name.split('/')[-1]
#     pre = pre.split('\\')[-1]
#     name = str(cntr)
#     if pre is not None:
#         ind_bott = pre.rfind('_')
#         pre = pre[:ind_bott] if ind_bott != -1 else pre
#         name = pre
#     return name
#
# def get_name2(file_name, cntr):
#     """
#     :param file_name: the path of the file containing the name of the test
#     :param cntr:  default return if not successful
#     :return: the name of the test clean of unrelevant info and file path
#     """
#     pre = file_name.split('/')[-1]
#     pre = pre.split('\\')[-1]
#     name = str(cntr)
#     if pre is not None:
#         ind_bott = pre.rfind('_')
#         pre = pre[:ind_bott] if ind_bott != -1 else pre
#         if pre.rfind("green") != -1:
#             ind_bott = pre.rfind('_')
#             pre = pre[:ind_bott] if ind_bott != -1 else pre
#         name = pre
#     return name
#
# def get_name_super(folder_path):
#     pre = folder_path.split('/')[-1]
#     pre = pre.split('\\')[-1]
#     return pre
#
# def filter_it(color, points, red_points, green_points, density, coloc, f_type, path):
#     all_files = [];
#     files_type = r".*?clusters_.*?\.csv" if f_type == "all" else r".*?clusters_{}?\.csv".format(f_type)
#     for root, dirs, files in os.walk(path, topdown=True):
#         for file in files:
#             if re.findall(files_type, file, re.DOTALL):  # changed from 'r".*?green.*?.csv"'
#     directories.append(main_folder)
#     print(directories)
#     for directory in directories:
#         print(directory)
#         print(os.listdir(directory))
#         filessss = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
#         print(filessss)
#         files = [os.path.join(directory, f) for f in filessss]
#         if len(files) == 0:
#             continue
#         session_name = get_name_super(directory)
#         particles_filess = []
#         cntr = 0
#         green_filess = []
#         red_filess = []
#         raw_green_filess = []
#         raw_red_filess = []
#         old_filess = []
#
#         nrm_cntr = 0
#         raw_cntr = 0
#         prtcls_cntr = 0
#         old_cntr = 0
#         for name in files:
#             if re.findall(r".*?done\.txt", name, re.DOTALL):
#                 print("Done file found!")
#                 break
#                 green_filess.append(os.path.join(root, name))
#                 nrm_cntr += 1
#                 print("normal counter: {}".format(nrm_cntr))
#             if re.findall(r".*?red\.csv", name, re.DOTALL):  # changed from 'r".*?red.*?.csv"'
#                 red_filess.append(os.path.join(root, name))
#             if re.findall(r".*?green_r[ao]w\.csv", name, re.DOTALL):
#                 raw_green_filess.append(os.path.join(root, name))
#                 raw_cntr += 1
#                 print("raw counter: {}".format(raw_cntr))
#             if re.findall(r".*?red_r[ao]w\.csv", name, re.DOTALL):
#                 raw_red_filess.append(os.path.join(root, name))
#             # if re.findall(r".*?regions.*?\.txt", name, re.DOTALL):
#             #     old_filess.append(os.path.join(root, name))
#             # # if re.findall(r"particles\.csv", name):
#             #     if not os.path.join(root, name) in final_particles_files: # NOTICE!!! NOT SUPPORTED YET!
#             #         particles_filess.append(os.path.join(root, name))
#             #         prtcls_cntr += 1
#             #         print("particles counter: {}".format(prtcls_cntr))
#
#         if (len(green_filess) + len(raw_green_filess)) > 0:
#             new_directory = directory + "/test_{}_eps{}_min{}_{}".format(time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()), epsilon, minimum_neighbors, d_type)
#             # make output folder and open files
#             if not os.path.exists(new_directory):
#                 os.mkdir(new_directory)