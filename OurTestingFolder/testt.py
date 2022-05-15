
from __future__ import division

import numpy as np
import math

from numba import cuda
@cuda.jit
def last_lobe_loop(last_lobe,jtop_array, jbottom_array,iright_array,ileft_array, max_cells, parent, Zhazard, Zflow_local_array,descendents ):
    i = cuda.grid(1)
    if(i < last_lobe):
        j_top = jtop_array[i]
        j_bottom = jbottom_array[i]

        i_right = iright_array[i]
        i_left = ileft_array[i]

        if (i > 0):

            j_top_int = np.minimum(j_top, jtop_array[parent[i]])
            j_bottom_int = np.maximum(j_bottom, jbottom_array[parent[i]])
            i_left_int = np.maximum(i_left, ileft_array[parent[i]])
            i_right_int = np.minimum(i_right, iright_array[parent[i]])

            Zlocal_new = np.zeros((max_cells, max_cells), dtype=np.int)
            Zlocal_parent = np.zeros((max_cells, max_cells), dtype=np.int)

            Zlocal_parent = Zflow_local_array[parent[i], np.maximum(0, j_bottom_int-jbottom_array[parent[i]]):
                                                np.minimum(
                                                    j_top_int-jbottom_array[parent[i]], jtop_array[parent[i]]-jbottom_array[parent[i]]),
                                                np.maximum(i_left_int-ileft_array[parent[i]], 0):
                                                np.minimum(i_right_int-ileft_array[parent[i]], iright_array[parent[i]]-ileft_array[parent[i]])]

            Zlocal_new = Zflow_local_array[i,
                                            0:j_top-j_bottom, 0:i_right-i_left]

            if (Zlocal_parent.shape[0] == 0 or Zlocal_parent.shape[1] == 0):

                print('check')
                print('idx', i)
                print('j', j_bottom, j_top)
                print('i', i_left, i_right)
                print('idx parent', parent[i])
                print('j', jbottom_array[parent[i]], jtop_array[parent[i]])
                print('i', ileft_array[parent[i]], iright_array[parent[i]])
                print(j_bottom_int, j_top_int, i_left_int, i_right_int)

            Zlocal_new[np.maximum(0, j_bottom_int-j_bottom):
                        np.minimum(j_top_int-j_bottom, j_top-j_bottom),
                        np.maximum(i_left_int-i_left, 0):
                        np.minimum(i_right_int-i_left, i_right-i_left)] *= (1 - Zlocal_parent)

            Zhazard[j_bottom:j_top, i_left:i_right] += descendents[i] \
                * Zlocal_new[0:j_top-j_bottom, 0:i_right-i_left]

        else:

            Zhazard[j_bottom:j_top, i_left:i_right] += descendents[i] \
                * Zflow_local_array[i, 0:j_top-j_bottom, 0:i_right-i_left]

max_cells = 5 
last_lobe = 10

descendents = np.zeros(5, dtype=np.int)
parent = np.zeros(5, dtype=np.int)
jtop_array = np.zeros(5, dtype=np.int)
jbottom_array = np.zeros(5, dtype=np.int)

iright_array = np.zeros(5, dtype=np.int)
ileft_array = np.zeros(5, dtype=np.int)
Zhazard = np.zeros((5, 5))
Zhazard_temp = np.zeros((5, 5))

Zflow_local_array = np.zeros((5, max_cells, max_cells), dtype=np.int)


for i in range(0, last_lobe):

    j_top = jtop_array[i]
    j_bottom = jbottom_array[i]

    i_right = iright_array[i]
    i_left = ileft_array[i]

    if (i > 0):

        j_top_int = np.minimum(j_top, jtop_array[parent[i]])
        j_bottom_int = np.maximum(j_bottom, jbottom_array[parent[i]])
        i_left_int = np.maximum(i_left, ileft_array[parent[i]])
        i_right_int = np.minimum(i_right, iright_array[parent[i]])

        Zlocal_new = np.zeros((max_cells, max_cells), dtype=np.int)
        Zlocal_parent = np.zeros((max_cells, max_cells), dtype=np.int)

        Zlocal_parent = Zflow_local_array[parent[i], np.maximum(0, j_bottom_int-jbottom_array[parent[i]]):
                                            np.minimum(
                                                j_top_int-jbottom_array[parent[i]], jtop_array[parent[i]]-jbottom_array[parent[i]]),
                                            np.maximum(i_left_int-ileft_array[parent[i]], 0):
                                            np.minimum(i_right_int-ileft_array[parent[i]], iright_array[parent[i]]-ileft_array[parent[i]])]

        Zlocal_new = Zflow_local_array[i,
                                        0:j_top-j_bottom, 0:i_right-i_left]

        if (Zlocal_parent.shape[0] == 0 or Zlocal_parent.shape[1] == 0):

            print('check')
            print('idx', i)
            print('j', j_bottom, j_top)
            print('i', i_left, i_right)
            print('idx parent', parent[i])
            print('j', jbottom_array[parent[i]], jtop_array[parent[i]])
            print('i', ileft_array[parent[i]], iright_array[parent[i]])
            print(j_bottom_int, j_top_int, i_left_int, i_right_int)

        Zlocal_new[np.maximum(0, j_bottom_int-j_bottom):
                    np.minimum(j_top_int-j_bottom, j_top-j_bottom),
                    np.maximum(i_left_int-i_left, 0):
                    np.minimum(i_right_int-i_left, i_right-i_left)] *= (1 - Zlocal_parent)

        Zhazard[j_bottom:j_top, i_left:i_right] += descendents[i] \
            * Zlocal_new[0:j_top-j_bottom, 0:i_right-i_left]

    else:

        Zhazard[j_bottom:j_top, i_left:i_right] += descendents[i] \
            * Zflow_local_array[i, 0:j_top-j_bottom, 0:i_right-i_left]