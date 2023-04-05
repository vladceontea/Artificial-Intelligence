# -*- coding: utf-8 -*-
"""
In this file your task is to write the solver function!

"""


def fuzzify(value, start, high, end):
    fuzzy_result = 0
    if value == high:
        fuzzy_result = 1
    elif start <= value < high:
        fuzzy_result = (value-start)/(high-start)
    elif high < value <= end:
        fuzzy_result = (end-value)/(end-high)

    return fuzzy_result


def solver(t, w):
    """
    Parameters
    ----------
    t : TYPE: float
        DESCRIPTION: the angle theta
    w : TYPE: float
        DESCRIPTION: the angular speed omega

    Returns
    -------
    F : TYPE: float
        DESCRIPTION: the force that must be applied to the cart
    or
    
    None :if we have a division by zero

    """

    neg_very_big_t = fuzzify(t, -50, -40, -25)
    neg_big_t = fuzzify(t, -40, -25, -10)
    neg_t = fuzzify(t, -20, -10, 0)
    zo_t = fuzzify(t, -5, 0, 5)
    pos_t = fuzzify(t, 0, 10, 20)
    pos_big_t = fuzzify(t, 10, 25, 40)
    pos_very_big_t = fuzzify(t, 25, 40, 50)

    neg_big_w = fuzzify(w, -10, -8, -3)
    neg_w = fuzzify(w, -6, -3, 0)
    zo_w = fuzzify(w, -1, 0, 1)
    pos_w = fuzzify(w, 0, 3, 6)
    pos_big_w = fuzzify(w, 3, 6, 10)

    t_table = [pos_very_big_t, pos_big_t, pos_t, zo_t, neg_t, neg_big_t, neg_very_big_t]
    w_table = [pos_big_w, pos_w, zo_w, neg_w, neg_big_w]

    force_table = [[0 for y in range(5)] for x in range(7)]
    for x in range(7):
        for y in range(5):
            force_table[x][y] = min(t_table[x], w_table[y])

    pos_very_very_big_f = max(force_table[0][0], force_table[0][1], force_table[1][0])
    pos_very_big_f = max(force_table[0][2], force_table[1][1], force_table[2][0])
    pos_big_f = max(force_table[0][3], force_table[1][2], force_table[2][1], force_table[3][0])
    pos_f = max(force_table[0][4], force_table[1][3], force_table[2][2], force_table[3][1], force_table[4][0])
    zo_f = max(force_table[1][4], force_table[2][3], force_table[3][2], force_table[4][1], force_table[5][0])
    neg_f = max(force_table[2][4], force_table[3][3], force_table[4][2], force_table[5][1], force_table[6][0])
    neg_big_f = max(force_table[3][4], force_table[4][3], force_table[5][2], force_table[6][1])
    neg_very_big_f = max(force_table[4][4], force_table[5][3], force_table[6][2])
    neg_very_very_big_f = max(force_table[5][4], force_table[6][3], force_table[6][4])

    numerator_f = (-32)*neg_very_very_big_f + (-24)*neg_very_big_f + (-16)*neg_big_f + (-8)*neg_f + 0*zo_f + 8*pos_f + 16*pos_big_f + 24*pos_very_big_f + 32*pos_very_very_big_f
    denominator_f = neg_very_very_big_f + neg_very_big_f + neg_big_f + neg_f + zo_f + pos_f + pos_big_f + pos_very_big_f + pos_very_very_big_f

    force = numerator_f/denominator_f

    return force
