#!/usr/bin/env python
import math
import numpy as np
from scipy import stats


def preprosses(samples):
  n = samples.shape[0]
  mean = np.mean(samples)
  stddev = np.std(samples)
  p = np.array([(i + 0.5) / n for i in xrange(n)])
  return samples, n, mean, stddev, p

# fit samples with q, return R^2


def compute_r_squared(samples, q):
  # linear regression
  slope, intercept, r_value, p_value, std_err = stats.linregress(samples, q)
  r_squared = r_value ** 2

  return r_squared


def isExp(samples):
  samples, n, mean, stddev, p = preprosses(samples)
  # estimate lambda
  l = 1 / mean
  # generate quartiles
  q = - np.log(1 - p) / l
  return q, {'lambda': l}


def isUniform(samples):
  samples, n, mean, stddev, p = preprosses(samples)
  q = stddev * math.sqrt(3) * (2 * p - 1) + mean
  return q, {
      'a': np.min(samples), 'b': np.max(samples)}


# def isNormal(samples, min_r_squared=0.95):
#   samples, n, mean, stddev, p = preprosses(samples)
#   miu, sigma = stats.norm.fit(samples)
#   q = np.array([stats.norm.ppf(pp, loc=miu, scale=sigma) for pp in p])
#   return compute_r_squared(
#       samples, q) > min_r_squared, {'miu': miu, 'sigma': sigma}


# def isLogNormal(samples, min_r_squared=0.95):
#   samples, n, mean, stddev, p = preprosses(samples)
#   if np.sum(samples > 0) == len(samples):
#     r, p = isNormal(np.log(samples), min_r_squared)
#     s, miu, sigma = stats.lognorm.fit(samples)
#     return r, {'s': s, 'miu': miu, 'sigma': sigma}
#   else:
#     return False, {}

def isNormal(samples):
  samples, n, mean, stddev, p = preprosses(samples)
  miu, sigma = stats.norm.fit(samples)
  q = np.array([stats.norm.ppf(pp, loc=miu, scale=sigma) for pp in p])
  return q, {'miu': miu, 'sigma': sigma}


def isLogNormal(samples):
  if np.sum(np.array(samples) > 0) == len(samples):
    samples, n, mean, stddev, p = preprosses(samples)
    q, parameters = isNormal(np.log(samples))
    parameters = {
        'shape': parameters['sigma'],
        'scale': np.exp(
            parameters['miu']),
        'loc': 0}
    q = np.array(
        [stats.lognorm.ppf(pp, parameters['shape'], loc=0, scale=parameters['scale']) for pp in p])
    return q, parameters
  return np.array([]), {}


def isPoisson(samples):
  samples, n, mean, stddev, p = preprosses(samples)
  q = np.array([stats.poisson.ppf(pp, mu=mean) for pp in p])
  return q, {'mu': mean}


def isDistribution(samples, distribution, min_r_squared=0.95):
  if distribution not in m.keys():
    print 'Error, unknonwn distribution type:', distribution
    return None

  samples = np.array(samples)
  samples = np.sort(samples)
  q, p = m[distribution](samples)
  if samples.shape != q.shape:
    R = 0
  else:
    R = compute_r_squared(samples, q)
  result = True
  if R < min_r_squared:
    result = False
  return result, p, R


# best == True: return all matched distributions
# best == False: return the best matched distributions


def whichDistribution(samples, min_r_squared=0.95, best=False):
  d = {}
  best_R = min_r_squared
  for name in m:
    result, parameters, R = isDistribution(samples, name, min_r_squared)
    parameters['R^2'] = R
    if result:
      if best:
        if R < best_R:
          continue
        best_R = R
        d = {name: parameters}
      else:
        d[name] = parameters
  if len(d) == 0:
    d = {'None': {}}
  return d

m = {
    'exp': isExp,
    'norm': isNormal,
    'possion': isPoisson,
    'uniform': isUniform,
    'lognorm': isLogNormal
}

if __name__ == '__main__':
  samples = stats.expon.rvs(loc=1, scale=1, size=500)
  print 'expected = [\'exp\'], actual =', whichDistribution(samples, 0.98)

  # normal
  samples = stats.norm.rvs(loc=1, scale=1, size=500)
  print 'expected = [\'norm\'], actual =', whichDistribution(samples, 0.98)

  # poisson
  samples = stats.poisson.rvs(mu=2, size=500)
  print 'expected = [\'possion\'], actual =', whichDistribution(samples, 0.95)

  # uniform
  samples = stats.uniform.rvs(loc=1, scale=1, size=10)
  print 'expected = [\'uniform\'], actual =', whichDistribution(samples, 0.8, True)

  # lognormal
  samples = stats.lognorm.rvs(s=1, loc=0, scale=10, size=500)
  print 'expected = [\'lognorm\'], actual =', whichDistribution(samples, 0.9, True)
