'''
Anushka Chandiramani
File: drv.py
To be imported into HW4
'''


import copy
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import random

class DRV:
    """ A model for discrete random variables where outcomes are numeric """

    def __init__(self, dist=None, dist_type='discrete', min_val=None, max_val=None, mean=None, stdev=None, bins=None):
        """ Constructor """
        self.dist_type = dist_type
        self.min_val = min_val
        self.max_val = max_val
        self.mean = mean
        self.stdev = stdev
        self.bins = bins

        if dist_type == 'discrete':
            self.dist = copy.deepcopy(dist) if dist is not None else {}
        elif dist_type == 'uniform':
            self.dist = self._create_uniform_distribution(min_val, max_val, bins)
        elif dist_type == 'normal':
            self.dist = self._create_normal_distribution(mean, stdev, bins)

    def _create_uniform_distribution(self, min_val, max_val, bins):
        step = (max_val - min_val) / bins
        dist = {min_val + i * step: 1 / bins for i in range(bins)}
        return dist

    def _create_normal_distribution(self, mean, stdev, bins):
        x = np.linspace(mean - 3 * stdev, mean + 3 * stdev, bins)
        pdf = 1 / (stdev * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mean) / stdev) ** 2)
        pdf /= pdf.sum() * (x[1] - x[0])  # Normalize so that the sum of probabilities equals 1
        dist = {x[i]: pdf[i] for i in range(bins)}
        return dist

    def __getitem__(self, x):
        return self.dist.get(x, 0.0)

    def __setitem__(self, x, p):
        if x in self.dist:
            self.dist[x] += p
        else:
            self.dist[x] = p

    def apply(self, other, op):
        """ Apply a binary operator to self and other """
        Z = DRV()
        items = self.dist.items()
        oitems = other.dist.items()
        for x, px in items:
            for y, py in oitems:
                Z[op(x, y)] += px * py
        return Z

    def applyscalar(self, a, op):
        Z = DRV()
        items = self.dist.items()
        for x, p in items:
            Z[op(x,a)] += p
        return Z

    def __add__(self, other):
        return self.apply(other, lambda x, y: x + y)

    def __radd__(self, a):
        return self.applyscalar(a, lambda x, c: c + x)

    def __rmul__(self, a):
        return self.applyscalar(a, lambda x, c: c * x)

    def __rsub__(self, a):
        return self.applyscalar(a, lambda x, c: c - x)

    def __sub__(self, other):
        return self.apply(other, lambda x, y: x - y)

    def __mul__(self, other):
        return self.apply(other, lambda x, y: x * y)

    def __truediv__(self, other):
        # might require div by 0 handling
        return self.apply(other, lambda x, y: x / y)

    def __pow__(self, other):
        return self.apply(other, lambda x, y: x ** y)

    def __repr__(self):
        xp = sorted(self.dist.items())
        rslt = ''
        for x, p in xp:
            rslt += str(round(x)) + " : " + str(round(p, 8)) + "\n"
        return rslt

    def expected_value(self):
        """Compute the expected value of the discrete random variable."""
        return sum(x * p for x, p in self.dist.items())

    def calculate_stdev(self):
        """Compute the standard deviation of the discrete random variable."""
        mean = self.expected_value()
        variance = sum(p * (x - mean) ** 2 for x, p in self.dist.items())
        return np.sqrt(variance)

    def random(self):
        """Generate a random sample from the distribution"""
        if self.dist_type == 'discrete':
            return random.choices(list(self.dist.keys()), weights=list(self.dist.values()))[0]
        elif self.dist_type == 'uniform':
            return random.uniform(self.min_val, self.max_val)
        elif self.dist_type == 'normal':
            return random.normalvariate(self.mean, self.stdev)

    def plot(self, title='', xscale='', yscale='',
             trials=0, bins=20, show_cumulative=False):
        """Display the DRV distribution"""

        if trials == 0:
            plt.bar(self.dist.keys(), self.dist.values())
        else:
            sample = [self.random() for i in range(trials)]
            sns.displot(sample, kind='hist', stat='probability', bins=bins)


        plt.title(title)
        plt.xlabel('value')
        plt.ylabel('probabilities')
        plt.grid()

        if xscale == 'log':
            plt.xscale(xscale)

        if yscale == 'log':
            plt.yscale(yscale)

        if show_cumulative:
            plt.yticks([0.0, 0.25, 0.50, 0.75, 1.00])
            xp = sorted(list(self.dist.items()))
            xval = [t[0] for t in xp]
            pval = [t[1] for t in xp]
            totalp = 0.0
            pcumul = []
            for p in pval:
                totalp += p
                pcumul.append(totalp)
            sns.lineplot(x=xval, y=pcumul)

        plt.show()