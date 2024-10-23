import math as m
from algos import min_Jars_rec, min_Jars_ite, algorithm_Glouton

# Tests pour l'algorithme I.
assert min_Jars_rec(0, [1, 2, 4], 3) == 0
assert min_Jars_rec(1, [], 0) == m.inf
assert min_Jars_rec(-1, [1, 2, 4], 3) == m.inf
assert min_Jars_rec(18, [1, 5, 10], 3) == 5
assert min_Jars_rec(10, [1, 5, 6], 3) == 2
# assert min_Jars_rec(748, [1, 2, 5, 10, 20, 50, 100, 200], 8) == 9

# Tests pour l'algorithme II.
assert min_Jars_ite(0, [1, 2, 4], 3) == (0, [0, 0, 0])
assert min_Jars_ite(1, [], 0) == (m.inf, [])
assert min_Jars_ite(-1, [1, 2, 4], 3) == (m.inf, [])
assert min_Jars_ite(18, [1, 5, 10], 3) == (5, [3, 1, 1])
assert min_Jars_ite(10, [1, 5, 6], 3) == (2, [0, 2, 0])
assert min_Jars_ite(748, [1, 2, 5, 10, 20, 50, 100, 200], 8) == (9, [1, 1, 1, 0, 2, 0, 1, 3])

# Tests pour l'algorithme III.
assert algorithm_Glouton(0, [1, 2, 4], 3) == (0, [0, 0, 0])
assert algorithm_Glouton(1, [], 0) == (m.inf, [])
assert algorithm_Glouton(-1, [1, 2, 4], 3) == (m.inf, [])
assert algorithm_Glouton(18, [1, 5, 10], 3) == (5, [3, 1, 1])
assert algorithm_Glouton(10, [1, 5, 6], 3) == (2, [0, 2, 0])
assert algorithm_Glouton(748, [1, 2, 5, 10, 20, 50, 100, 200], 8) == (9, [1, 1, 1, 0, 2, 0, 1, 3])
