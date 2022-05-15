## GLOBAL VARS
# vent_flag
# n_init
# n_flows
# max_slope_prob
# max_aspect_ratio
# aspect_ratio_coeff
# lobe_area

# lobe_exponent
# force_max_length
# max_length
# start_from_dist_flag

@cuda.jit
def transform_loop_three(dist_int, parent, n_lobes ):
    i = cuda.grid(1)
    if i < n_lobes:
        if (lobe_exponent > 0):

                idx0 = np.random.uniform(0, 1, size=1)

                idx1 = idx0 ** lobe_exponent

                if (force_max_length):

                    # the parent lobe is chosen only among those with
                    # dist smaller than the maximum value fixed in input
                    mask = dist_int[0:i] < max_length

                    idx2 = sum(mask[0:i]) * idx1

                    idx3 = np.floor(idx2)

                    idx = np.int(idx3)

                    sorted_dist = np.argsort(dist_int[0:i])

                    idx = sorted_dist[idx]

                else:

                    # the parent lobe is chosen among all the lobes

                    idx2 = i * idx1

                    idx3 = np.floor(idx2)

                    idx = np.int(idx3)

                if (start_from_dist_flag):

                    # the probability law is associated to the distance
                    # from the vent
                    sorted_dist = np.argsort(dist_int[0:i])

                    idx = sorted_dist[idx]

        else:

            idx = i-1


        # save the index of the parent and the distance from first lobe of the chain
        parent[i] = idx
        dist_int[i] = dist_int[idx] + 1






for i in range(n_init, n_lobes):

        if (n_flows == 1):
            # print on screen bar with percentage of flows computed
            last_percentage = np.rint(i*20.0/(n_lobes-1))*5
            sys.stdout.write('\r')
            sys.stdout.write("[%-20s] %d%%" %
                             ('='*(last_percentage/5), last_percentage))
            sys.stdout.flush()

        # STEP 0: DEFINE THE INDEX idx OF THE PARENT LOBE

        if (lobe_exponent > 0):

            idx0 = np.random.uniform(0, 1, size=1)

            idx1 = idx0 ** lobe_exponent

            if (force_max_length):

                # the parent lobe is chosen only among those with
                # dist smaller than the maximum value fixed in input
                mask = dist_int[0:i] < max_length

                idx2 = sum(mask[0:i]) * idx1

                idx3 = np.floor(idx2)

                idx = np.int(idx3)

                sorted_dist = np.argsort(dist_int[0:i])

                idx = sorted_dist[idx]

            else:

                # the parent lobe is chosen among all the lobes

                idx2 = i * idx1

                idx3 = np.floor(idx2)

                idx = np.int(idx3)

            if (start_from_dist_flag):

                # the probability law is associated to the distance
                # from the vent
                sorted_dist = np.argsort(dist_int[0:i])

                idx = sorted_dist[idx]

        else:

            idx = i-1

        # save the index of the parent and the distance from first lobe of the chain
        parent[i] = idx
        dist_int[i] = dist_int[idx] + 1

        # for all the "ancestors" increase by one the number of descendents

        last = i
        # Loop 2
        count_inside += 1
        # print("DSFdsf ", dist_int[idx])


        for j in range(0, dist_int[idx]+1):

            previous = parent[last]
            descendents[previous] = descendents[previous]+1
            last = previous

        # local slope of the topography. The slope affects both the location of
        # the new lobe on the boundary of the previous one and its aspect
        # ratio:
        # if slope = 0 the lobe is a circle (x1=x2);
        # if slope > 1 the lobe is an ellipse.

        # STEP 1: COMPUTE THE SLOPE AND THE MAXIMUM SLOPE ANGLE
        #         The direction az_i as described in the paper is found here

        # Search for the cell containing the center of the parent lobe
        xi = (x[idx] - xmin)/cell
        yi = (y[idx] - ymin)/cell

        # Indexes of the lower-left corner of the cell containing the center of the parent lobe
        ix = np.floor(xi)
        iy = np.floor(yi)

        # Convert to integer
        ix = ix.astype(int)
        iy = iy.astype(int)

        # Indexes of the top-right corner of the cell containing the center of the parent lobe
        ix1 = ix+1
        iy1 = iy+1

        # Stopping condition (lobe close the domain boundary)
        if (ix <= max_cells) or (ix1 >= nx-max_cells) or (iy <= max_cells) or (iy1 >= ny-max_cells):

            last_lobe = i-1
            break

        # Relative coordinates of the center of the parent lobe in the cell
        xi_fract = xi-ix
        yi_fract = yi-iy

        # Ztot at the parent lobe center (obained with a bilinear interpolation)
        zidx = xi_fract * (yi_fract * Ztot[iy1, ix1] + (1.0-yi_fract) * Ztot[iy, ix1]) \
            + (1.0-xi_fract) * (yi_fract *
                                Ztot[iy1, ix] + (1.0-yi_fract) * Ztot[iy, ix])

        # Compute n_points on the parent lobe boundary to search for the point with minimum Ztot
        [xe, ye] = ellipse(x[idx], y[idx], x1[idx], x2[idx],
                           angle[idx], X_circle, Y_circle)

        xei = (xe - xmin)/cell
        yei = (ye - ymin)/cell

        # Indexes of the lower-left corners of the cells containing the points on the lobe boundary
        ixe = np.floor(xei)
        iye = np.floor(yei)

        # Convert to integers
        ixe = ixe.astype(int)
        iye = iye.astype(int)

        # Indexes of the top-right corners of the cells containing the points on the lobe boundary
        ixe1 = ixe+1
        iye1 = iye+1

        # Relative coordinates of the n_points in the respective containing cells
        xei_fract = xei-ixe
        yei_fract = yei-iye

        # Ztot at the n_points on the parent lobe boundary (obained with a bilinear interpolation)
        ze = xei_fract * (yei_fract * Ztot[iye1, ixe1] + (1.0-yei_fract) * Ztot[iye, ixe1]) \
            + (1.0-xei_fract) * (yei_fract *
                                 Ztot[iye1, ixe] + (1.0-yei_fract) * Ztot[iye, ixe])

        # Index of the point with minimum Ztot
        idx_min = np.argmin(ze)

        # Components of the vector from the parent lobe center to the point of minimum
        dx_lobe = x[idx] - xe[idx_min]
        dy_lobe = y[idx] - ye[idx_min]
        dz_lobe = zidx - ze[idx_min]

        # Slope of the vector
        slope = np.maximum(
            0.0, dz_lobe / (np.sqrt(np.square(dx_lobe)+np.square(dy_lobe))))

        # Angle defining the direction of maximum slope
        max_slope_angle = np.mod(
            180 + (180 * np.arctan2(dy_lobe, dx_lobe) / pi), 360)

        # STEP 2: PERTURBE THE MAXIMUM SLOPE ANGLE ACCORDING TO PROBABILITY LAW
        #         the direction az_i' as described in the paper is found here

        # This expression define a coefficient used for the direction of the next slope
        if (max_slope_prob < 1):

            # Angle defining the direction of the new slope. when slope=0, then
            # we have an uniform distribution for the possible angles for the next lobe.

            slopedeg = 180.0 * np.arctan(slope) / pi

            if (slopedeg > 0.0) and (max_slope_prob > 0.0):

                sigma = (1.0 - max_slope_prob) / max_slope_prob * \
                    (90.0 - slopedeg) / slopedeg
                rand_angle_new = rtnorm.rtnorm(-180, 180, 0, sigma)

            else:

                rand = np.random.uniform(0, 1, size=1)
                rand_angle_new = 360.0 * np.abs(rand-0.5)

            new_angle = max_slope_angle + rand_angle_new[0]

        else:

            new_angle = max_slope_angle

        # STEP 3: ADD THE EFFECT OF INERTIA
        #         the direction az_i'' as described in the paper is found here

        # cos and sin of the angle of the parent lobe
        cos_angle1 = np.cos(angle[idx]*deg2rad)
        sin_angle1 = np.sin(angle[idx]*deg2rad)

        # cos and sin of the angle of maximum slope
        cos_angle2 = np.cos(new_angle*deg2rad)
        sin_angle2 = np.sin(new_angle*deg2rad)

        if (inertial_exponent == 0):

            alfa_inertial[i] = 0.0

        else:

            alfa_inertial[i] = (1.0 - (2.0 * np.arctan(slope) / np.pi)**inertial_exponent) \
                ** (1.0 / inertial_exponent)

        x_avg = (1.0 - alfa_inertial[i]) * \
            cos_angle2 + alfa_inertial[i] * cos_angle1
        y_avg = (1.0 - alfa_inertial[i]) * \
            sin_angle2 + alfa_inertial[i] * sin_angle1

        angle_avg = np.mod(180 * np.arctan2(y_avg, x_avg) / pi, 360)

        new_angle = angle_avg

        # STEP 4: DEFINE THE SEMI-AXIS OF THE NEW LOBE

        # a define the ang.coeff. of the line defining the location of the
        # center of the new lobe in a coordinate system defined by the
        # semi-axes of the existing lobe
        a = np.tan(deg2rad*(new_angle-angle[idx]))

        # xt is the 1st-coordinate of the point of the boundary of the ellipse
        # definind the direction of the new lobe, in a coordinate system
        # defined by the semi-axes of the existing lobe
        if (np.cos(deg2rad*(new_angle-angle[idx])) > 0):

            xt = np.sqrt(x1[idx]**2 * x2[idx]**2 /
                         (x2[idx]**2 + x1[idx]**2 * a**2))

        else:

            xt = - np.sqrt(x1[idx]**2 * x2[idx]**2 /
                           (x2[idx]**2 + x1[idx]**2 * a**2))

        # yt is the 2nd-coordinate of the point of the boundary of the ellipse
        # definind the direction of the new lobe, in a coordinate system
        # defined by the semi-axes of the existing lobe
        yt = a * xt

        # (delta_x,delta_y) is obtained rotating the vector (xt,yt) by the
        # angle defined by the major semi-axis of the existing lobe. In this
        # way we obtain the location in a coordinate-system centered in the
        # center of the existing lobe, but this time with the axes parallel to
        # the original x and y axes.

        delta_x = xt * cos_angle1 - yt * sin_angle1
        delta_y = xt * sin_angle1 + yt * cos_angle1

        # The slope coefficient is evaluated at the point of the boundary of the ellipse
        # definind by the direction of the new lobe

        xi = (x[idx]+delta_x - xmin)/cell
        yi = (y[idx]+delta_y - ymin)/cell

        ix = np.floor(xi)
        iy = np.floor(yi)

        ix = ix.astype(int)
        iy = iy.astype(int)

        ix1 = ix+1
        iy1 = iy+1

        # Stopping condition (lobe close the domain boundary)
        if (ix <= max_cells) or (ix1 >= nx-max_cells) or (iy <= max_cells) or (iy1 >= ny-max_cells):

            last_lobe = i-1
            break

        xi_fract = xi-ix
        yi_fract = yi-iy

        # ztot at the new budding point
        ze = xi_fract * (yi_fract * Ztot[iy1, ix1] + (1.0-yi_fract) * Ztot[iy, ix1]) \
            + (1.0-xi_fract) * (yi_fract *
                                Ztot[iy1, ix] + (1.0-yi_fract) * Ztot[iy, ix])

        slope = np.maximum(0.0, (zidx - ze) /
                           (np.sqrt(np.square(delta_x)+np.square(delta_y))))

        aspect_ratio = min(max_aspect_ratio, 1.0 + aspect_ratio_coeff * slope)

        # (new_x1,new_x2) are the semi-axes of the new lobe. slope_coeff is
        # used to have an elongated lobe accoriding to the slope of the
        # topography. It is possible to modifiy these values in order to have
        # the same volume for all the lobes.
        new_x1 = np.sqrt(lobe_area/np.pi)*np.sqrt(aspect_ratio)
        new_x2 = np.sqrt(lobe_area/np.pi)/np.sqrt(aspect_ratio)

        # v1 is the distance of the new point found on the boundary of the lobe
        # from the center of the lobe
        v1 = np.sqrt(delta_x**2 + delta_y**2)

        # v2 is the distance between the centers of the two lobes when they
        # intersect in one point only
        v2 = v1 + new_x1

        # v is the distance between the centers of the two lobes, according to
        # the value of the parameter dist_fact
        v = (v1 * (1.0 - dist_fact) + v2 * dist_fact) / v1

        # STEP 5: BUILD THE NEW LOBE

        # (x_new,y_new) are the coordinates of the center of the new lobe
        x_new = x[idx] + v * delta_x
        y_new = y[idx] + v * delta_y

        # Plot the new lobe
        if (plot_lobes_flag == 1):

            patch.append(Ellipse([x_new, y_new], 2*new_x1, 2*new_x2, new_angle,
                                 facecolor='none', edgecolor='r'))

        # Store the parameters of the new lobe in arrays
        angle[i] = new_angle
        x1[i] = new_x1
        x2[i] = new_x2
        x[i] = x_new
        y[i] = y_new

        if (saveshape_flag):

            # Compute n_points on the lobe boundary
            [xe, ye] = ellipse(x_new, y_new, new_x1, new_x2,
                               new_angle, X_circle, Y_circle)

            shape_verts[0:npoints-1, 0] = xe[0:npoints-1]
            shape_verts[0:npoints-1, 1] = ye[0:npoints-1]

            w.poly(parts=[shape_verts.tolist()])
            w.record(
                str(i+1), dist_int[i], str(descendents[i]), str(parent[i]), str(flow+1))

        # Check the grid points covered by the lobe
        if (saveraster_flag == 1) or (topo_mod_flag >= 1) or (plot_flow_flag):

            # Compute n_points on the new lobe boundary
            [xe, ye] = ellipse(x[i], y[i], x1[i], x2[i],
                               angle[i], X_circle, Y_circle)

            # Bounding box for the new lobe
            min_xe = np.min(xe)
            max_xe = np.max(xe)

            min_ye = np.min(ye)
            max_ye = np.max(ye)

            xi = (min_xe - xmin)/cell
            ix = np.floor(xi)
            i_left = ix.astype(int)-1
            i_left = np.maximum(0, np.minimum(nx-1, i_left))

            xi = (max_xe - xmin)/cell
            ix = np.floor(xi)
            i_right = ix.astype(int)+3
            i_right = np.maximum(0, np.minimum(nx-1, i_right))

            yj = (min_ye - ymin)/cell
            jy = np.floor(yj)
            j_bottom = jy.astype(int)-1
            j_bottom = np.maximum(0, np.minimum(ny-1, j_bottom))

            yj = (max_ye - ymin)/cell
            jy = np.floor(yj)
            j_top = jy.astype(int)+3
            j_top = np.maximum(0, np.minimum(ny-1, j_top))

            # Copy the full grid within the bounding box on a local one to work on a smaller
            # domain and reduce the computational cost
            Xs_local = Xs[j_bottom:j_top, i_left:i_right]
            Ys_local = Ys[j_bottom:j_top, i_left:i_right]

            # Compute the fraction of cells covered by the lobe (local indexing)
            area_fract = local_intersection(
                Xs_local, Ys_local, x[i], y[i], x1[i], x2[i], angle[i], xv, yv, nv2)

            Zflow_local = area_fract

            # Compute the local integer covering (0-not covered  1-covered)
            Zflow_local_int = np.ceil(area_fract)
            Zflow_local_int = Zflow_local_int.astype(int)

            # Define the distance (number of lobes) from the vent (local indexing)
            Zdist_local = Zflow_local_int * \
                dist_int[i] + 9999 * (Zflow_local == 0)

            # update the minimum distance in the global indexing
            Zdist[j_bottom:j_top, i_left:i_right] = np.minimum(Zdist[j_bottom:j_top, i_left:i_right],
                                                               Zdist_local)

            # Compute the thickness of the lobe
            lobe_thickness = thickness_min + (i-1) * delta_lobe_thickness

            # Update the thickness for the grid points selected (global indexing)
            Zflow[j_bottom:j_top, i_left:i_right] += lobe_thickness*Zflow_local

            Ztot_temp[j_bottom:j_top, i_left:i_right] = Zs[j_bottom:j_top, i_left:i_right] + \
                filling_parameter * Zflow[j_bottom:j_top, i_left:i_right]

            # Save the bounding box of the i-th lobe
            jtop_array[i] = j_top
            jbottom_array[i] = j_bottom

            iright_array[i] = i_right
            ileft_array[i] = i_left

            if (hazard_flag):

                # Store the local arrays used later for the hazard map

                if not (Zflow_local_int.shape[0] == (j_top-j_bottom)):

                    print(Zflow_local_int.shape[0], j_top, j_bottom)
                    print(Zflow_local_int.shape[1], i_right, i_left)
                    print('')

                if not (Zflow_local_int.shape[1] == (i_right - i_left)):

                    print(Zflow_local_int.shape[0], j_top, j_bottom)
                    print(Zflow_local_int.shape[1], i_right, i_left)
                    print('')

                if (np.max(Zflow_local.shape) > Zflow_local_array.shape[1]):

                    print(cell, new_x1, new_x2, new_angle)

                    print(Zflow_local)

                Zflow_local_array[i, 0:j_top-j_bottom,
                                  0:i_right-i_left] = Zflow_local_int

            if (n_check_loop > 0) and (i > i_first_check):

                i_left_last_lobes = np.min(ileft_array[i-n_check_loop:i])
                i_right_last_lobes = np.max(iright_array[i-n_check_loop:i])

                delta_i_last_lobes = i_right_last_lobes - i_left_last_lobes

                j_bottom_last_lobes = np.min(jbottom_array[i-n_check_loop:i])
                j_top_last_lobes = np.max(jtop_array[i-n_check_loop:i])

                delta_j_last_lobes = j_top_last_lobes - j_bottom_last_lobes

                max_delta = max(delta_i_last_lobes, delta_j_last_lobes)

                if (max_delta <= max_cells):

                    i_first_check = i + n_check_loop
                    np.copyto(Ztot, Ztot_temp)

            lobes_counter = lobes_counter + 1

        # Update the deposit of the lava lobes over the computational grid
        if (topo_mod_flag == 2) and (lobes_counter == n_lobes_counter):

            lobes_counter = 0
            np.copyto(Ztot, Ztot_temp)