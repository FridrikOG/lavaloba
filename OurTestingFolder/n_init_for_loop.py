##  GLOBAL VARS
# vent_flag
# n_init
# n_flows
# max_slope_prob
# max_aspect_ratio
# aspect_ratio_coeff
# lobe_area




@cuda.jit
def n_init_loop(n_lobes, n_vents, x, y, x_vent, y_vent, flow, cum_fiss_length, dist_int, descendents, Ztot, angle, x1, x2, xmin, ymin, cell ):
    i =  cuda.grid(1)    
    if i  < n_init:
        if (n_flows == 1):
            # Print on screen bar with percentage of flows computed
            last_percentage = np.rint(i*20.0/(n_lobes-1))*5
            last_percentage = last_percentage.astype(int)

            sys.stdout.write('\r')
            sys.stdout.write("[%-20s] %d%%" %
                                ('='*(last_percentage/5), last_percentage))
            sys.stdout.flush()

        # STEP 0: COMPUTE THE FIRST LOBES OF EACH FLOW

        if (n_vents == 1):

            x[i] = x_vent[0]
            y[i] = y_vent[0]

        else:

            if (vent_flag == 0):

                i_vent = np.int(np.floor(flow * n_vents / n_flows))

                x[i] = x_vent[i_vent]
                y[i] = y_vent[i_vent]

            elif (vent_flag == 1):

                i_vent = np.random.randint(n_vents, size=1)

                x[i] = x_vent[i_vent]
                y[i] = y_vent[i_vent]

            elif (vent_flag == 2):

                alfa_polyline = np.random.uniform(0, 1, size=1)

                idx_vent = np.argmax(cum_fiss_length > alfa_polyline)

                num = alfa_polyline - cum_fiss_length[idx_vent-1]
                den = cum_fiss_length[idx_vent] - cum_fiss_length[idx_vent-1]

                alfa_segment = num / den

                x[i] = alfa_segment * x_vent[idx_vent] + \
                    (1.0 - alfa_segment) * x_vent[idx_vent-1]
                y[i] = alfa_segment * y_vent[idx_vent] + \
                    (1.0 - alfa_segment) * y_vent[idx_vent-1]



            elif (vent_flag == 3):

                i_segment = np.random.randint(n_vents-1, size=1)

                alfa_segment = np.random.uniform(0, 1, size=1)

                x[i] = alfa_segment * x_vent[i_segment] + \
                    (1.0 - alfa_segment) * x_vent[i_segment-1]
                y[i] = alfa_segment * y_vent[i_segment] + \
                    (1.0 - alfa_segment) * y_vent[i_segment-1]

        # Initialize distance from first lobe and number of descendents
        dist_int[i] = 0
        descendents[i] = 0

        if (plot_lobes_flag) or (plot_flow_flag):

            # plot the center of the first lobe
            plt.plot(x[i], y[i], 'o')

        # Compute the gradient of the topography(+ eventually the flow)

        xi = (x[i] - xmin)/cell
        yi = (y[i] - ymin)/cell

        # Index of the lower-left corner of the cell containing the point
        ix = np.floor(xi)
        iy = np.floor(yi)

        ix = ix.astype(int)
        iy = iy.astype(int)

        xi_fract = xi-ix
        yi_fract = yi-iy

        Fx_test = (yi_fract*(Ztot[iy+1, ix+1] - Ztot[iy+1, ix]) +
                   (1.0-yi_fract)*(Ztot[iy, ix+1] - Ztot[iy, ix])) / cell
        Fy_test = (xi_fract*(Ztot[iy+1, ix+1] - Ztot[iy, ix+1]) +
                   (1.0-xi_fract)*(Ztot[iy+1, ix] - Ztot[iy, ix])) / cell



        # (max_slope_angle,slope ) = slope_calc(Fy_test, Fx_test)

        ''' CONVERTED INTO A FUNCTION '''
        # major semi-axis direction
        max_slope_angle = np.mod(
            180 + (180 * np.arctan2(Fy_test, Fx_test) / pi), 360)

        # slope of the topography at (x[0],y[0])
        slope = np.sqrt(np.square(Fx_test)+np.square(Fy_test))
        ''' end '''

        # PERTURBE THE MAXIMUM SLOPE ANGLE ACCORDING TO PROBABILITY LAW

        # this expression define a coefficient used for the direction of the next slope
        if (max_slope_prob < 1):

            # rand_angle_new = get_rand_new_angle(slope)

            
            ''' CONVERTED INTO A FUNCTION '''
            # anle defining the direction of the new slope. when slope=0, then
            # we have an uniform distribution for the possible angles for the next lobe.

            slopedeg = 180.0 * np.arctan(slope) / pi

            if (slopedeg > 0.0) and (max_slope_prob > 0):

                sigma = (1.0 - max_slope_prob) / max_slope_prob * \
                    (90.0 - slopedeg) / slopedeg
                rand_angle_new = rtnorm.rtnorm(-180, 180, 0, sigma)

            else:

                rand = np.random.uniform(0, 1, size=1)
                rand_angle_new = 360.0 * np.abs(rand-0.5)

            ''' end '''

            angle[i] = max_slope_angle + rand_angle_new

        else:

            angle[i] = max_slope_angle

        # factor for the lobe eccentricity
        aspect_ratio = min(max_aspect_ratio, 1.0 + aspect_ratio_coeff * slope)

        # semi-axes of the lobe:
        # x1(i) is the major semi-axis of the lobe;
        # x2(i) is the minor semi-axis of the lobe.
        x1[i] = np.sqrt(lobe_area/np.pi) * np.sqrt(aspect_ratio)
        x2[i] = np.sqrt(lobe_area/np.pi) / np.sqrt(aspect_ratio)

        # (x1[i], x2[i])  = get_two_xi(slope)







