# from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
# from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
from linecache import getline
from scipy.stats import beta
from matplotlib.patches import Ellipse
# from matplotlib.path import Path
# import matplotlib.patches as patches
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import shapefile
import time
import os
import numpy.ma as ma
import sys
import shutil
import datetime
import rtnorm
from random import randrange
from os.path import exists
import gc


from input_data_advanced import *
from input_data import *

from multiprocessing import freeze_support
import concurrent.futures
    
from numba import vectorize, int64, float32, float64
from numba import jit
import math

# @jit(nopython=True)
# def slope_calc(Fy_test, Fx_test):
#      # major semi-axis direction
#     max_slope_angle = np.mod(
#         180 + (180 * np.arctan2(Fy_test, Fx_test) / np.pi), 360)

#     # slope of the topography at (x[0],y[0])
#     slope = np.sqrt(np.square(Fx_test)+np.square(Fy_test))

#     out = (max_slope_angle, slope)

#     return out




def add_Ellipse(ep):
    # == 2 is for the ellipses with edgecolor = 'r'
    if (ep[5] == 2):
        ellip = Ellipse([ep[0],ep[1]], 2*ep[2],2*ep[3], ep[4], facecolor = 'none',edgecolor='r')
    else: 
        ellip = Ellipse([ep[0],ep[1]], 2*ep[2],2*ep[3], ep[4], facecolor = 'none',edgecolor='k')     

    return ellip
    

def run_processes(ellipse_patches2):

    with concurrent.futures.ProcessPoolExecutor() as executor:
        # creating processes to run addEllipse in parallel
        results = executor.map(add_Ellipse, ellipse_patches2)
        # the results contain the ellipses already created and ready to add to the axis with ax.add_patch()
        return results


@jit(nopython=True)
def get_two_xi(slope):
    # factor for the lobe eccentricity
    aspect_ratio = min(max_aspect_ratio, 1.0 + aspect_ratio_coeff * slope)

    # semi-axes of the lobe:
    # x1(i) is the major semi-axis of the lobe;
    # x2(i) is the minor semi-axis of the lobe.
    xonei = np.sqrt(lobe_area/np.pi) * np.sqrt(aspect_ratio)
    xtwoi = np.sqrt(lobe_area/np.pi) / np.sqrt(aspect_ratio)
    out = (xonei, xtwoi)

    return out

@jit(nopython=True)
def get_two_xi(slope):
    # factor for the lobe eccentricity
    aspect_ratio = min(max_aspect_ratio, 1.0 + aspect_ratio_coeff * slope)

    # semi-axes of the lobe:
    # x1(i) is the major semi-axis of the lobe;
    # x2(i) is the minor semi-axis of the lobe.
    xonei = np.sqrt(lobe_area/np.pi) * np.sqrt(aspect_ratio)
    xtwoi = np.sqrt(lobe_area/np.pi) / np.sqrt(aspect_ratio)
    out = (xonei, xtwoi)

    return out


# @jit(nopython=True)
# def mul_n_arr(n, arr):
#     for i in range(arr.size):
#         arr[i] = arr[i]*n
#     return arr

# @jit(nopython=True)
# def add_n_arr(n, arr):
#     for i in range(arr.size):
#         arr[i] = arr[i]+n
#     return arr 

# @jit(nopython=True)
# def add_arrays(a,b):
#     for i in range(a.size):
#         a[i] = a[i] + b[i]
#     return a

# @jit(nopython=True)
# def sub_arrays(a,b):
#     for i in range(a.size):
#         a[i] = a[i] - b[i]
#     return a


# @jit(nopython=True)
# def ellipse( xc , yc , ax1 , ax2 , angle , X_circle , Y_circle ):
#     cos_angle = np.cos(angle*np.pi/180)
#     sin_angle = np.sin(angle*np.pi/180)

#     X = mul_n_arr(ax1, X_circle)
#     Y = mul_n_arr(ax2, Y_circle)

#     xe = add_n_arr(xc,sub_arrays(mul_n_arr(cos_angle,X), mul_n_arr(sin_angle,Y)))
#     ye = add_n_arr(yc, add_arrays(mul_n_arr(cos_angle,Y), mul_n_arr(sin_angle,X)))

#     return (xe,ye)



'''ELLIPSE WITH VECTORIZE START '''
# @vectorize([int64(int64,int64), float32(float32,float32), float64(float64,float64)], nopython=True)
# def multiply_array(n, arr):
#     return n*arr

# @vectorize([int64(int64,int64), float32(float32,float32), float64(float64,float64)], nopython=True)
# def add_array(n, arr):
#     return n+arr

# @vectorize([int64(int64,int64), float32(float32,float32), float64(float64,float64)], nopython=True)
# def sub_array(n, arr):
#     return n-arr

# @jit(nopython=True)
# def ellipse( xc , yc , ax1 , ax2 , angle , X_circle , Y_circle ):
#     cos_angle = math.cos(angle*np.pi/180)
#     sin_angle = math.sin(angle*np.pi/180)

#     # x1 = xc + ax1 * cos_angle
#     # y1 = yc + ax1 * sin_angle

#     # x2 = xc - ax2 * sin_angle
#     # y2 = yc + ax2 * cos_angle

#     X = multiply_array(ax1, X_circle)
#     Y = multiply_array(ax2, Y_circle)
#     # X = ax1 * X_circle
#     # Y = ax2 * Y_circle

#     xe = add_array(sub_array(multiply_array(X,cos_angle), multiply_array(Y,sin_angle)),xc)
#     ye = add_array(add_array(multiply_array(Y,cos_angle), multiply_array(X,sin_angle)),yc)
#     # xe = xc + X*cos_angle - Y*sin_angle
#     # ye = yc + X*sin_angle + Y*cos_angle

#     return (xe,ye)
'''ELLIPSE WITH VECTORIZE END '''


'''ELLIPSE WITH JIT ONLY START '''
@jit(nopython=True)
def ellipse( xc , yc , ax1 , ax2 , angle , X_circle , Y_circle ):

    cos_angle = np.cos(angle*np.pi/180)
    sin_angle = np.sin(angle*np.pi/180)

    # x1 = xc + ax1 * cos_angle
    # y1 = yc + ax1 * sin_angle

    # x2 = xc - ax2 * sin_angle
    # y2 = yc + ax2 * cos_angle

    X = ax1 * X_circle
    Y = ax2 * Y_circle

    xe = xc + X*cos_angle - Y*sin_angle
    ye = yc + X*sin_angle + Y*cos_angle

    return (xe,ye)
'''ELLIPSE WITH JIT ONLY END '''

'''ORIGINAL ELLIPSE START '''
# def ellipse( xc , yc , ax1 , ax2 , angle , X_circle , Y_circle ):

#     cos_angle = np.cos(angle*np.pi/180)
#     sin_angle = np.sin(angle*np.pi/180)

#     # x1 = xc + ax1 * cos_angle
#     # y1 = yc + ax1 * sin_angle

#     # x2 = xc - ax2 * sin_angle
#     # y2 = yc + ax2 * cos_angle

#     X = ax1 * X_circle
#     Y = ax2 * Y_circle

#     xe = xc + X*cos_angle - Y*sin_angle
#     ye = yc + X*sin_angle + Y*cos_angle

#     return (xe,ye)
'''ORIGINAL ELLIPSE END '''

def local_intersection(Xc_local,Yc_local,xc_e,yc_e,ax1,ax2,angle,xv,yv,nv2):

    # the accuracy of this procedure depends on the resolution of xv and yv
    # representing a grid of points [-0.5*cell;0.5*cell] X [-0.5*cell;0.5*cell]
    # built around the centers

    nx_cell = Xc_local.shape[0]
    ny_cell = Xc_local.shape[1]
 
    c = np.cos(angle*np.pi/180)
    s = np.sin(angle*np.pi/180)
   
    c1 = c/ax1
    s1 = s/ax1

    c2 = c/ax2
    s2 = s/ax2

    xv = xv-xc_e
    yv = yv-yc_e
   
    Xc_local_1d = Xc_local.ravel()
    Yc_local_1d = Yc_local.ravel()
               
    c1xv_p_s1yv = c1*xv + s1*yv
    c2yv_m_s2yv = c2*yv - s2*xv

    term1 = ( c1**2 + s2**2 ) * Xc_local_1d**2 
    term2 = ( 2*c1*s1 - 2*c2*s2 ) * Xc_local_1d * Yc_local_1d
    term3 = np.tensordot( Xc_local_1d , 2*c1*c1xv_p_s1yv - 2*s2*c2yv_m_s2yv , 0 )
    term4 = ( c2**2 + s1**2 ) * Yc_local_1d**2
    term5 = np.tensordot( Yc_local_1d , 2*c2*c2yv_m_s2yv + 2*s1*c1xv_p_s1yv , 0 )
    term6 = c1xv_p_s1yv**2 + c2yv_m_s2yv**2

    term124 = term1+term2+term4
    term356 = term3+term5+term6

    term_tot = term124+term356.transpose()

    inside = ( term_tot <=1 )

    area_fract_1d = np.sum(inside.astype(float),axis=0)

    area_fract_1d /= nv2 

    area_fract = area_fract_1d.reshape(nx_cell,ny_cell)
    
    return (area_fract)


if __name__ == '__main__':
    # freeze support is only required for windows (usually) to run multiprocessing
    freeze_support()
    # Main start here

    print ("")
    print ("Mr Lava Loba by M.de' Michieli Vitturi and S.Tarquini")
    print ("")


    # read the run parameters form the file inpot_data.py

    filling_parameter = 1.0 - thickening_parameter

    n_vents = len(x_vent)


    if (('x_vent_end' in globals()) and (len(x_vent_end) > 0) and (vent_flag > 3)):

        first_j = 0
        cum_fiss_length = np.zeros(n_vents+1)

    else:

        first_j = 1
        cum_fiss_length = np.zeros(n_vents)

    for j in range(first_j,n_vents):

        if (('x_vent_end' in globals()) and (len(x_vent_end) > 0) and (vent_flag > 3)):

            delta_xvent = x_vent_end[j] - x_vent[j]
            delta_yvent = y_vent_end[j] - y_vent[j]

            cum_fiss_length[j+1] = cum_fiss_length[j] + np.sqrt( delta_xvent**2 + delta_yvent**2 )
    
        else:

            delta_xvent =  x_vent[j] - x_vent[j-1]
            delta_yvent =  y_vent[j] - y_vent[j-1]

            cum_fiss_length[j] = cum_fiss_length[j-1] + np.sqrt( delta_xvent**2 + delta_yvent**2 )

    if ('fissure_probabilities' in globals()):

        if ( vent_flag == 8 ):

            cum_fiss_length = np.cumsum(fissure_probabilities)

        elif ( vent_flag > 5):

            cum_fiss_length[1:] = np.cumsum(fissure_probabilities)


    if ( n_vents >1 ):
        cum_fiss_length = cum_fiss_length.astype(float) / cum_fiss_length[-1]


    # print(cum_fiss_length)

    #search if another run with the same base name already exists
    i = 0

    condition = True

    base_name = run_name

    while condition:
        
        run_name = base_name + '_{0:03}'.format(i) 

        backup_advanced_file = run_name + '_advanced_inp.bak'
        backup_file = run_name + '_inp.bak'

        condition = os.path.isfile(backup_file)

        i = i + 1

    # create a backup file of the input parameters
    shutil.copy2('input_data_advanced.py', backup_advanced_file)
    shutil.copy2('input_data.py', backup_file)

    print ('Run name',run_name)
    print ('')

    if ( plot_flow_flag ) or ( plot_lobes_flag):
        #  create plot
        fig     = plt.figure()
        ax      = fig.add_subplot(111)


    if ( len(shape_name) > 0 ): 

        # read the shapefile
        sf = shapefile.Reader(shape_name)
        recs    = sf.records()
        shapes  = sf.shapes()
        Nshp    = len(shapes)

        cm    = plt.get_cmap('Dark2')
        cccol = cm(1.*np.arange(Nshp)/Nshp)

        for nshp in xrange(Nshp):

            ptchs   = []
            pts     = np.array(shapes[nshp].points)
            prt     = shapes[nshp].parts
            par     = list(prt) + [pts.shape[0]]

            for pij in xrange(len(prt)):
                ptchs.append(Polygon(pts[par[pij]:par[pij+1]]))
        
            ax.add_collection(PatchCollection(ptchs,facecolor=cccol[nshp,:],edgecolor='k', linewidths=.1))


    print ('')

    if ( a_beta == 0 ) and ( b_beta == 0 ):

        alloc_n_lobes = int(max_n_lobes)

    else:

        x_beta = np.rint( range(0,n_flows) ) / ( n_flows - 1 )

        beta_pdf = beta.pdf( x_beta , a_beta , b_beta )

        alloc_n_lobes = int( np.rint( min_n_lobes + 0.5 * ( max_n_lobes - min_n_lobes) \
                                    * np.max( beta_pdf ) ) )

        print ('Flow with the maximum number of lobes',np.argmax( beta_pdf))

    print ('Maximum number of lobes',alloc_n_lobes)


    # initialize the arrays for the lobes variables
    angle = np.zeros(alloc_n_lobes)
    x = np.zeros(alloc_n_lobes)
    y = np.zeros(alloc_n_lobes)
    x1 = np.zeros(alloc_n_lobes)
    x2 = np.zeros(alloc_n_lobes)
    h = np.zeros(alloc_n_lobes)

    dist_int = np.zeros(alloc_n_lobes, dtype=int)-1
    descendents = np.zeros(alloc_n_lobes, dtype=int)
    parent = np.zeros(alloc_n_lobes, dtype=int)
    alfa_inertial = np.zeros(alloc_n_lobes)

    if ( volume_flag == 1 ):

        if ( fixed_dimension_flag == 1 ):
            print("total_volume", total_volume, "n_flows", n_flows, "lobe_area", lobe_area, "min_n_lobes", min_n_lobes, "max_n_lobes", max_n_lobes)
            avg_lobe_thickness = total_volume / ( n_flows * lobe_area * 0.5 * ( min_n_lobes + max_n_lobes ) )    
            sys.stdout.write("Average Lobe thickness = %f m\n\n" % (avg_lobe_thickness))

        elif ( fixed_dimension_flag == 2 ):

            lobe_area = total_volume / ( n_flows * avg_lobe_thickness * 0.5 * ( min_n_lobes + max_n_lobes ) )    
            sys.stdout.write("Lobe area = %f m2\n\n" % (lobe_area))
            

    # Needed for numpy conversions
    deg2rad = np.pi / 180.0
    rad2deg = 180.0 / np.pi


    # Define variables needed to build the ellipses
    t = np.linspace(0.0,2.0*np.pi,npoints)
    X_circle = np.cos(t)
    Y_circle = np.sin(t)


    # Parse the header using a loop and
    # the built-in linecache module
    hdr = [getline(source, i) for i in range(1,7)]
    values = [float(h.split(" ")[-1].strip()) for h in hdr]
    del hdr

    cols,rows,lx,ly,cell,nd = values
    del values

    cols = int(cols)
    rows = int(rows)

    crop_flag = ( "west_to_vent" in locals() ) and ( "east_to_vent" in locals() ) \
            and ( "south_to_vent" in locals() ) and ( "north_to_vent" in locals() )

    print('Crop flag = ',crop_flag)

    if sys.version_info >= (3, 0):
        start = time.process_time()
    else:
        start = time.clock()

    source_npy = source.replace(".asc",".npy")

    if os.path.isfile(source_npy):
        print (source_npy," exists")
    else:
        print (source_npy," does not exist")
        data = np.loadtxt(source, skiprows=6)
        np.save(source_npy, data)
        del data
        

    if crop_flag:

        # Load the dem into a numpy array
        arr_temp = np.flipud(np.load(source_npy))

        # the values are associated to the center of the pixels
        xc_temp = lx + cell*(0.5+np.arange(0,arr_temp.shape[1]))
        yc_temp = ly + cell*(0.5+np.arange(0,arr_temp.shape[0]))

        # crop the DEM to the desired domain
        iW = np.maximum(0,(np.floor((np.min(x_vent)-west_to_vent-lx)/cell)).astype(int))
        iE = np.minimum(cols,(np.ceil((np.max(x_vent)+east_to_vent-lx)/cell)).astype(int))
        jS = np.maximum(0,(np.floor((np.min(y_vent)-south_to_vent-ly)/cell)).astype(int))
        jN = np.minimum(rows,(np.ceil((np.max(y_vent)+north_to_vent-ly)/cell)).astype(int))
        
        print('Cropping of original DEM')
        print('iW,iE,jS,jN',iW,iE,jS,jN)
        print('')


        arr = arr_temp[jS:jN,iW:iE]
        xc = xc_temp[iW:iE]
        yc = yc_temp[jS:jN]

        lx = xc[0] - 0.5*cell
        ly = yc[0] - 0.5*cell

        nx = arr.shape[1]
        ny = arr.shape[0]

        header = "ncols     %s\n" % arr.shape[1]
        header += "nrows    %s\n" % arr.shape[0]
        header += "xllcorner " + str(lx) +"\n"
        header += "yllcorner " + str(ly) +"\n"
        header += "cellsize " + str(cell) +"\n"
        header += "NODATA_value " + str(nd) +"\n"

        output_DEM = run_name + '_DEM.asc'

        np.savetxt(output_DEM, np.flipud(arr), header=header, fmt='%1.5f',comments='')

        del arr_temp
        del xc_temp
        del yc_temp
        gc.collect()

    else:

        # Load the dem into a numpy array
        arr = np.flipud(np.load(source_npy))

        nx = arr.shape[1]
        ny = arr.shape[0]

        # the values are associated to the center of the pixels
        xc = lx + cell*(0.5+np.arange(0,nx))
        yc = ly + cell*(0.5+np.arange(0,ny))

    gc.collect()


    if sys.version_info >= (3, 0):
        elapsed = (time.process_time() - start)
    else:
        elapsed = (time.clock() - start)

    print('Time to read DEM '+str(elapsed)+'s')

    xcmin = np.min(xc)
    xcmax = np.max(xc)

    ycmin = np.min(yc)
    ycmax = np.max(yc)

    Xc,Yc = np.meshgrid(xc,yc)

    Zc = np.zeros((ny,nx))
    np.copyto(Zc,arr)

    # load restart files (if existing) 
    for i_restart in range(0,len(restart_files)): 

        Zflow_old = np.zeros((ny,nx))

        source = restart_files[i_restart]
        file_exists = exists(source)
        if not file_exists:
            print(source + ' not found.')
            quit()
        
        hdr = [getline(source, i) for i in range(1,7)]
        try:
            values = [float(h.split(" ")[-1].strip()) for h in hdr]
        except:
            print("An problem occurred with header of file ",source)
            print(hdr)
        
        cols,rows,lx,ly,cell,nd = values    

        # Load the previous flow thickness into a numpy array
        arr = np.loadtxt(source, skiprows=6)
        arr[arr==nd] = 0.0

        Zflow_old = np.flipud(arr)

        # Load the relevant filling_parameter (to account for "subsurface flows")
        filling_parameter_i = restart_filling_parameters[i_restart]
        
        Zc = Zc + (Zflow_old * filling_parameter_i)


    # Define a small grid for lobe-cells intersection
    nv = 15
    xv,yv = np.meshgrid(np.linspace(-0.5*cell,0.5*cell, nv),np.linspace(-0.5*cell,0.5*cell, nv))
    # xv,yv = np.meshgrid(np.linspace(0.0,cell, nv),np.linspace(0.0,cell, nv))
    xv = np.reshape(xv,-1)
    yv = np.reshape(yv,-1)
    nv2 = nv*nv

    # Create a simple contour plot with labels using default colors.  The
    # inline argument to clabel will control whether the labels are draw
    # over the line segments of the contour, removing the lines beneath
    # the label

    if ( plot_lobes_flag ) or ( plot_flow_flag):

        plt.contour(Xc, Yc, Zc,150)

        plt.savefig('fig_map.png')


    Ztot = np.zeros((ny,nx))

    # the first argument is the destination, the second is the source
    np.copyto(Ztot,Zc)
        
    Zflow = np.zeros((ny,nx))

    max_semiaxis = np.sqrt( lobe_area * max_aspect_ratio / np.pi )
    max_cells = np.ceil( 2.0 * max_semiaxis / cell ) + 2
    max_cells = max_cells.astype(int)

    print ('max_semiaxis',max_semiaxis)
    print ('max_cells',max_cells)

    jtop_array = np.zeros(alloc_n_lobes, dtype=int)
    jbottom_array = np.zeros(alloc_n_lobes, dtype=int)

    iright_array = np.zeros(alloc_n_lobes, dtype=int)
    ileft_array =np.zeros(alloc_n_lobes, dtype=int)


    Zhazard = np.zeros((ny,nx), dtype=int)
    Zhazard_temp = np.zeros((ny,nx), dtype=int)

    Zdist = np.zeros((ny,nx),dtype=int) + 9999
    
    if ( saveshape_flag ):
        
        # create the Polygon shapefile
        w = shapefile.Writer(shapefile.POLYGON)
        w.autoBalance = 1
        # the field
        w.field('ID','N','40')
        w.field('DIST_INT','N','40')
        w.field('DESCENDENTS','N','40')
        w.field('PARENT','N','40')
        w.field('FLOW','N','40')


    patch = []


    print ('End pre-processing')
    print ('')


    if sys.version_info >= (3, 0):
        start = time.process_time()
    else:
        start = time.clock()


    est_rem_time = ''

    n_lobes_tot = 0


    ''' THESE 3 LISTS ARE ONLY REQUIRED FOR THE PARALLEL VERSION OF ELLIPSE CREATION (refer to README.md for more info)'''
    if plot_parallel == 1 and plot_lobes_flag:
        to_plot_centers = []
        to_ellipse_patch = []
        to_ellipse_patch2 = []

    for flow in range(0,n_flows):

        Zflow_local_array = np.zeros((alloc_n_lobes,max_cells,max_cells),dtype=int)
        descendents = np.zeros(alloc_n_lobes, dtype=int)

        i_first_check = n_check_loop

        if ( a_beta == 0 ) and ( b_beta == 0 ):
            
            # DEFINE THE NUMBER OF LOBES OF THE FLOW (RANDOM VALUE BETWEEN MIN AND MAX)
            n_lobes = int( np.ceil( np.random.uniform(min_n_lobes, max_n_lobes, size=1) ))

        else:

            x_beta = ( 1.0 * flow ) / ( n_flows - 1 )
            n_lobes = int( np.rint( min_n_lobes + 0.5 * ( max_n_lobes - min_n_lobes ) \
                                    * beta.pdf( x_beta , a_beta , b_beta ) ) )

        n_lobes_tot = n_lobes_tot + n_lobes

        thickness_min = 2.0 * thickness_ratio / ( thickness_ratio + 1.0 ) * avg_lobe_thickness
        delta_lobe_thickness = 2.0 * ( avg_lobe_thickness - thickness_min ) / ( n_lobes - 1.0 )

        # print ('n_lobes',n_lobes)
        # print ('thickness_min',thickness_min)
        # print ('delta_lobe_thickness',delta_lobe_thickness)

        if ( n_flows > 1 and not ('SLURM_JOB_NAME' in os.environ.keys())):
            # print on screen bar with percentage of flows computed
            last_percentage_5 = np.rint(flow*20.0/(n_flows)).astype(int)
            last_percentage = np.rint(flow*100.0/(n_flows))
            last_percentage = np.rint(flow*100.0/(n_flows))
            last_percentage = last_percentage.astype(int)
            sys.stdout.write('\r')
            sys.stdout.write("[%-20s] %d%% %s" % ('='*(last_percentage_5), last_percentage, est_rem_time))
            sys.stdout.flush()
        
        for i in range(0,n_init):

            if ( n_flows == 1 and not ('SLURM_JOB_NAME' in os.environ.keys())):
                # print on screen bar with percentage of flows computed
                last_percentage = np.rint(i*20.0/(n_lobes-1))*5
                last_percentage = last_percentage.astype(int)

                sys.stdout.write('\r')
                sys.stdout.write("[%-20s] %d%%" % ('='*(last_percentage/5), last_percentage))
                sys.stdout.flush()
            else:
                pass

            # STEP 0: COMPUTE THE FIRST LOBES OF EACH FLOW
        
            if ( n_vents == 1 ):

                x[i] = x_vent[0]
                y[i] = y_vent[0]
    
            else:

                if ( vent_flag == 0 ):

                    # vent_flag = 0  => the initial lobes are on the vents coordinates
                    #                   and the flows start initially from the first vent,
                    #                   then from the second and so on.

                    i_vent = int(np.floor( flow * n_vents / n_flows ) )

                    x[i] = x_vent[i_vent]
                    y[i] = y_vent[i_vent]

                elif ( vent_flag == 1 ):

                    # vent_flag = 1  => the initial lobes are chosen randomly from the vents
                    #                   coordinates and each vent has the same probability

                    i_vent = np.random.randint(n_vents, size=1)

                    x[i] = x_vent[int(i_vent)]
                    y[i] = y_vent[int(i_vent)]

                elif ( (vent_flag == 2) or (vent_flag==6) ):

                    # vent_flag = 2  => the initial lobes are on the polyline connecting
                    #                   the vents and all the point of the polyline
                    #                   have the same probability

                    # vent_flag = 6  => the initial lobes are on the polyline connecting
                    #                   the vents and the probability of
                    #                   each segment is fixed in the input file

                    alfa_polyline = np.random.uniform(0, 1, size=1)

                    idx_vent = np.argmax(cum_fiss_length>alfa_polyline)

                    num = alfa_polyline - cum_fiss_length[idx_vent-1]
                    den = cum_fiss_length[idx_vent] - cum_fiss_length[idx_vent-1]

                    alfa_segment = num / den

                    x[i] = alfa_segment * x_vent[idx_vent] + \
                        ( 1.0 - alfa_segment ) * x_vent[idx_vent-1] 

                    y[i] = alfa_segment * y_vent[idx_vent] + \
                        ( 1.0 - alfa_segment ) * y_vent[idx_vent-1]
                

                elif ( vent_flag == 3 ):

                    # vent_flag = 3  => the initial lobes are on the polyline connecting
                    #                   the vents and all the segments of the polyline
                    #                   have the same probability

                    i_segment = randrange(n_vents)
                
                    alfa_segment = np.random.uniform(0, 1, size=1)
                
                    x[i] = alfa_segment * x_vent[i_segment] + \
                        ( 1.0 - alfa_segment ) * x_vent[i_segment-1] 

                    y[i] = alfa_segment * y_vent[i_segment] + \
                        ( 1.0 - alfa_segment ) * y_vent[i_segment-1]

                elif ( (vent_flag == 4) or (vent_flag == 7) ):

                    # vent_flag = 4  => the initial lobes are on multiple
                    #                   fissures and all the point of the fissures
                    #                   have the same probability

                    # vent_flag = 7  => the initial lobes are on multiple
                    #                   fissures and the probability of
                    #                   each fissure is fixed in the input file


                    alfa_polyline = np.random.uniform(0, 1, size=1)

                    idx_vent = np.argmax(cum_fiss_length>alfa_polyline)

                    num = alfa_polyline - cum_fiss_length[idx_vent-1]
                    den = cum_fiss_length[idx_vent] - cum_fiss_length[idx_vent-1]

                    alfa_segment = num / den
                    print()
                    print(idx_vent-1,alfa_segment)

                    x[i] = alfa_segment * x_vent_end[idx_vent-1] + \
                        ( 1.0 - alfa_segment ) * x_vent[idx_vent-1] 

                    y[i] = alfa_segment * y_vent_end[idx_vent-1] + \
                        ( 1.0 - alfa_segment ) * y_vent[idx_vent-1]
                
                elif ( vent_flag == 5 ):

                    # vent_flag = 5  => the initial lobes are on multiple
                    #                   fissures and all the fissures
                    #                   have the same probability

                    i_segment = randrange(n_vents)

                    alfa_segment = np.random.uniform(0, 1, size=1)

                    x[i] = alfa_segment * x_vent_end[i_segment] + \
                        ( 1.0 - alfa_segment ) * x_vent[i_segment] 

                    y[i] = alfa_segment * y_vent_end[i_segment] + \
                        ( 1.0 - alfa_segment ) * y_vent[i_segment]

                elif ( vent_flag == 8 ):

                    # vent_flag = 1  => the initial lobes are chosen randomly from the vents
                    #                   coordinates and each vent has the same probability

                    alfa_vent = np.random.uniform(0, 1, size=1)
                    i_vent = np.argmax(cum_fiss_length>alfa_vent)


                    x[i] = x_vent[int(i_vent)]
                    y[i] = y_vent[int(i_vent)]


            # initialize distance from first lobe and number of descendents        
            dist_int[i] = 0
            descendents[i] = 0
            
            # inside for i in range(0,n_init):
            if ( plot_lobes_flag ) or ( plot_flow_flag):
                if plot_parallel == 1:
                    to_plot_centers.append([x[i],y[i]])
                else:
                    # plot the center of the first lobe        
                    plt.plot(x[i],y[i],'o')
            
            # compute the gradient of the topography(+ eventually the flow)
            # here the centered grid is used (Z values saved at the centers of the pixels)
            # xc[ix] < lobe_center_x < xc[ix1]
            # yc[iy] < lobe_center_y < yc[iy1]
            xi = (x[i] - xcmin)/cell
            yi = (y[i] - ycmin)/cell

            ix = np.floor(xi)
            iy = np.floor(yi)

            ix = ix.astype(int)
            iy = iy.astype(int)

            # compute the baricentric coordinated of the lobe center in the pixel
            # 0 < xi_fract < 1
            # 0 < yi_fract < 1
            xi_fract = xi-ix
            yi_fract = yi-iy

            # interpolate the slopes at the edges of the pixel to find the slope at the center of the lobe
            Fx_test = ( yi_fract*( Ztot[iy+1,ix+1] - Ztot[iy+1,ix] ) + \
                    (1.0-yi_fract)*( Ztot[iy,ix+1] - Ztot[iy,ix] ) ) / cell

            Fy_test = ( xi_fract*( Ztot[iy+1,ix+1] - Ztot[iy,ix+1] ) + \
                    (1.0-xi_fract)*( Ztot[iy+1,ix] - Ztot[iy,ix] ) ) / cell

        

            # ( max_slope_angle,slope ) = slope_calc(Fy_test, Fx_test)
            ''' CONVERTED INTO A FUNCTION '''
            # major semi-axis direction
            max_slope_angle = np.mod(180.0 + ( 180.0 * np.arctan2(Fy_test,Fx_test) / np.pi ),360.0)
            
            # slope of the topography at (x[0],y[0])
            slope = np.sqrt(np.square(Fx_test)+np.square(Fy_test))
            ''' END '''

            # PERTURBE THE MAXIMUM SLOPE ANGLE ACCORDING TO PROBABILITY LAW
            
            # this expression define a coefficient used for the direction of the next slope
            if ( max_slope_prob < 1 ):

                # angle defining the direction of the new slope. when slope=0, then
                # we have an uniform distribution for the possible angles for the next lobe.  

                slopedeg = 180.0 * np.arctan(slope) / np.pi

                if ( slopedeg > 0.0 ) and ( max_slope_prob > 0 ):

                    sigma = (1.0 - max_slope_prob ) / max_slope_prob * ( 90.0 - slopedeg ) / slopedeg
                    rand_angle_new = rtnorm.rtnorm(-180,180,0,sigma)

                else:

                    rand = np.random.uniform(0, 1, size=1)
                    rand_angle_new = 360.0 * np.abs( rand-0.5 )

                angle[i] = max_slope_angle + rand_angle_new

            else:

                angle[i] = max_slope_angle
            

            (x1[i], x2[i])  = get_two_xi(slope)
            ''' CONVERTED INTO A FUNCTION '''
            # # factor for the lobe eccentricity
            # aspect_ratio = min(max_aspect_ratio,1.0 + aspect_ratio_coeff * slope)

            # # semi-axes of the lobe:
            # # x1(i) is the major semi-axis of the lobe;
            # # x2(i) is the minor semi-axis of the lobe.
            # x1[i] = np.sqrt(lobe_area/np.pi) * np.sqrt(aspect_ratio)
            # x2[i] = np.sqrt(lobe_area/np.pi) / np.sqrt(aspect_ratio)
            ''' end '''




            # inside for i in range(0,n_init): 
            if ( plot_lobes_flag ):
                if plot_parallel == 1:
                    to_ellipse_patch.append([x[i], y[i], x1[i], x2[i], angle[i], 1])
                else: 
                    patch.append(Ellipse([x[i],y[i]], 2*x1[i], 2*x2[i], angle[i], facecolor = 'none',edgecolor='k'))


            # print("Line 801 (PLOTTING  took ", plotting_time )
            if ( saveraster_flag == 1 ):
                
                # compute the points of the lobe
                [ xe , ye ] = ellipse( x[i] , y[i] , x1[i] , x2[i] , angle[i] , X_circle , Y_circle )
                
                # bounding box for the lobe (xc[i_left]<xe<xc[i_right];yc[j_bottom]<ye<yc[j_top])
                # the indexes are referred to the centers of the pixels
                min_xe = np.min(xe)
                max_xe = np.max(xe)
            
                min_ye = np.min(ye)
                max_ye = np.max(ye)

                xi = (min_xe - xcmin)/cell
                ix = np.floor(xi)
                i_left = ix.astype(int)

                xi = (max_xe - xcmin)/cell
                ix = np.floor(xi)
                i_right = ix.astype(int)+2

                yj = (min_ye - ycmin)/cell
                jy = np.floor(yj)
                j_bottom = jy.astype(int)            

                yj = (max_ye - ycmin)/cell
                jy = np.floor(yj)
                j_top = jy.astype(int)+2            

                # define the subgrid of pixels to check for coverage
                Xc_local = Xc[j_bottom:j_top,i_left:i_right]
                Yc_local = Yc[j_bottom:j_top,i_left:i_right]

                # compute the fraction of cells covered by the lobe (local indexing)
                # for each pixel a square [-0.5*cell;0.5*cell] X [-0.5*cell;0.5*cell]
                # is built around its center to compute the intersection with the lobe
                # the coverage values are associated to each pixel (at the center)
                area_fract = local_intersection(Xc_local,Yc_local,x[i],y[i],x1[i],x2[i],angle[i],xv,yv,nv2)
                Zflow_local = area_fract

                # compute also as integer (0=pixel non covereb by lobe;1=pixel covered by lobe)
                Zflow_local_int = np.ceil(area_fract)
                Zflow_local_int = Zflow_local_int.astype(int)

                # compute the thickness of the lobe
                lobe_thickness = thickness_min + ( i-1 ) * delta_lobe_thickness

                # update the thickness of the flow with the new lobe
                Zflow[j_bottom:j_top,i_left:i_right] += lobe_thickness * Zflow_local

                # update the topography  
                
                ### change 2022/01/13
                # FROM HERE 
                Ztot[j_bottom:j_top,i_left:i_right] += filling_parameter * lobe_thickness * Zflow_local
                
                # TO HERE

                # compute the new minimum "lobe distance" of the pixels from the vent
                Zdist_local = Zflow_local_int * dist_int[i] + 9999 * ( Zflow_local == 0 )

                Zdist[j_bottom:j_top,i_left:i_right] = np.minimum( Zdist[j_bottom:j_top,i_left:i_right] \
                                                                , Zdist_local )

                # store the bounding box of the new lobe
                jtop_array[i] = j_top
                jbottom_array[i] = j_bottom
                
                iright_array[i] = i_right
                ileft_array[i] = i_left

                if ( hazard_flag ):

                    # store the local array of integer coverage in the global array
                    Zflow_local_array[i,0:j_top-j_bottom,0:i_right-i_left] = Zflow_local_int
                    
            if ( saveshape_flag ):
                # compute the lobe
                [ xe , ye ] = ellipse( x[i] , y[i] , x1[i] , x2[i] , angle[i] , X_circle , Y_circle )

                shape_verts = np.zeros((npoints-1, 2))

                shape_verts[0:npoints-1,0] = xe[0:npoints-1]
                shape_verts[0:npoints-1,1] = ye[0:npoints-1]

                w.poly(parts=[shape_verts.tolist()])
                w.record(str(i+1),str(dist_int[i]),str(descendents[i]),str(0),str(flow+1))

        last_lobe = n_lobes

        ''' for i in range(n_init,n_lobes): start '''
        for i in range(n_init,n_lobes):

            #print('i',i)

            if ( n_flows == 1 and not 'SLURM_JOB_NAME' in os.environ.keys()):
                # print on screen bar with percentage of flows computed
                last_percentage = np.rint(i*20.0/(n_lobes-1))*5
                sys.stdout.write('\r')
                sys.stdout.write("[%-20s] %d%%" % ('='*(last_percentage/5), last_percentage))
                sys.stdout.flush()


            # STEP 0: DEFINE THE INDEX idx OF THE PARENT LOBE

            if ( lobe_exponent > 0 ):

                idx0 = np.random.uniform(0, 1, size=1)
                
                idx1 = idx0 ** lobe_exponent

                if ( force_max_length ):

                    # the parent lobe is chosen only among those with
                    # dist smaller than the maximum value fixed in input 
                    mask = dist_int[0:i] < max_length

                    idx2 = sum( mask[0:i] ) * idx1 

                    idx3 = np.floor( idx2 )
                
                    idx = int(idx3)

                    sorted_dist = np.argsort(dist_int[0:i])
                        
                    idx = sorted_dist[idx]

                else:

                    # the parent lobe is chosen among all the lobes
                    
                    idx2 = i * idx1 
                
                    idx3 = np.floor( idx2 )
                
                    idx = int(idx3)
                
                if ( start_from_dist_flag ):
                    
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

            for j in range(0,dist_int[idx]+1):

                previous = parent[last]
                descendents[previous] = descendents[previous]+1
                last = previous


            # local slope of the topography. The slope affects both the location of 
            # the new lobe on the boundary of the previous one and its aspect
            # ratio:
            # if slope = 0 the lobe is a circle (x1=x2);
            # if slope > 1 the lobe is an ellipse.

            
            # STEP 1: COMPUTE THE SLOPE AND THE MAXIMUM SLOPE ANGLE
            # here the centered grid is used (Z values saved at the centers of the pixels)
            # xc[ix] < lobe_center_x < xc[ix1]
            # yc[iy] < lobe_center_y < yc[iy1]
            xi = (x[idx] - xcmin)/cell
            yi = (y[idx] - ycmin)/cell

            ix = np.floor(xi)
            iy = np.floor(yi)

            ix = ix.astype(int)
            iy = iy.astype(int)

            ix1 = ix+1
            iy1 = iy+1

            # stopping condition (lobe close the domain boundary)
            if ( ix <= 0.5 * max_cells ) or ( ix1 >= (nx - 0.5*max_cells) ) or \
            ( iy <= 0.5 * max_cells ) or ( iy1 >= (ny - 0.5*max_cells) ) or \
            ( Zc[iy,ix] == nd ) or ( Zc[iy1,ix1] == nd ) or \
            ( Zc[iy,ix1] == nd ) or ( Zc[iy1,ix] == nd ):

                last_lobe = i-1
                break

            
            # compute the baricentric coordinated of the lobe center in the pixel
            # 0 < xi_fract < 1
            # 0 < yi_fract < 1
            xi_fract = xi-ix
            yi_fract = yi-iy

            # interpolate the elevation at the corners of the pixel to find the elevation at the center of the lobe
            zidx = xi_fract * ( yi_fract * Ztot[iy1,ix1] + (1.0-yi_fract) * Ztot[iy,ix1] ) \
                + (1.0-xi_fract) * ( yi_fract * Ztot[iy1,ix] + (1.0-yi_fract) * Ztot[iy,ix] )
            """
            # interpolate the slopes at the edges of the pixel to find the slope at the center of the lobe
            Fx_lobe = ( yi_fract * ( Ztot[iy1,ix1] - Ztot[iy1,ix] ) \
                        + (1.0-yi_fract) * ( Ztot[iy,ix1] - Ztot[iy,ix] ) ) / cell

            Fy_lobe = ( xi_fract * ( Ztot[iy1,ix1] - Ztot[iy,ix1] ) \
                        + (1.0-xi_fract) * ( Ztot[iy1,ix] - Ztot[iy,ix] ) ) / cell


            slope = np.sqrt(np.square(Fx_lobe)+np.square(Fy_lobe))
            # angle defining the direction of maximum slope (max_slope_angle = aspect)
            max_slope_angle = np.mod(180 + ( 180 * np.arctan2(Fy_lobe,Fx_lobe) / np.pi ),360.0)
            """
            
            # compute the lobe (npoints on the ellipse) 
            '''HELLO YES HELP'''
            [ xe , ye ] = ellipse( x[idx] , y[idx] , x1[idx] , x2[idx] , angle[idx] , X_circle , Y_circle )

            # For all the points of the ellipse compute the indexes of the pixel containing the points.
            # This is done with respect to the centered grid. We want to interpolate from the centered
            # values (elevation) to the location of the points on the ellipse)
            xei = (xe - xcmin)/cell
            yei = (ye - ycmin)/cell

            ixe = np.floor(xei)
            iye = np.floor(yei)

            ixe = ixe.astype(int)
            iye = iye.astype(int)

            ixe1 = ixe+1
            iye1 = iye+1

            # compute the local coordinates of the points (0<x,y<1) within the pixels containing them
            xei_fract = xei-ixe
            yei_fract = yei-iye

            # interpolate the grid values to find the elevation at the ellipse points
            ze = xei_fract * ( yei_fract * Ztot[iye1,ixe1] + (1.0-yei_fract) * Ztot[iye,ixe1] ) \
                + (1.0-xei_fract) * ( yei_fract * Ztot[iye1,ixe] + (1.0-yei_fract) * Ztot[iye,ixe] )

            # find the point on the ellipse with minimum elevation
            idx_min = np.argmin(ze)

            # compute the vector from the center of the lobe to the point of minimum z on the boundary
            Fx_lobe = x[idx] - xe[idx_min]
            Fy_lobe = y[idx] - ye[idx_min]

            # compute the slope and the angle
            slope = np.maximum( 0.0 , ( zidx - ze[idx_min] ) / \
                    ( np.sqrt(np.square(Fx_lobe)+np.square(Fy_lobe) ) ) )

            max_slope_angle = np.mod(180.0 + ( 180.0 * np.arctan2(Fy_lobe,Fx_lobe) / np.pi ),360.0)
            
            # STEP 2: PERTURBE THE MAXIMUM SLOPE ANGLE ACCORDING TO PROBABILITY LAW
            
            # this expression define a coefficient used for the direction of the next slope
            if ( max_slope_prob < 1 ):

                # angle defining the direction of the new slope. when slope=0, then
                # we have an uniform distribution for the possible angles for the next lobe.  

                slopedeg = 180.0 * np.arctan(slope) / np.pi

                if ( slopedeg > 0.0 ) and ( max_slope_prob > 0.0 ):

                    sigma = (1.0 - max_slope_prob ) / max_slope_prob * ( 90.0 - slopedeg ) / slopedeg
                    rand_angle_new = rtnorm.rtnorm(-180.0,180.0,0.0,sigma)

                else:

                    rand = np.random.uniform(0, 1, size=1)
                    rand_angle_new = 360.0 * np.abs( rand-0.5 )

                new_angle = max_slope_angle + rand_angle_new[0]

            else:

                new_angle = max_slope_angle
            


            # STEP 3: ADD THE EFFECT OF INERTIA
            
            # cos and sin of the angle of the parent lobe
            cos_angle1 = np.cos(angle[idx]*deg2rad)
            sin_angle1 = np.sin(angle[idx]*deg2rad)

            # cos and sin of the angle of maximum slope
            cos_angle2 = np.cos(new_angle*deg2rad)
            sin_angle2 = np.sin(new_angle*deg2rad)

            if ( inertial_exponent == 0 ): 

                alfa_inertial[i] = 0.0

            else:

                alfa_inertial[i] = ( 1.0 - (2.0 * np.arctan(slope) / np.pi)**inertial_exponent ) \
                                ** ( 1.0 / inertial_exponent )

            x_avg = ( 1.0 - alfa_inertial[i] ) * cos_angle2 + alfa_inertial[i] * cos_angle1
            y_avg = ( 1.0 - alfa_inertial[i] ) * sin_angle2 + alfa_inertial[i] * sin_angle1

            angle_avg = np.mod(180 * np.arctan2(y_avg,x_avg) / np.pi , 360)   

            new_angle = angle_avg

            # STEP 4: DEFINE THE SEMI-AXIS OF THE NEW LOBE

            # a define the ang.coeff. of the line defining the location of the
            # center of the new lobe in a coordinate system defined by the
            # semi-axes of the existing lobe
            a = np.tan(deg2rad*(new_angle-angle[idx]))
            
            # xt is the 1st-coordinate of the point of the boundary of the ellipse
            # definind the direction of the new lobe, in a coordinate system 
            # defined by the semi-axes of the existing lobe
            if ( np.cos(deg2rad*(new_angle-angle[idx])) > 0 ):
                
                xt = np.sqrt( x1[idx]**2 * x2[idx]**2 / ( x2[idx]**2 + x1[idx]**2 * a**2 ) )
                
            else:
                
                xt = - np.sqrt( x1[idx]**2 * x2[idx]**2 / ( x2[idx]**2 + x1[idx]**2 * a**2 ) )

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
            
            # the slope coefficient is evaluated at the point of the boundary of the ellipse
            # definind by the direction of the new lobe
            
            xi = (x[idx]+delta_x - xcmin)/cell
            yi = (y[idx]+delta_y - ycmin)/cell

            ix = np.floor(xi)
            iy = np.floor(yi)

            ix = ix.astype(int)
            iy = iy.astype(int)

            ix1 = ix+1
            iy1 = iy+1

            # stopping condition (lobe close the domain boundary)
            if ( ix <= 0.5 * max_cells ) or ( ix1 >= nx - 0.5*max_cells ) or \
            ( iy <= 0.5 * max_cells ) or ( iy1 >= ny - 0.5*max_cells ):

                #print('ix',ix,'iy',iy)
                last_lobe = i-1
                break

            xi_fract = xi-ix
            yi_fract = yi-iy

            # ztot at the new budding point
            ze = xi_fract * ( yi_fract * Ztot[iy1,ix1] + (1.0-yi_fract) * Ztot[iy,ix1] ) \
                + (1.0-xi_fract) * ( yi_fract * Ztot[iy1,ix] + (1.0-yi_fract) * Ztot[iy,ix] )

            slope = np.maximum( 0.0 , ( zidx - ze ) / ( np.sqrt(np.square(delta_x)+np.square(delta_y) ) ) )

            aspect_ratio = min(max_aspect_ratio,1.0 + aspect_ratio_coeff * slope)

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
            v = ( v1 * ( 1.0 - dist_fact ) + v2 * dist_fact ) / v1  

            # STEP 5: BUILD THE NEW LOBE

            # (x_new,y_new) are the coordinates of the center of the new lobe
            x_new = x[idx] + v * delta_x
            y_new = y[idx] + v * delta_y
                
            plotting_time = time.process_time()                
            # plot the new lobe
            # for i in range(0,n_init):
            if ( plot_lobes_flag == 1 ):
                if plot_parallel == 1:
                    to_ellipse_patch2.append([x_new,y_new,new_x1,new_x2,new_angle, 2])
                else: 
                    patch.append(Ellipse([x_new,y_new], 2*new_x1, 2*new_x2, new_angle, facecolor = 'none',edgecolor='r'))

            # print("line 1207 (PLOTTING) took ", plotting_time)        
            # store the parameters of the new lobe in arrays    
            angle[i] = new_angle
            x1[i] = new_x1
            x2[i] = new_x2
            x[i] = x_new
            y[i] = y_new
            
            if ( saveshape_flag ):

                # compute the lobe
                [ xe , ye ] = ellipse( x_new, y_new, new_x1, new_x2, new_angle , X_circle , Y_circle )

                shape_verts[0:npoints-1,0] = xe[0:npoints-1]
                shape_verts[0:npoints-1,1] = ye[0:npoints-1]

                w.poly(parts=[shape_verts.tolist()])
                w.record(str(i+1),dist_int[i],str(descendents[i]),str(parent[i]),str(flow+1))
    
            # check the grid points covered by the lobe
            if ( saveraster_flag == 1 ) or ( plot_flow_flag):
                
                # compute the new lobe 
                [ xe , ye ] = ellipse( x[i], y[i], x1[i], x2[i], angle[i] , X_circle , Y_circle )
            
                # bounding box for the new lobe
                # the indexes are referred to the centers of the pixels
                min_xe = np.min(xe)
                max_xe = np.max(xe)
                    
                min_ye = np.min(ye)
                max_ye = np.max(ye)

                xi = (min_xe - xcmin)/cell
                ix = np.floor(xi)
                i_left = ix.astype(int)
                i_left = np.maximum( 0 , np.minimum( nx-1 , i_left ) )

                xi = (max_xe - xcmin)/cell
                ix = np.floor(xi)
                i_right = ix.astype(int)+2
                i_right = np.maximum( 0 , np.minimum( nx-1 , i_right ) )

                yj = (min_ye - ycmin)/cell
                jy = np.floor(yj)
                j_bottom = jy.astype(int)            
                j_bottom = np.maximum( 0 , np.minimum( ny-1 , j_bottom ) )

                yj = (max_ye - ycmin)/cell
                jy = np.floor(yj)
                j_top = jy.astype(int)+2            
                j_top = np.maximum( 0 , np.minimum( ny-1 , j_top ) )

                # the centers of the pixels are used to compute the intersection with the lobe
                Xc_local = Xc[j_bottom:j_top,i_left:i_right]
                Yc_local = Yc[j_bottom:j_top,i_left:i_right]
            
                # compute the fraction of cells covered by the lobe (local indexing)
                # for each pixel a square [-0.5*cell;0.5*cell] X [-0.5*cell;0.5*cell]
                # is built around its center to compute the intersection with the lobe
                # the coverage values are associated to each pixel (at the center)
                area_fract = local_intersection(Xc_local,Yc_local,x[i],y[i],x1[i],x2[i],angle[i],xv,yv,nv2)

                Zflow_local = area_fract

                # compute the local integer covering (0-not covered  1-covered) 
                Zflow_local_int = np.ceil(area_fract)
                Zflow_local_int = Zflow_local_int.astype(int)

                #print('Zflow_local_int')
                #print(Zflow_local_int)

                # define the distance (number of lobes) from the vent (local indexing)
                Zdist_local = Zflow_local_int * dist_int[i] + 9999 * ( Zflow_local == 0 )

                # update the minimum distance in the global indexing
                Zdist[j_bottom:j_top,i_left:i_right] = np.minimum( Zdist[j_bottom:j_top,i_left:i_right] , \
                                                                Zdist_local )

                # compute the thickness of the lobe                
                lobe_thickness = thickness_min + ( i-1 ) * delta_lobe_thickness

                # update the thickness for the grid points selected (global indexing)
                Zflow[j_bottom:j_top,i_left:i_right] += lobe_thickness*Zflow_local

                ### change 2022/01/13
                
                Ztot[j_bottom:j_top,i_left:i_right] += filling_parameter * lobe_thickness*Zflow_local
                # TO HERE


                # save the bounding box of the i-th lobe            
                jtop_array[i] = j_top
                jbottom_array[i] = j_bottom
                
                iright_array[i] = i_right
                ileft_array[i] = i_left

                if ( hazard_flag ):

                    # store the local arrays used later for the hazard map

                    if not ( Zflow_local_int.shape[0] == ( j_top-j_bottom ) ):

                        print(Zflow_local_int.shape[0], j_top, j_bottom)
                        print(Zflow_local_int.shape[1], i_right , i_left)
                        print('')

                    if not ( Zflow_local_int.shape[1] == ( i_right - i_left ) ):

                        print(Zflow_local_int.shape[0], j_top, j_bottom)
                        print(Zflow_local_int.shape[1], i_right , i_left)
                        print('')
    
                    if ( np.max(Zflow_local.shape) > Zflow_local_array.shape[1] ):

                        print ('check 3')
                        print (cell,new_x1,new_x2,new_angle)
                        print (x[i],y[i],x1[i],x2[i])
                        np.set_printoptions(precision=1)
                        print (Zflow_local_int)

                    Zflow_local_array[i,0:j_top-j_bottom,0:i_right-i_left] = Zflow_local_int

        ''' for i in range(n_init,n_lobes): END '''
        if ( hazard_flag ):

            # update the hazard map accounting for the number of descendents, representative
            # of the number of times a flow has passed over a cell

            for i in range(0,last_lobe):

                j_top = jtop_array[i]
                j_bottom = jbottom_array[i]

                i_right = iright_array[i]
                i_left = ileft_array[i]

                if ( i > 0):
                    
                    j_top_int = np.minimum( j_top , jtop_array[parent[i]] )
                    j_bottom_int = np.maximum( j_bottom , jbottom_array[parent[i]] )
                    i_left_int = np.maximum( i_left , ileft_array[parent[i]] )
                    i_right_int = np.minimum( i_right , iright_array[parent[i]] )
                        
                    Zlocal_new = np.zeros((max_cells,max_cells),dtype=int)
                    Zlocal_parent = np.zeros((max_cells,max_cells),dtype=int)


                    Zlocal_parent = Zflow_local_array[parent[i],np.maximum(0,j_bottom_int-jbottom_array[parent[i]]): \
                        np.minimum(j_top_int-jbottom_array[parent[i]],jtop_array[parent[i]]-jbottom_array[parent[i]]),   \
                        np.maximum(i_left_int-ileft_array[parent[i]],0):   \
                        np.minimum(i_right_int-ileft_array[parent[i]],iright_array[parent[i]]-ileft_array[parent[i]])]


                    Zlocal_new = Zflow_local_array[i,0:j_top-j_bottom,0:i_right-i_left]

                    if ( Zlocal_parent.shape[0]==0 or Zlocal_parent.shape[1]==0 ):

                        print('check')
                        print('idx',i)  
                        print('j',j_bottom,j_top)
                        print('i',i_left,i_right)
                        print('idx parent',parent[i])  
                        print('j',jbottom_array[parent[i]],jtop_array[parent[i]])
                        print('i',ileft_array[parent[i]],iright_array[parent[i]])
                        print(j_bottom_int,j_top_int,i_left_int,i_right_int)

                    Zlocal_new[np.maximum(0,j_bottom_int-j_bottom):        \
                        np.minimum(j_top_int-j_bottom,j_top-j_bottom),   \
                        np.maximum(i_left_int-i_left,0):                 \
                        np.minimum(i_right_int-i_left,i_right-i_left)] *= ( 1 - Zlocal_parent )


                    Zhazard[j_bottom:j_top,i_left:i_right] += descendents[i] \
                                                            * Zlocal_new[0:j_top-j_bottom,0:i_right-i_left]

                else:

                    Zhazard[j_bottom:j_top,i_left:i_right] += descendents[i] \
                                                            * Zflow_local_array[i,0:j_top-j_bottom,0:i_right-i_left]
            
        # plot the patches for the lobes
        
        if ( plot_lobes_flag == 1 and plot_parallel != 1 ):
            p = PatchCollection(patch, match_original = True)
            ax.add_collection(p)



        if sys.version_info >= (3, 0):
            elapsed = (time.process_time() - start)
        else:
            elapsed = (time.clock() - start)

        estimated = np.ceil( elapsed * n_flows / (flow+1) - elapsed )
        est_rem_time = str(datetime.timedelta(seconds=estimated))
        

    if ( n_flows > 1 and not 'SLURM_JOB_NAME' in os.environ.keys()):
        # print on screen bar with percentage of flows computed
        last_percentage = 100
        sys.stdout.write('\r')
        sys.stdout.write("[%-20s] %d%%" % ('='*20, last_percentage))
        sys.stdout.flush()


    
    if plot_parallel == 1 and plot_lobes_flag:
        ''' PLOTTING OUTSIDE OF LOOPS '''
        print("I am plotting in parallel")
        for i in range(0, len(to_plot_centers)):
            plt.plot(to_plot_centers[i][0],to_plot_centers[i][1],'o')

        ellip_k = run_processes(to_ellipse_patch)
        ellip_r = run_processes(to_ellipse_patch2)

        for el in ellip_k: 
            ax.add_patch(el)
        for el in ellip_r:
            ax.add_patch(el)

        ''' PLOTTING OUTSIDE OF LOOPS END '''


    if sys.version_info >= (3, 0):
        elapsed = (time.process_time() - start)
    else:
        elapsed = (time.clock() - start)

    

    print ('')
    print ('')
    print ('Total number of lobes',n_lobes_tot,'Average number of lobes',int(1.0*n_lobes_tot/n_flows))
    print ('')
    print ('Time elapsed ' + str(elapsed) + ' sec.' + ' / ' + str(int(elapsed/60)) + ' min.')
    print ('')
    print ('Saving files')
    
    # print ('Max thickness',np.max(Ztot-Zc),' m')

    if ( saveshape_flag ):

        # Save the shapefile
        output_shape = run_name + '_out'
        w.save(output_shape)

    if ( saveraster_flag == 1 ):
        # Save raster files

        header = "ncols     %s\n" % Zflow.shape[1]
        header += "nrows    %s\n" % Zflow.shape[0]
        header += "xllcorner " + str(lx) +"\n"
        header += "yllcorner " + str(ly) +"\n"
        header += "cellsize " + str(cell) +"\n"
        header += "NODATA_value 0\n"

        output_full = run_name + '_thickness_full.asc'

        np.savetxt(output_full, np.flipud(Zflow), header=header, fmt='%1.5f',comments='')


        print ('')
        print (output_full + ' saved')

        if isinstance(masking_threshold,float):
        
            masking_threshold = [masking_threshold]

        n_masking = len(masking_threshold)

        for i_thr in range(n_masking):

            if ( masking_threshold[i_thr] < 1):

                max_lobes = int(np.floor(np.max(Zflow/avg_lobe_thickness)))

                for i in range(1,10*max_lobes):

                    masked_Zflow = ma.masked_where(Zflow < i*0.1*avg_lobe_thickness, Zflow)

                    total_Zflow = np.sum(Zflow)

                    if ( flag_threshold == 1 ):

                        volume_fraction = np.sum( masked_Zflow ) / total_Zflow

                        coverage_fraction = volume_fraction

                    else:

                        area_fraction = np.true_divide( np.sum( masked_Zflow > 0 ) , \
                                                            np.sum( Zflow >0 ) )

                        coverage_fraction = area_fraction
                        #print (coverage_fraction)
                    

                    if ( coverage_fraction < masking_threshold[i_thr] ): 

                        if ( flag_threshold == 1 ):
                    
                            print('')
                            print ('Masking threshold',masking_threshold[i_thr])
                            print ('Total volume',cell**2*total_Zflow, \
                                ' m3 Masked volume',cell**2*np.sum( masked_Zflow ), \
                                ' m3 Volume fraction',coverage_fraction)
                            print ('Total area',cell**2*np.sum( Zflow >0 ), \
                                ' m2 Masked area',cell**2*np.sum( masked_Zflow >0 ),' m2')
                            print ('Average thickness full',total_Zflow/np.sum( Zflow >0 ), \
                                ' m Average thickness mask',np.sum( masked_Zflow )/ np.sum( masked_Zflow >0 ),' m')

                        output_thickness = run_name + '_avg_thick.txt'
                        with open(output_thickness, 'a') as the_file:
                        
                            if (i_thr == 0):
                                the_file.write('Average lobe thickness = '+str(avg_lobe_thickness)+' m\n')
                                the_file.write('Total volume = '+str(cell**2*total_Zflow)+' m3\n')
                                the_file.write('Total area = '+str(cell**2*np.sum( Zflow >0 ))+' m2\n')
                                the_file.write('Average thickness full = '+str(total_Zflow/np.sum( Zflow >0 ))+' m\n')

                            the_file.write('Masking threshold = '+str(masking_threshold[i_thr])+'\n')
                            the_file.write('Masked volume = '+str(cell**2*np.sum( masked_Zflow ))+' m3\n')
                            the_file.write('Masked area = '+str(cell**2*np.sum( masked_Zflow >0 ))+' m2\n')
                            the_file.write('Average thickness mask = '+str(np.sum( masked_Zflow )/ np.sum( masked_Zflow >0 ))+' m\n')

                        

                        output_masked = run_name + '_thickness_masked' + '_' + str(masking_threshold[i_thr]).replace('.','_') + '.asc'

                        np.savetxt(output_masked, np.flipud((1-masked_Zflow.mask)*Zflow), \
                                header=header, fmt='%1.5f',comments='')

                        print ('')
                        print (output_masked + ' saved')

                        break

        output_dist = run_name + '_dist_full.asc'
        
        # ST skipped this (and conjugated masked) to save up disk space (poorly used so far):
        """
        # np.savetxt(output_dist, np.flipud(Zdist), header=header, fmt='%4i',comments='')

        # print ('')
        # print (output_dist + ' saved')

        output_dist = run_name + '_dist_masked.asc'

        if ( masking_threshold < 1):

            Zdist = (1-masked_Zflow.mask) * Zdist + masked_Zflow.mask * 0

            # np.savetxt(output_dist, np.flipud(Zdist), header=header, fmt='%4i',comments='')

            # print ('')
            # print (output_dist + ' saved')
        
        """
        
        if ( hazard_flag ):

            output_haz = run_name + '_hazard_full.asc'
            
            np.savetxt(output_haz, np.flipud(Zhazard), header=header, fmt='%1.5f',comments='')

            print ('')
            print (output_haz + ' saved')

            for i_thr in range(n_masking):

                if ( masking_threshold[i_thr] < 1):

                    max_Zhazard = int(np.floor(np.max(Zhazard)))

                    total_Zflow = np.sum(Zflow)

                    # for i in range(1,max_Zhazard):
                    for i in np.unique(Zhazard):

                        masked_Zflow = ma.masked_where(Zhazard < i, Zflow)

                        if ( flag_threshold == 1 ):

                            volume_fraction = np.sum( masked_Zflow ) / total_Zflow

                            coverage_fraction = volume_fraction

                        else:

                            area_fraction = np.true_divide( np.sum( masked_Zflow > 0 ) , \
                                                            np.sum( Zflow >0 ) )

                            coverage_fraction = area_fraction

                        if ( coverage_fraction < masking_threshold ): 

                            break

                    output_haz_masked = run_name + '_hazard_masked' + '_' + str(masking_threshold[i_thr]).replace('.','_') + '.asc'

                    np.savetxt(output_haz_masked, np.flipud((1-masked_Zflow.mask)*Zhazard), \
                            header=header, fmt='%1.5f',comments='')

                    print ('')
                    print (output_haz_masked + ' saved')


        # this is to save an additional output for the cumulative deposit, if restart_files is not empty
        # load restart files (if existing) 
        if (len(restart_files) > 0):
            for i_restart in range(0,len(restart_files)): 

                Zflow_old = np.zeros((ny,nx))

                source = restart_files[i_restart]

                file_exists = exists(source)
                if not file_exists:
                    print(source + ' not found.')
                    quit()
        
                hdr = [getline(source, i) for i in range(1,7)]
                try:
                    values = [float(h.split(" ")[-1].strip()) for h in hdr]
                except:
                    print("An problem occurred with header of file ",source)
                    print(hdr)
                
                cols,rows,lx,ly,cell,nd = values    

                # Load the previous flow thickness into a numpy array
                arr = np.loadtxt(source, skiprows=6)
                arr[arr==nd] = 0.0

                Zflow_old = np.flipud(arr)

                Zflow = Zflow + Zflow_old

            output_full = run_name + '_thickness_cumulative.asc'

            np.savetxt(output_full, np.flipud(Zflow), header=header, fmt='%1.5f',comments='')

            output_thickness_cumulative = run_name + '_thickness_cumulative.asc'

            print ('')
            print (output_thickness_cumulative + ' saved')


        
        if ( plot_flow_flag ):

            print ("")
            print ("Plot solution")

            plt.pcolormesh(Xc, Yc, masked_Zflow)


    


    



    if ( plot_flow_flag ) or ( plot_lobes_flag):
        
        plt.axis('equal')
        plt.ylim([ycmin,ycmax])
        plt.xlim([xcmin,xcmax])
        plt.savefig("plotted.png")
        # plt.show()




