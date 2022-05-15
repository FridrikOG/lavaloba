import numpy as np
## ends at n_lobes



@cuda.jit
def save_at_end(lobe_thickness_array, x, y, x1, x2, angle, X_circle, Y_circle, xmin, ymin, nx, ny, cell, Xs, Ys, xv, yv, nv2, dist_int, Zdist, Zflow, Ztot_temp, jtop_array, jbottom_array, iright_array, ileft_array, Zflow_local_array, max_cells, Ztot):
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
    # lobe_thickness = thickness_min + (i-1) * delta_lobe_thickness

    # Update the thickness for the grid points selected (global indexing)
    Zflow[j_bottom:j_top, i_left:i_right] += lobe_thickness_array[i]*Zflow_local

    Ztot_temp[j_bottom:j_top, i_left:i_right] = Zs[j_bottom:j_top, i_left:i_right] + \
        filling_parameter * Zflow[j_bottom:j_top, i_left:i_right]

    # Save the bounding box of the i-th lobe
    jtop_array[i] = j_top
    jbottom_array[i] = j_bottom

    iright_array[i] = i_right
    ileft_array[i] = i_left

    if (hazard_flag):

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

