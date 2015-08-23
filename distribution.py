#!/usr/bin/env python
import math
import numpy as np
from scipy import stats

def preprosses(samples):
	samples = np.array(samples)	
	samples = np.sort(samples)
	n = samples.shape[0]
	mean = np.mean(samples)
	stddev = np.std(samples)
	p = np.array([(i + 0.5)  / n for i in xrange(n)])
	return samples, n, mean, stddev, p

# fit samples with q, return R^2
def compute_r_squared(samples, q):
	# linear regression
	slope, intercept, r_value, p_value, std_err = stats.linregress(samples, q)
	r_squared = r_value**2

	return r_squared

def isExp(samples, min_r_squared = 0.95):
	samples, n, mean, stddev, p = preprosses(samples)
	# estimate lambda
	l = 1 / mean
	# generate quartiles
	q = - np.log( 1 - p) / l
	return compute_r_squared(samples, q) > min_r_squared


def isUniform(samples, min_r_squared = 0.95):
	samples, n, mean, stddev, p = preprosses(samples)
	q = stddev * math.sqrt(3) * (2*p - 1) + mean
	return compute_r_squared(samples, q) > min_r_squared	

def isNormal(samples, min_r_squared = 0.95):
	samples, n, mean, stddev, p = preprosses(samples)
	q = np.array([stats.norm.ppf(pp, loc = mean, scale = stddev) for pp in p])
	return compute_r_squared(samples, q) > min_r_squared

def isPoisson(samples, min_r_squared = 0.95):
	samples, n, mean, stddev, p = preprosses(samples)
	q = np.array([stats.poisson.ppf(pp, mu = mean) for pp in p])
	return compute_r_squared(samples, q) > min_r_squared


def isDistribution(samples, distribution, min_r_squared = 0.95):	
	if distribution not in m.keys():
		print 'Error, unknonwn distribution type:', distribution
		return None

	return m[distribution](samples, min_r_squared)

def whichDistribution(samples, min_r_squared = 0.95):
	d = []
	for name in m:
		if isDistribution(samples, name, min_r_squared): d.append(name)
	return d

m = {
	'exp': isExp,
	'norm': isNormal,
	'poission': isPoisson,
	'uniform': isUniform
}

if __name__ == '__main__':
	samples = [1.09,1.19,1.3,1.44,1.54,1.72,1.83,2.14,2.33,2.51,2.88,3.01,3.62,3.84,4.19,4.87,5.01,5.67,6.13,7.06,7.53,8.6,9.2,10.79,11.21,12.3,13.47,15.24,16.77,18.81,20.86,24.37,25.91,29]
	print isExp(samples, 0.99)
	print isDistribution(samples, 'exp')
	print whichDistribution(samples)
	print '--------------------------------'

	samples = [2.18,2.28,2.32,2.52,2.61,2.65,3,3.09,3.33,3.45,3.58,3.63,3.67,3.79,4.15]
	print isNormal(samples, 0.95)
	print whichDistribution(samples)
	print '--------------------------------'

	samples = [0,0,0,0,1,1,1,1,1,1,1,2,2,2,2,3,3,4]
	print whichDistribution(samples)
	print '--------------------------------'

	samples = [1,1,1,2,2,2,3,3,3,4,4,4,5,5,5,6,6,6]
	print whichDistribution(samples)
	print '--------------------------------'
