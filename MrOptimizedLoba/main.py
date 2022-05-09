from input_data_advanced import *
from input_data import *
from optimistic import main_program


if __name__ == "__main__":
    aList = []
    for i in range(5):
        elapsed = main_program(run_name, source, vent_flag, x_vent, y_vent, hazard_flag, masking_threshold, n_flows, min_n_lobes, max_n_lobes, volume_flag, total_volume, fixed_dimension_flag, lobe_area, thickness_ratio, topo_mod_flag, n_flows_counter, n_lobes_counter, thickening_parameter, lobe_exponent, max_slope_prob, inertial_exponent, restart_files, saveshape_flag, saveraster_flag, flag_threshold, plot_lobes_flag, plot_flow_flag, a_beta, b_beta, force_max_length, max_length,n_check_loop,start_from_dist_flag, dist_fact, npoints, aspect_ratio_coeff, max_aspect_ratio, shape_name)
        aList.append(elapsed)
        time = 0
        for x in aList:
            time += x
        print("Total elipsed time average ", time/len(aList))
