import numpy as np 
import pickle


def nearest_element_idx(arr, a, both=True):
	if both:
		dist = np.abs(arr-a)
		dist_arg = np.argsort(dist)
		return  dist_arg[0], dist_arg[1]
	else:
		return np.abs(arr-a).argmin()


