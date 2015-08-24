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
  p = np.array([(i + 0.5) / n for i in xrange(n)])
  return samples, n, mean, stddev, p

# fit samples with q, return R^2


def compute_r_squared(samples, q):
  # linear regression
  slope, intercept, r_value, p_value, std_err = stats.linregress(samples, q)
  r_squared = r_value ** 2

  return r_squared


def isExp(samples, min_r_squared=0.95):
  samples, n, mean, stddev, p = preprosses(samples)
  # estimate lambda
  l = 1 / mean
  # generate quartiles
  q = - np.log(1 - p) / l
  return compute_r_squared(samples, q) > min_r_squared, {'lambda': l}


def isBeta(samples, min_r_squared=0.95):
  samples, n, mean, stddev, p = preprosses(samples)
  # estimate alpha, beta
  a = samples.min()
  c = samples.max()

  x_bar = (mean - a) / (c - a)
  v_bar = stddev ** 2 / (c - a) ** 2

  if v_bar < x_bar * (1 - x_bar):
    alpha = x_bar * (x_bar * (1 - x_bar) / v_bar - 1)
    beta = (1 - x_bar) * alpha
    print 'a,b=', alpha, beta
    print stats.beta.fit(samples, alpha, beta)
    # q = np.array([stats.beta.ppf()])
    # return compute_r_squared(samples, q) > min_r_squared, {'alpha':alp}
    return False, {}
  else:
    return False, {}


def isUniform(samples, min_r_squared=0.95):
  samples, n, mean, stddev, p = preprosses(samples)
  q = stddev * math.sqrt(3) * (2 * p - 1) + mean
  return compute_r_squared(samples, q) > min_r_squared, {
      'a': np.min(samples), 'b': np.max(samples)}


def isNormal(samples, min_r_squared=0.95):
  samples, n, mean, stddev, p = preprosses(samples)
  miu, sigma = stats.norm.fit(samples)
  q = np.array([stats.norm.ppf(pp, loc=miu, scale=sigma) for pp in p])
  return compute_r_squared(
      samples, q) > min_r_squared, {'miu': miu, 'sigma': sigma}


def isLogNormal(samples, min_r_squared=0.95):
  if np.sum(samples > 0) == len(samples):
    r, p = isNormal(np.log(samples), min_r_squared)
    # s, miu, sigma = stats.lognorm.fit(samples)
    # return r, {'s': s, 'miu': miu, 'sigma': sigma}
    return r, p
  else:
    return False, {}


def isPoisson(samples, min_r_squared=0.95):
  samples, n, mean, stddev, p = preprosses(samples)
  q = np.array([stats.poisson.ppf(pp, mu=mean, loc=mean) for pp in p])
  return compute_r_squared(
      samples, q) > min_r_squared, {'mu': mean, 'miu': mean}


def isPowerlaw(samples, min_r_squared=0.95):
  samples, n, mean, stddev, p = preprosses(samples)
  min_value = samples.min()
  if min_value == 0 or np.sum(samples < 0) > 0:
    return False, {}
  alpha = 1 + n / np.sum(np.log(samples / min_value))
  alpha, loc, scale = stats.powerlaw.fit(samples, alpha)
  q = np.array([stats.powerlaw.ppf(pp, alpha, loc=loc, scale=scale)
                for pp in p])
  return compute_r_squared(samples, q) > min_r_squared, {
      'alpha': alpha, 'miu': loc, 'sigma': scale}


def isDistribution(samples, distribution, min_r_squared=0.95):
  if distribution not in m.keys():
    print 'Error, unknonwn distribution type:', distribution
    return None

  return m[distribution](samples, min_r_squared)


def whichDistribution(samples, min_r_squared=0.95):
  d = {}
  for name in m:
    result, parameters = isDistribution(samples, name, min_r_squared)
    if result:
      d[name] = parameters
  if len(d) == 0:
    d = {'None': {}}
  return d

m = {
    'exp': isExp,
    'norm': isNormal,
    'possion': isPoisson,
    'uniform': isUniform,
    'lognorm': isLogNormal,
    'powerlaw': isPowerlaw
    # 'beta': isBeta
}

if __name__ == '__main__':
  samples = stats.powerlaw.rvs(2, loc=0, scale=1, size=500)
  print 'expected = [\'powerlaw\'], actual =', whichDistribution(samples, 0.98)

  samples = stats.expon.rvs(loc=1, scale=1, size=500)
  print 'expected = [\'exp\'], actual =', whichDistribution(samples, 0.98)

  # normal
  samples = stats.norm.rvs(loc=1, scale=1, size=500)
  print 'expected = [\'norm\'], actual =', whichDistribution(samples, 0.98)

  # poisson
  samples = stats.poisson.rvs(mu=2, size=500)
  print 'expected = [\'possion\'], actual =', whichDistribution(samples, 0.98)

  # uniform
  samples = stats.uniform.rvs(loc=1, scale=1, size=500)
  print 'expected = [\'uniform\'], actual =', whichDistribution(samples, 0.98)

  # lognormal
  samples = stats.lognorm.rvs(s=1, loc=0, scale=3, size=500)
  print 'expected = [\'lognorm\'], actual =', whichDistribution(samples, 0.9)
