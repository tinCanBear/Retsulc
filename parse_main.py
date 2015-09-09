from __future__ import print_function
import os
from classes import *
from show import *
import numpy as np
from sklearn.cluster import DBSCAN

new_stuff = False

def main(data_type, epsilon, minimum_neighbors, mini_eps, mini_minimum_neighbors, green_name, red_name, proj_name, file_dir):
    green_file_name = green_name
    red_file_name = red_name
    name = proj_name
    clusters_file_final = "clusters_final" #+ name
    clusters_file_pre = "clusters_pre" #+ name

    remarks = "....."
    file_directory = file_dir
    #------------------------Dimension----------------------------------------#
    if data_type != "3d" and data_type != "raw_3d":
        dimension = 2
    else:
        dimension = 3

    ##               create sample object: 's'                           ##

    s = Sample(green_file_name,red_file_name, epsilon = epsilon, min_n = minimum_neighbors, path=file_directory, \
               data_type=data_type, name=name)

    s.mini_eps = mini_eps
    s.mini_minimum_ngbs = mini_minimum_neighbors
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

    # make output folder and open files
    if not os.path.exists(file_directory):
        os.mkdir(file_directory)

    s.f = open(file_directory + "summary.txt", "w")
    s.f_clusters_final = open(file_directory + clusters_file_final + ".csv", "w")
    s.f_clusters_pre = open(file_directory + clusters_file_pre + ".csv", "w")
    s.print_f("the green file is: \n", s.f)
    s.print_f(green_file_name + "\n", s.f)
    s.print_f("the red file is: \n", s.f)
    s.print_f(red_file_name + "\n", s.f)

    s.points_summary()

    # PCA analysis

    s.clusters = [x for x in s.clusters if len(x.points) > 3] # dillute small clusters
    s.green_clusters = [x for x in s.green_clusters if len(x.points) > 3] # dillute small clusters
    s.red_clusters = [x for x in s.red_clusters if len(x.points) > 3] # (because they can cause problems in pca)

    for i in s.green_clusters:
        i.pca_analysis(dimension)
    for j in s.red_clusters:
        j.pca_analysis(dimension)
    for k in s.clusters:
        k.pca_analysis

    # plot k-distances

    plot_knn(s.green_points_dbscan, file_directory, "kdist_green")
    plot_knn(s.red_points_dbscan, file_directory, "kdist_red")

    # make rainbow pic.
    rainbow(s, "_pre")
    green_hist = []
    red_hist = []
    for green_cluster in s.green_clusters:
        green_hist.append(green_cluster.size)
    for red_cluster in s.red_clusters:
        red_hist.append(red_cluster.size)
    make_histogram(s, red_hist, "red", other="_pre")
    make_histogram(s, green_hist, "green", other="_pre")


    csv_clusters_titles = "color,#points,#red points,#green points,sphere score,angle_x,angle_y,size,density,colocalized\n"
    s.print_f(csv_clusters_titles, s.f_clusters_pre)
    s.print_f(csv_clusters_titles, s.f_clusters_final)

    # ____need to return the clusters now 'as-is'_____#
    red_output_list_pre = []
    green_output_list_pre = []
    null_list = []
    for red_cluster in s.red_clusters:
        line, changed = get_line(s, null_list, red_cluster, "red", append=False)
        s.print_f(line, s.f_clusters_pre)
        red_output_list_pre.append(line)

    for green_cluster in s.green_clusters:
        line, changed = get_line(s, null_list, green_cluster, "green", append=False)
        s.print_f(line, s.f_clusters_pre)
        green_output_list_pre.append(line)

    # for red_cluster in s.red_clusters:
    #     if red_cluster.size == 0:
    #         continue
    #     red_line_pre = "red" + ", "+\
    #                 str(len(red_cluster.points))+", "+\
    #                 str(sum([1 for x in red_cluster.points if x.color == "red"])) + ", " +\
    #                 str(sum([1 for x in red_cluster.points if x.color == "green"])) + ", " +\
    #                 str(red_cluster.shape_2d) + ", " +\
    #                 str(red_cluster.angle_x) + ", " +\
    #                 str(red_cluster.angle_y) + ", " +\
    #                 str(red_cluster.size) + ", " +\
    #                 str(len(red_cluster.points)/float(red_cluster.size)) + "\n"
    #     s.print_f(red_line_pre, s.f_clusters_pre)
    #     red_output_list_pre.append(red_line_pre)
    # for green_cluster in s.green_clusters:
    #     if green_cluster.size == 0:
    #         continue
    #     green_line_pre = "green" + ", "+\
    #                     str(len(green_cluster.points))+", "+\
    #                     str(sum([1 for x in green_cluster.points if x.color == "red"])) + ", " +\
    #                     str(sum([1 for x in green_cluster.points if x.color == "green"])) + ", " +\
    #                     str(green_cluster.shape_2d) + ", " + str(green_cluster.angle_x) + ", " +\
    #                     str(green_cluster.angle_y) + ", " +\
    #                     str(green_cluster.size) + ", " +\
    #                     str(len(green_cluster.points)/float(green_cluster.size)) + "\n"
    #     s.print_f(green_line_pre, s.f_clusters_pre)
    #     green_output_list_pre.append(green_line_pre)

    # ____need to return the clusters now 'as-is'_____#
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

    p_green_clstrs_with_red_points = float(len(greens))*100/len(s.green_clusters) if len(s.green_clusters) > 0 else 0
    p_red_clstrs_with_green_points = float(len(reds))*100/len(s.red_clusters) if len(s.red_clusters) > 0 else 0

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

    avg_green_in_red = float(green_in_red_total)/len(s.red_clusters) if len(s.red_clusters) > 0 else 0
    avg_red_in_green = float(red_in_green_total)/len(s.green_clusters) if len(s.green_clusters) > 0 else 0
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
        i.pca_analysis(dimension, sphere=False)
    for j in s.red_clusters:
        j.pca_analysis(dimension, sphere=False)

    rainbow(s, "_final")

    # calculate mean shape

    green_output_list = []
    red_output_list = []

    mean_green_shape = float(sum([x.shape_2d for x in s.green_clusters]))/len(s.green_clusters) if len(s.green_clusters) > 0 else 0
    mean_red_shape = float(sum([x.shape_2d for x in s.red_clusters]))/len(s.red_clusters) if len(s.red_clusters) > 0 else 0
    s.print_f("Mean green shape: {}%.\n".format(mean_green_shape), s.f)
    s.print_f("Mean red shape: {}%.\n".format(mean_red_shape), s.f)


    # save sizes to compute histograms
    green_hist = []
    red_hist = []
    hist_lists = [red_hist, green_hist]
    # assign lists to pick up the clusters that changed their color (used to be 'red' but now has more green points)

    for red_cluster in s.red_clusters:
        line, changed = get_line(s, hist_lists, red_cluster, "red")
        s.print_f(line, s.f_clusters_final)
        if changed:
           green_output_list.append(line)
        else:
            red_output_list.append(line)

    for green_cluster in s.green_clusters:
        line, changed = get_line(s, hist_lists, green_cluster, "green")
        s.print_f(line, s.f_clusters_final)
        if changed:
            red_output_list.append(line)
        else:
            green_output_list.append(line)
        # if red_cluster.size == 0:
        #     continue
        # gs = sum([1 for x in red_cluster.points if x.color == "green"])
        # rds = sum([1 for x in red_cluster.points if x.color == "red"])
        # if gs > rds: # change of dominant color!!
        #     leftovers_red.append(red_cluster)
        #     continue
        # red_hist.append(red_cluster.size)
        # red_line = "red" + ", "+\
        #             str(len(red_cluster.points))+", "+\
        #             str(sum([1 for x in red_cluster.points if x.color == "red"])) + ", " +\
        #             str(sum([1 for x in red_cluster.points if x.color == "green"])) + ", " +\
        #             str(red_cluster.shape_2d) + ", " +\
        #             str(red_cluster.angle_x) + ", " +\
        #             str(red_cluster.angle_y) + ", " +\
        #             str(red_cluster.size) + ", " +\
        #             str(len(red_cluster.points)/float(red_cluster.size)) + "\n"
        # s.print_f(red_line, s.f_clusters_final)
        # red_output_list.append(red_line)
        # if green_cluster.size == 0:
        #     continue
        # gs = sum([1 for x in red_cluster.points if x.color == "green"])
        # rds = sum([1 for x in red_cluster.points if x.color == "red"])
        # if gs < rds: # change of dominant color!!
        #     leftovers_green.append(red_cluster)
        #     continue
        # green_hist.append(green_cluster.size)
        # green_line = "green" + ", "+\
        #                 str(len(green_cluster.points))+", "+\
        #                 str(sum([1 for x in green_cluster.points if x.color == "red"])) + ", " +\
        #                 str(sum([1 for x in green_cluster.points if x.color == "green"])) + ", " +\
        #                 str(green_cluster.shape_2d) + ", " + str(green_cluster.angle_x) + ", " +\
        #                 str(green_cluster.angle_y) + ", " +\
        #                 str(green_cluster.size) + ", " +\
        #                 str(len(green_cluster.points)/float(green_cluster.size)) + "\n"
        # s.print_f(green_line, s.f_clusters_final)
        # green_output_list.append(green_line)

    make_histogram(s, hist_lists[0], "red", other="_final")
    make_histogram(s, hist_lists[1], "green", other="_final")
    s.print_f(remarks, s.f)
    s.print_f("That's it. Thank you and Bye Bye.", s.f)
    s.f.close()
    s.f_clusters_pre.close()
    s.f_clusters_final.close()

    if new_stuff:
        ##----OPTION-1----##
        mixed_clusters = s.red_clusters + s.green_clusters
        for c1 in mixed_clusters:
            for c2 in mixed_clusters:
                if c1 is c2:
                    continue
                biggest = 0 if c1.size > c2.size else 1
                big_radius = c1.size if c1.size > c2.size else c2.size
                if dist(c1.center, c2.center) < big_radius:
                    if not biggest:
                        c1.points = c1.points + c2.points
                        c2.size = 0
                        c2.points = []
                        c1.pca_analysis(dim=2)
                    else:
                        c2.points = c1.points + c2.points
                        c1.size = 0
                        c1.points = []
                        c2.pca_analysis(dim=2)
        mixed_clusters = s.red_clusters + s.green_clusters
        for c1 in mixed_clusters:
            for c2 in mixed_clusters:
                if c1 is c2:
                    continue
                biggest = 0 if c1.size > c2.size else 1
                big_radius = c1.size if c1.size > c2.size else c2.size
                if dist(c1.center, c2.center) < big_radius:
                    if not biggest:
                        c1.points = c1.points + c2.points
                        c2.size = 0
                        c2.points = []
                        c1.pca_analysis(dim=2)
                    else:
                        c2.points = c1.points + c2.points
                        c1.size = 0
                        c1.points = []
                        c2.pca_analysis(dim=2)
        rainbow(s, other="_option1")
    return red_output_list, green_output_list, red_output_list_pre, green_output_list_pre

def get_line(s, hist_lists, cluster, color, append=True):
    index_hists = 0 if color == "red" else 1 #hist_lists[0] = red_hist
    changed = False
    other_color = "green" if color=="red" else "red"
    this_color = color
    if cluster.size == 0:
        return 0
    other_color_count = sum([1 for x in cluster.points if x.color == other_color])
    color_count = sum([1 for x in cluster.points if x.color == color])
    if other_color_count > color_count: # change of dominant color!!
        this_color = other_color
        index_hists = (index_hists + 1)%2 # add to the other list
        changed = True
    ending = ",0\n"
    if append: # use this variable to distinguish between 1st part and 2nd.
        ending = ",1\n" if is_good_colocalized(s, cluster, this_color) else ",0\n"
    if append:
        hist_lists[index_hists].append(cluster.size)
    line = this_color + ", "+\
                str(len(cluster.points))+", "+\
                str(sum([1 for x in cluster.points if x.color == "red"])) + ", " +\
                str(sum([1 for x in cluster.points if x.color == "green"])) + ", " +\
                str(cluster.shape_2d) + ", " +\
                str(cluster.angle_x) + ", " +\
                str(cluster.angle_y) + ", " +\
                str(cluster.size) + ", " +\
                str(len(cluster.points)/float(cluster.size)) + ending
    return line, changed

def is_good_colocalized(s, cluster, color):
    other_color = "green" if color == "red" else "red"
    cnt = 0
    points = []
    for point in cluster.points:
        if point.color == other_color:
            cnt += 1
            points.append(point.point)
    if cnt < 10:
        return 0
    else:
        mini_c = Sample("","", epsilon = s.mini_eps, min_n = s.mini_minimum_ngbs, path="", \
           data_type="2d", name="")
        mini_c.points = points
        all_points = np.array(mini_c.points)
        db = DBSCAN(eps = mini_c.epsilon, min_samples = mini_c.min_n).fit(all_points)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_
        mini_c.labels = labels
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        mini_c.clusters = [Cluster() for i in range(n_clusters_)]
        for i in range(len(labels)):
            if labels[i] != -1:
                mini_c.clusters[labels[i]].add_point(mini_c.points[i])
        for mini_cluster in mini_c.clusters:
            if len(mini_cluster.points) >= 10:
                return 1 # there exists a cluster of the other color by itself!
        return 0 # clusters are not big enough
