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

def isLogNormal(samples, min_r_squared = 0.95):
	samples, n, mean, stddev, p = preprosses(samples)
	if np.sum(samples > 0) == len(samples):
		return isNormal(np.log(samples), min_r_squared)
	else:
		return False

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
	if len(d) == 0: d = ['None']
	return d

m = {
	'exp': isExp,
	'norm': isNormal,
	'possion': isPoisson,
	'uniform': isUniform,
	'lognorm': isLogNormal
}

if __name__ == '__main__':
	samples = stats.expon.rvs(loc = 3, scale = 5, size = 500)
	print 'expected = [\'exp\'], actual =', whichDistribution(samples, 0.98)	

	# normal
	samples = stats.norm.rvs(loc = 2, scale = 3, size = 500)	
	print 'expected = [\'norm\'], actual =', whichDistribution(samples, 0.98)	

	# poisson
	samples = stats.poisson.rvs(mu = 2, size = 500)
	print 'expected = [\'possion\'], actual =', whichDistribution(samples, 0.98)

	# uniform
	samples = stats.uniform.rvs(loc = 0, scale = 1, size = 500)
	print 'expected = [\'uniform\'], actual =', whichDistribution(samples, 0.98)	

	# lognormal
	samples = stats.lognorm.rvs(s = 1.0, size = 500)
	print 'expected = [\'lognorm\'], actual =', whichDistribution(samples, 0.98)	
