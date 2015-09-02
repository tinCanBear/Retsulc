from __future__ import print_function
import os
from classes import *
from show import *
import numpy as np
from sklearn.cluster import DBSCAN

def main(data_type, epsilon, minimum_neighbors, green_name, red_name, proj_name, file_dir):
    green_file_name = green_name
    red_file_name = red_name
    name = proj_name
    clusters_file = "clusters_" + name
    remarks = "....."
    file_directory = file_dir
    #------------------------$$$$$$$$$$$----------------------------------------#
    if data_type != "3d" and data_type != "raw_3d":
        dimension = 2
    else:
        dimension = 3

    ##               !!!!FROM HERE: DO NOT TOUCH!!!!                           ##

    s = Sample(green_file_name,red_file_name, epsilon = epsilon, min_n = minimum_neighbors, path=file_directory, \
               data_type=data_type, name=name)


    s.get_points(s.data_type)

    # prepare samples

    all_points = np.array(s.points_dbscan)

    red_points = np.array(s.red_points_dbscan)

    green_points = np.array(s.green_points_dbscan)


    # Compute DBSCAN

        # both prots

    db = DBSCAN(eps = s.epsilon, min_samples = s.min_n).fit(all_points)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

        # just green

    db_g = DBSCAN(eps = s.epsilon, min_samples = s.min_n).fit(green_points)
    core_samples_mask_g = np.zeros_like(db_g.labels_, dtype=bool)
    core_samples_mask_g[db_g.core_sample_indices_] = True
    g_labels = db_g.labels_

        # just red

    db_r = DBSCAN(eps = s.epsilon, min_samples = s.min_n).fit(red_points)
    core_samples_mask_r = np.zeros_like(db_r.labels_, dtype=bool)
    core_samples_mask_r[db_r.core_sample_indices_] = True
    r_labels = db_r.labels_

        # assign labels
    s.labels = labels
    s.green_labels = g_labels
    s.red_labels = r_labels

    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    ng_clusters_ = len(set(g_labels)) - (1 if -1 in g_labels else 0)
    nr_clusters_ = len(set(r_labels)) - (1 if -1 in r_labels else 0)
    s.clusters = [Cluster() for i in range(n_clusters_)]
    s.green_clusters = [Cluster() for i in range(ng_clusters_)]
    s.red_clusters = [Cluster() for i in range(nr_clusters_)]

        # assign points to clusters

    for i in range(len(labels)):
        if labels[i] != -1:
            s.clusters[labels[i]].add_point(s.points[i])
            s.points[i].cluster = labels[i]


    for k in range(len(g_labels)):
        if g_labels[k] != -1:
            s.green_clusters[g_labels[k]].add_point(s.green_points[k])
            s.green_points[k].green_cluster = g_labels[k]
            s.clustered_points.append(s.green_points[k])
        else:
            s.unclustered_points.append(s.green_points[k])

    for j in range(len(r_labels)):
        if r_labels[j] != -1:
            s.red_clusters[r_labels[j]].add_point(s.red_points[j])
            s.red_points[j].red_cluster = r_labels[j]
            s.clustered_points.append(s.red_points[j])

        else:
            s.unclustered_points.append(s.red_points[j])

    # make output folder
    if not os.path.exists(file_directory):
        os.mkdir(file_directory)

    s.f = open(file_directory + name + "_summary.txt", "w")
    s.f_clusters = open(file_directory + clusters_file + ".csv", "w")
    s.f_csv = open(file_directory + name + ".csv", "w")
    s.print_f("the green file is: \n", s.f)
    s.print_f(green_file_name + "\n", s.f)
    s.print_f("the red file is: \n", s.f)
    s.print_f(red_file_name + "\n", s.f)

    s.points_summary()

    # PCA analysis

    s.green_clusters = [x for x in s.green_clusters if len(x.points) > 3] # dillute small clusters
    s.red_clusters = [x for x in s.red_clusters if len(x.points) > 3] # (because they can cause problems in pca)

    for i in s.green_clusters:
        i.pca_analysis(dimension)
    for j in s.red_clusters:
        j.pca_analysis(dimension)

    # plot k-distances

    plot_knn(s.green_points_dbscan, file_directory, "kdist_green")
    plot_knn(s.red_points_dbscan, file_directory, "kdist_red")

    # make rainbow pic.
    rainbow(s)

    s.print_f("\n\n-----------------END OF PART I------------------------\n\n", s.f)

    added_points = []
    s.print_f("Checking for green presence in red clusters and vice versa...\n\n", s.f)

    for red_cluster in s.red_clusters:
        for gp in s.green_points:
            if dist(gp.point,red_cluster.center)<red_cluster.large_diameter:
                red_cluster.points.append(gp)
                added_points.append(gp)
                red_cluster.is_mixed = True
                gp.opposite_clusters += 1


    for green_cluster in s.green_clusters:
        for rp in s.red_points:
            if dist(rp.point,green_cluster.center)<green_cluster.large_diameter:
                green_cluster.points.append(rp)
                added_points.append(rp)
                green_cluster.is_mixed = True
                rp.opposite_clusters += 1

    reds = [c for c in s.red_clusters if c.is_mixed is True]
    greens = [c for c in s.green_clusters if c.is_mixed is True]

    p_green_clstrs_with_red_points = float(len(greens))*100/len(s.green_clusters)
    p_red_clstrs_with_green_points = float(len(reds))*100/len(s.red_clusters)

    red_5 = []
    red_10 = []
    green_in_red_total = 0 # the total of green points in red clusters

    for red in reds:
         cntr = 0
         for point in red.points:
             if point.color == "green":
                 cntr += 1
         if cntr > 3:
            red_5.append(red)
            if cntr > 6:
                red_10.append(red)
         green_in_red_total += cntr

    green_5 = []
    green_10 = []
    red_in_green_total = 0 # the total of red points in green clusters
    for green in greens:
         cntr = 0
         for point in green.points:
             if point.color == "red":
                 cntr += 1
         if cntr > 3:
            green_5.append(green)
            if cntr > 6:
                green_10.append(green)
         red_in_green_total += cntr

    avg_green_in_red = float(green_in_red_total)/len(s.red_clusters)
    avg_red_in_green = float(red_in_green_total)/len(s.green_clusters)
    s.print_f("\n_______green clusters__vs.__red points____________\n\n", s.f)
    s.print_f("The average number of red points in a green cluster is: {} \n".format(avg_red_in_green), s.f)
    s.print_f("The total number of red points in green clusters: {} \n".format(red_in_green_total), s.f)
    s.print_f("The number of green clusters containing at least one red point is: {} \n".format(len(greens)), s.f)
    s.print_f("which are {}% of the green clusters. \n\n".format(p_green_clstrs_with_red_points), s.f)

    s.print_f("The number of green clusters containing at least three red points is: {} \n".format(len(green_5)), s.f)
    s.print_f("which are {}% of the green clusters. \n\n".format(float(len(green_5))*100/len(s.green_clusters)), s.f)

    s.print_f("The number of green clusters containing at least six red points is: {} \n".format(len(green_10)), s.f)
    s.print_f("which are {}% of the green clusters. \n\n".format(float(len(green_10))*100/len(s.green_clusters)), s.f)

    s.print_f("\n_______red clusters__vs.__green points____________\n\n", s.f)

    s.print_f("The number of red clusters containing at least one green point is: {} \n".format(len(reds)), s.f)
    s.print_f("which are {}% of the red clusters. \n\n".format(p_red_clstrs_with_green_points), s.f)

    s.print_f("The number of red clusters containing at least three green points is: {} \n".format(len(red_5)), s.f)
    s.print_f("which are {}% of the red clusters. \n\n".format(float(len(red_5))*100/len(s.red_clusters)), s.f)

    s.print_f("The number of red clusters containing at least six green points is: {} \n".format(len(red_10)), s.f)
    s.print_f("which are {}% of the red clusters. \n\n".format(float(len(red_10))*100/len(s.red_clusters)), s.f)

    s.print_f("The average number of green points in a red cluster is: {} \n".format(avg_green_in_red), s.f)
    s.print_f("The total number of green points in red clusters: {} \n".format(green_in_red_total), s.f)

    # get a picture of the  after appending

    get_picture(s,[s.clustered_points, added_points], ["green", "red"], name="diameter_specific_appending")

    s.print_f("\nPerforming second round of clustering  on all clustered points\n", s.f)


    print("green cleaning process")
    new_green_points = []
    excluded = []
    for i in range(len(s.green_clusters)):
        pts = s.green_clusters[i].clean_outliers(dim=dimension)
        ok_list = pts[0]
        new_green_points += ok_list
        excluded += pts[1]

    print("red cleaning process")
    new_red_points = []
    for i in range(len(s.red_clusters)):
        pts = s.red_clusters[i].clean_outliers(dim=dimension)
        ok_list = pts[0]
        new_red_points += ok_list
        excluded += pts[1]

    # get a picture of the  after appending and after outliers

    get_picture(s,[new_green_points+new_red_points, excluded], ["green", "red"], name="outliers")
    s.part2_points = new_red_points + new_green_points
    s.part2_points_dbscan = to_np(s.part2_points)
    antr_line = "cleaning process is over. Excluded {} points, which constitue {}% of all points.\n"\
        .format(len(excluded), (float(len(excluded))/len(s.part2_points))*100 )
    s.print_f(antr_line, s.f)

    # PCA analysis of 2nd part clusters

    s.green_clusters = [x for x in s.green_clusters if len(x.points) > 3] # dillute small clusters
    s.red_clusters = [x for x in s.red_clusters if len(x.points) > 3] # because they can cause problems in pca

    for i in s.green_clusters:
        i.pca_analysis(dimension)
    for j in s.red_clusters:
        j.pca_analysis(dimension)

    # calculate mean shape

    green_output_list = []
    red_output_list = []

    mean_green_shape = float(sum([x.shape_2d for x in s.green_clusters]))/len(s.green_clusters)
    mean_red_shape = float(sum([x.shape_2d for x in s.red_clusters]))/len(s.red_clusters)
    s.print_f("Mean green shape: {}%.\n".format(mean_green_shape), s.f)
    s.print_f("Mean red shape: {}%.\n".format(mean_red_shape), s.f)

    s.print_f("color, #points, #red points, #green points, sphere score, angle_x, angle_y, size, density\n", s.f_clusters)

    # save sizes to compute histograms
    green_hist = []
    red_hist = []

    for red_cluster in s.red_clusters:
        red_hist.append(red_cluster.size)
        if red_cluster.size == 0:
            continue
        red_line = "red" + ", "+\
                    str(len(red_cluster.points))+", "+\
                    str(sum([1 for x in red_cluster.points if x.color == "red"])) + ", " +\
                    str(sum([1 for x in red_cluster.points if x.color == "green"])) + ", " +\
                    str(red_cluster.shape_2d) + ", " +\
                    str(red_cluster.angle_x) + ", " +\
                    str(red_cluster.angle_y) + ", " +\
                    str(red_cluster.size) + ", " +\
                    str(len(red_cluster.points)/float(red_cluster.size)) + "\n"
        s.print_f(red_line, s.f_clusters)
        red_output_list.append(red_line)
    for green_cluster in s.green_clusters:
        if green_cluster.size == 0:
            continue

        green_hist.append(green_cluster.size)
        green_line = "green" + ", "+\
                        str(len(green_cluster.points))+", "+\
                        str(sum([1 for x in green_cluster.points if x.color == "red"])) + ", " +\
                        str(sum([1 for x in green_cluster.points if x.color == "green"])) + ", " +\
                        str(green_cluster.shape_2d) + ", " + str(green_cluster.angle_x) + ", " +\
                        str(green_cluster.angle_y) + ", " +\
                        str(green_cluster.size) + ", " +\
                        str(len(green_cluster.points)/float(green_cluster.size)) + "\n"
        s.print_f(green_line, s.f_clusters)
        green_output_list.append(green_line)

    make_histogram(s, red_hist, "red")
    make_histogram(s, green_hist, "green")
    s.print_f(remarks, s.f)
    s.print_f("That's it. Thank you and Bye Bye.", s.f)
    s.f.close()
    s.f_clusters.close()
    s.f_csv.close()

    return red_output_list, green_output_list

