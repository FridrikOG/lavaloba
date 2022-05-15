# Introduction

This is a project for the course High Performance Computing (T-739 PHPC) taught by Jacqueline Mallet at the University of Reykjavik Spring 2022.

In this project we took a 4 year old project (https://github.com/demichie/MrLavaLoba/) and attempted to optimize the code using the packages Numba and concurrent.futures.

Important files include:
* MrOptimisticLoba/mr_lava_loba.py : the optimized version which includes numba and the parallelization of the creation of Ellipses using concurrent.futures
* MrOptimisticLoba/original_mr_lava_loba.py : the original mr_lava_loba.py
* testing.ipynb : contains a working cuda.jit version of the ellipse() function, not to be confused with the package Ellipse from **matplotlib.patches**
* MrOptimisticLoba\input_data_advanced.py  and input_data.py contain the settings for the program

The folder MrLavaLoba-original includes the original code from the github mentioned above. OurTestingFolder contains a lot of tests done...

**REQUIREMENTS** 
* have python3, 
* pip (or conda installed)

if you want to run the cuda version of the ellipse function, you'll need a cuda compatible GPU.

# How to run

First start up an environment and install the requirements.txt (in the root)
## Mac instructions:
```
pip install virtualenv 
```
(if you do not have it)
```
source venv/bin/activate
```
```
source venv/bin/activate
```

## Windows instructions:
```
pip install virtualenv
```
```
virtualenv venv
```
(run this next one within the main folder which contains the mr_lava_loba.py you wanna run)
```
.\venv\Scripts\activate
```
if you get a similar error to "[...] venv\Scripts\activate.ps1 cannot be loaded because running scripts is disabled on this system. For more information, see  about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170." 
then run: 
Set-ExecutionPolicy Unrestricted -Scope Process
and then run the previous command again!
```   
pip install -r requirements.txt
```
```
python3 OR python mr_lava_loba.py
```

----
To exit the environment simply run in the terminal: 
```
deactivate
```

# !!! IMPORTANT !!!
BEFORE running the actual program, you'll need to download two large files and put them in the MrOptimisticLoba, download them [here](https://www.dropbox.com/sh/horpkk5z0m7w72b/AABB1Wmq6g0qTzPD4J_i1iOEa?dl=0).

All the files needed to run the program include:

&#x2611; fig_map.png

&#x2611; input_data_advanced.py

&#x2611; input_data.py

&#x2611; make_plot.py

&#x2611; reysvakry10m_msl.npy

&#x2611; reysvakry10m_msl.asc

&#x2611; rtnorm.py

&#x2611; shapefile.py

&#x2611; variables_xVent_yVent_length_flowrate_runtime_minnlobes_test.csv

&#x2611; variables_xVent_yVent_length_flowrate_runtime_minnlobes.csv

----
Once the environment is set up and you have all the files required, please procceed to the folder 

```
 cd MrOptimisticLoba
```

From that folder you can run the newly optimized version program by:
```
python mr_lava_loba.py
```
or
```
python3 mr_lava_loba.py
```
depending on what you have.

### Without parallelization

If you want to run the plotting without the parallelization done, then go to input_data_advanced.py (within MrOptimisticLoba) and change *plot_parallel = 1* to *plot_parallel = 0*.


### Original MrLavaLoba
If you'd like to run the original version of the program
```
python original_mr_lava_loba.py
```

### Snakeviz and cProfile
If you'd like to use the snakeviz display simply change the settings you'd like to run, then run:
```
python -m cProfile -o profile1.prof mr_lava_loba.py
```
and once it's done running you can simply run 
```
snakeviz profile1.prof
```
This will open your browser window with 

![Snakeviz Example image](snakevizExample.png)

