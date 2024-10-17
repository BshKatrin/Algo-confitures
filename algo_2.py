from math import inf
from copy import deepcopy


def AlgoOptimise(S: int, V: list[int]) -> int:
    k = len(V)
    M = [[0 for _ in range(k+1)] for _ in range(S+1)]

    # Init
    for i in range(k+1):
        M[0][i] = 0
    for s in range(S+1):
        M[s][0] = inf

    # Fill matrix
    for i in range(1, k+1):
        for s in range(1, S+1):
            # print(i, V[i-1])
            if s - V[i-1] < 0:
                M[s][i] = M[s][i-1]
            else:
                M[s][i] = min(M[s][i-1], M[s-V[i-1]][i] + 1)

    return M[s][i]


V = [1, 2]
print(AlgoOptimise(5, V))


def AlgoOptimiseTab(S: int, V: list[int]) -> tuple[int, list[int]]:
    k = len(V)
    A = [0] * k
    M = [[(0, deepcopy(A)) for _ in range(k+1)] for _ in range(S+1)]

    # Init
    for i in range(k+1):
        M[0][i] = (0, [0] * k)
    for s in range(S+1):
        M[s][0] = (inf, [inf] * k)

    # Fill matrix
    for i in range(1, k+1):
        for s in range(1, S+1):
            m, A = M[s][i]
            if s - V[i-1] < 0:
                m, A = M[s][i-1]
                M[s][i] = m, deepcopy(A)
                continue
            m1, A1 = M[s][i-1]
            m2, A2 = M[s-V[i-1]][i]
            if m1 < m2 + 1:
                M[s][i] = m1, deepcopy(A1)
            else:
                M[s][i] = m2+1, deepcopy(A2)
                M[s][i][1][i-1] += 1

    return M[s][i]


V = [1, 2, 5, 10, 20, 50, 100, 200]
print(AlgoOptimiseTab(748, V))


def calc_backword(S: int, M: int, V: list[int], A: list[int], i: int) -> list[int]:
    # Solution
    if M == 0 and S == 0:
        return True
    # No solution
    if M == 0 or S < 0 or i == 0:
        return False
    sol1 = calc_backword(S, M, V, A, i-1)
    if sol1:
        return A
    A[i-1] += 1
    sol2 = calc_backword(S-V[i-1], M-1, V, A, i)
    if sol2:
        return A
    A[i-1] -= 1


# V = [1, 2]

S = 748
A = [0] * len(V)
M = AlgoOptimise(S, V)

print(calc_backword(S, M, V, A, len(V)))
