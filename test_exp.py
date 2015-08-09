#!/usr/bin/env python
import numpy as np
from scipy import stats

### data, 1-d array
def isExpDistribution(samples, min_r_squared = 0.95):
	# convert to np array
	samples = np.array(samples)
	n = samples.shape[0]

	# sort the samples
	samples = np.sort(samples)
	# estimate lambda
	l = 1 / np.mean(samples)

	# generate quartiles
	p = np.array([ (i + 0.5)  / n for i in range(n)])
	q = - np.log( 1 - p) / l
	
	# linear regression
	slope, intercept, r_value, p_value, std_err = stats.linregress(samples, q)
	r_squared = r_value**2

	return r_squared > min_r_squared

if __name__ == '__main__':
	samples = [1.09,1.19,1.3,1.44,1.54,1.72,1.83,2.14,2.33,2.51,2.88,3.01,3.62,3.84,4.19,4.87,5.01,5.67,6.13,7.06,7.53,8.6,9.2,10.79,11.21,12.3,13.47,15.24,16.77,18.81,20.86,24.37,25.91,29]
	print isExpDistribution(samples, 0.97)