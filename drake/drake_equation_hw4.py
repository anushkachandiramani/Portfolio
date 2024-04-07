'''
Anushka Chandiramani
Homework 4: The Drake Equation
'''

from drv import DRV

def main():
    # Star formation rate: Given distribution between 1.5 and 3.0 represented as a uniform distribution
    R_star = DRV(dist_type='uniform', min_val=1.5, max_val=3.0,
                 bins=20)

    # Fraction of stars that have planets: Given distribution of 1.0, assuming all stars have planets
    f_p = DRV({1.0:1.0})

    # Among stars that have planets, how many of those can support life:
    # Taken from the given distribution, this assumes there is a 0.2 probability that 10% could,
    # 0.2 probability that 20% could,0.1 probability that 30% could, 0.3 probability that 40% could,
    # and 0.2 probability that 50% could
    n_e = DRV({1:0.2, 2:0.2, 3:0.1, 4:0.3, 5:0.2})

    # Fraction of life-supporting planets that actually develop life: This is speculative,
    # assuming there is a 0.6 probability that 10% of planets will actually develop life,
    # and a 0.4 probability that 20% of planets will actually develop life
    f_l = DRV({0.1:0.6, 0.2:0.4})

    # Fraction of planets with life that develop intelligent life: This is speculative,
    # assuming that there is a 0.4 probability that 10% of planets will develop intelligent life,
    # 0.4 probability that 20% of planets will, and a 0.2 probability that 30% will
    f_i = DRV({0.1:0.4, 0.2:0.4, 0.3:0.2})

    # Fraction of intelligent life-bearing planets that develop technology that releases
    # detectable signals into space: This is speculative, assuming that there is
    # a 0.2 probability that 10% will, a 0.3 probability that 20% will,
    # a 0.4 probability that 30% will, and a 0.1 probability that 40% will
    f_c = DRV({0.1: 0.2, 0.2: 0.3, 0.3: 0.4,
               0.4: 0.1})

    # How many years would an advanced civilization last?: This is speculative, assuming that
    # there is a 0.1 probability that it would last for 100 years, a 0.4 probability that
    # it would last for 10,000 years, a 0.3 probability that it would last for 100,000 years,
    # and a 0.2 probability that it would last for 1,000,000 years
    L = DRV({1000: 0.1, 10000: 0.4, 100000: 0.3,
             1000000: 0.2})

    # Drake equation: multiplies all of the above factors
    N = R_star * f_p * n_e * f_l * f_i * f_c * L

    expected_N = N.expected_value()
    std_dev_N = N.calculate_stdev()

    print(f"Expected number of civilizations: {expected_N}")
    print(f"Standard deviation: {std_dev_N}")

    N.plot(title="Distribution of N", show_cumulative=False, xscale='', yscale='log', trials=100, bins=20)


if __name__ == '__main__':
    main()


"""
The expected number of intelligent civilizations
based on the Drake equation is 79376.414

The standard deviation is 243536.628
"""