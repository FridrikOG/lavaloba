import os
# name of the run (used to save the parameters and the output)
# by default, output with be saved in the same directory the code is in,
# unless the environmental variable "DESTINATION" is set, in which case
# that will be used.

run_name = 'fagralike'
#these are the variables that will be read on from a .csv file when i launch the runs
xVent    = 0.0
yVent    = 0.0
length = 0.0 # km
flowrate = 0.0 # m3/s
runtime = 0.0 # min
minnlobes = 0.0

# File name of ASCII digital elevation model
# CHANGE THESE AS NEEDED OR ADD TO .CSV FILE
source = "reysvakry10m_msl.asc"
DEMres = 10.0 #m
 
# For running in batch mode, attempt to read x_vent and y_vent from the
# environmental variables, xVent and yVent

try:

  xVent = float(os.environ['xVent'])
  yVent = float(os.environ['yVent'])
  length = float(os.environ['length'])
  flowrate = float(os.environ['flowrate'])
  runtime = float(os.environ['runtime'])
  minnlobes = float(os.environ['minnlobes'])
except: 
  # from variables_xVent_yVent_length_flowrate_runtime_minnlobes_test 339377,380305,0.04,5,660,0.7
  xVent = 339377
  yVent = 380305
  length = 0.04
  flowrate = 5
  runtime = 660
  minnlobes = 0.7
  print("Using default values for xVent,yVent,length,flowrate,runtime,minnlobes")

# Set destination directory if provided. The directory itself needs to be
# created by calling script somehow, and then passed over as the environmental 
# variable "DESTINATION"

try: 
  dest  = os.environ['DESTINATION']
  run_name = dest + "/" + run_name
except:
  pass

print("Output will be written to files with prefix: ", run_name + "*")

#print(os.environ)

#this determines how large an area will be clipped from the DEM. smaller = faster, but need to ensure nothing runs out of the domain
east_to_vent = 1500.0
west_to_vent = 1500.0
south_to_vent = 1500.0
north_to_vent = 1500.0

# This flag select how multiple initial coordinates are treated:
# vent_flag = 0  => the initial lobes are on the vents coordinates
#                   and the flows start initially from the first vent,
#                   then from the second and so on.
# vent_flag = 1  => the initial lobes are chosen randomly from the vents
#                   coordinates and each vent has the same probability
# vent_flag = 2  => the initial lobes are on the polyline connecting
#                   the vents and all the point of the polyline
#                   have the same probability
# vent_flag = 3  => the initial lobes are on the polyline connecting
#                   the vents and all the segments of the polyline
#                   have the same probability
# vent_flag = 4  => the initial lobes are on multiple
#                   fissures and all the point of the fissures
#                   have the same probability
# vent_flag = 5  => the initial lobes are on multiple
#                   fissures and all the fissures
#                   have the same probability
# vent_flag = 6  => the initial lobes are on the polyline connecting
#                   the vents and the probability of
#                   each segment is fixed by "fissure probabilities"
# vent_flag = 7  => the initial lobes are on multiple
#                   fissures and the probability of
#                   each fissure is fixed by "fissure_probabilities"

vent_flag = 2 
#any fissure length as a function of relation of length/10km

x_vent = [ xVent-3.473284*1000*length/10 , xVent+3.473284*1000*length/10 ]
y_vent = [ yVent-3.596706*1000*length/10 , yVent+3.596706*1000*length/10 ]

#10 km
#x_vent = [ xVent-3.473284*1000 , xVent+3.473284*1000 ]
#y_vent = [ yVent-3.596706*1000 , yVent+3.596706*1000 ]

#single vent
#x_vent = [ xVent ]
#y_vent = [ yVent ]


# If this flag is set to 1 then a raster map is saved where the values
# represent the probability of a cell to be covered.
hazard_flag = 1

# Fraction of the volume emplaced or the area invaded (according to the flag
# flag_threshold) used to save the run_name_*_masked.asc files.
# In this way we cut the "tails" with a low thickness (*_thickness_masked.asc)
# and a low probability (*_hazard_masked.asc). The file is used also
# to check the convergence of the solutions increasing the number of flows.
# The full outputs are saved in the files run_name_*_full.asc
# The masked files are saved only when masking_thresold < 1.
masking_threshold = 0.96

# Number of flows
#n_flows = 1600
#small
n_flows = [round((flowrate*runtime)/100) ]
#print("length: ",length)
#print("flowrate: ",flowrate)
#print("value: ",(flowrate/2 * length))
#print("value: ",round(flowrate/2 * length))
print("nflows: ",n_flows)
n_flows = n_flows[0]
print("nflows: ",n_flows)
#print("type: ",type(n_flows))
#n_flows = 200
# Minimum number of lobes generated for each flow
# default is 2 
#min_n_lobes =     2500
#medium
#min_n_lobes = 1500
#small
min_n_lobes = [round(((0.00665 * flowrate) + minnlobes) * runtime) ]
min_n_lobes = min_n_lobes[0]
#print("type: ",type(min_n_lobes))

#min_n_lobes = 400
# Maximum number of lobes generated for each flow
# default is 650
max_n_lobes = min_n_lobes

# If volume flag = 1 then the total volume is read in input, and the
# thickness or the area of the lobes are evaluated according to the
# flag fixed_dimension_flag and the relationship V = n*area*T.
# Otherwise the thickness and the area are read in input and the total
# volume is evaluated (V = n*area*T).
volume_flag = 1

# Total volume (this value is used only when volume_flag = 1) set "1" to be confirmed.
#Arnarseturshraun: 150000000. Eldvarpahraun: 120000000. Illahraun: 20000000.
total_volume = [ flowrate * runtime * 60 ]
total_volume = total_volume[0]
#total_volume = 150000000 # m^3 0.15 km3 = 1.5e8 m3
#total_volume = 20000000   # m^3 0.02 km3 = 2e7 m3 = Small scenario
#total_volume = 300000000  # m^3 0.3 km3 = 3e8 m3 = Medium scenario
# This flag select which dimension of the lobe is fixed when volume_flag=1:
# fixed_dimension_flag = 1  => the area of the lobes is assigned
# fixed_dimension_flag = 2  => the thickness of the lobes is assigend
fixed_dimension_flag = 1 

# Area of each lobe ( only effective when volume_flag = 0 or fixed_dimension_flag = 1 )
# default lobe_area = 1000   # m^2
#lobe_area = 1000 # m^2 MAP- if 5 m Grid = 25; if 20 m grid = 4000 . resolution of the DEMi # medium
lobe_area = [ DEMres * DEMres ]
lobe_area = lobe_area[0]
# Thickness of each lobe ( only effective when volume_flag = 0 or fixed_dimension_flag  2 )
# defualt avg_lobe_thickness = 0.02   # m
# MAP note: I need to get this smaller!
avg_lobe_thickness = 0.035
#avg_lobe_thickness = 0.015
# Ratio between the thickness of the first lobe of the flow and the thickness of the
# last lobe.
# thickness_ratio < 1   => the thickness increases with lobe "age"
# thickness_ratio = 1   => all the lobes have the same thickness
# thickness_ratio > 1   => the thickness decreases with lobe "age"
# default thickness_ratio = 1
thickness_ratio = 2

# This flag controls if the topography is modified by the lobes and if the
# emplacement of new flows is affected by the changed slope
# topo_mod_flag = 0   => the slope does not changes
# topo_mod_flag = 1   => the slope is re-evaluated every n_flows_counter flows
# topo_mod_flag = 2   => the slope is re-evaluated every n_lobes_counter flows
#                        and every n_flows_counter flows
topo_mod_flag = 2
# This parameter is only effective when topo_mod_flag = 1 and defines the
# number of flows for the re-evaluation of the slope modified by the flow
n_flows_counter = 1

# This parameter is only effective when topo_mod_flag = 2 and defines the
# number of lobes for the re-evaluation of the slope modified by the flow
n_lobes_counter = 1

# This parameter (between 0 and 1) allows for a thickening of the flow giving
# controlling the modification of the slope due to the presence of the flow.
# thickening_parameter = 0  => minimum thickening (maximum spreading)
# thickening_parameter = 1  => maximum thickening produced in the output
# default thickening_parameter = 0.2
# if you reduce this, the impact of the lava flow is lessened in the computation of the slope,
# but the thickness is still correct. this allows for "channel" flow, if = 1,
# then sublava flow would not happen.
thickening_parameter = 0.06

# Lobe_exponent is associated to the probability that a new lobe will
# be generated by a young or old (far or close to the vent when the
# flag start_from_dist_flag=1) lobe. The closer is lobe_exponent to 0 the
# larger is the probability that the new lobe will be generated from a
# younger lobe.
# lobe_exponent = 1  => there is a uniform probability distribution
#                       assigned to all the existing lobes for the choice
#                       of the next lobe from which a new lobe will be
#                       generated.
    # lobe_exponent = 0  => the new lobe is generated from the last one.
# default lobe_exponent = 0.015
# MAP note: this is very sensitive! as it goes up, the lava spreads out less and gets much thicker.
#lobe_exponent = 0.02
#lobe_exponent = 0.05
#lobe_exponent = 0.015 #medium
lobe_exponent = 0.03 #small

# max_slope_prob is related to the probability that the direction of
# the new lobe is close to the maximum slope direction:
# max_slope_prob = 0 => all the directions have the same probability;
# max_slope_prob > 0 => the maximum slope direction has a larger
#                       probability, and it increases with increasing
#                       value of the parameter;
# max_slope_prob = 1 => the direction of the new lobe is the maximum
#                       slope direction.
# default max_slope_prob = 0.8
# MAP note: this used to be called max_angle_prob
# MAP note: this is very sensitive
# if this is too low, then the randomness is driving the direction, and the
# topography is not having a proper impact. keep greater than 0.5
max_slope_prob = 0.8

# Inertial exponent:
# inertial_exponent = 0 => the max probability direction for the new lobe is the
#                          max slope direction;
# inertial_exponent > 0 => the max probability direction for the new lobe takes
#                          into account also the direction of the parent lobe and
#                          the inertia increaes with increasing exponent
# default inertial_exponent = 0.125
inertial_exponent = 0.1

