from copy import deepcopy
from math import inf


def readtxt(file: str) -> tuple[int, int, list[int]]:
    """
    Lecture de la quantité S et du système de capacité V à partir d'un fichier texte.
    Parameters:
    ----------
    file : str
        Chemin vers le fichier texte contenant les données du problème.
    Return:
    ------
    tuple[int, int, list[int]]
        La quantité S, le nombre d'éléments k, et la liste des capacités V.
    """

    with open(file, 'r') as f:
        # Lecture des lignes du fichier
        lines = f.readlines()

        # Extraction de S, k, et des éléments de V
        S = int(lines[0].strip())  # La première ligne contient S
        k = int(lines[1].strip())  # La deuxième ligne contient k
        V = [int(x.strip()) for x in lines[2:2+k]]  # Les k lignes suivantes contiennent les éléments de V

    return S, k, V


def min_Jars_rec(S: int, V: list[int], k: int) -> int:
    """
    Fonction récursive pour trouver le nombre minimum de pots nécessaires pour 
    atteindre la quantité S en utilisant un système de capacité V.

    Parameters:
    ----------
    S : int
        La quantité cible à atteindre.
    V : list[int]
        Liste des capacités des pots disponibles.
    k : int
        Le nombre de types de pots disponibles.

    Returns:
    -------
    int
        Le nombre minimum de pots nécessaires pour atteindre la quantité S, ou
        infini si ce n'est pas possible.
    """

    # Cas de base: si S = 0, on n'a besoin d'aucun pot
    if S == 0:
        return 0

    # Cas d'impossibilité: si S < 0 ou qu'il n'y a plus de pots disponibles
    if S < 0 or k == 0:
        return inf

    # Cas récursif : on choisit soit de ne pas prendre le pot k-1, soit de le prendre
    return min(min_Jars_rec(S, V, k - 1), min_Jars_rec(S - V[k - 1], V, k) + 1)


def min_Jars_ite(S: int, V: list[int], k: int) -> tuple[int, list[int]]:
    """
    Fonction itérative pour trouver le nombre minimum de pots nécessaires pour 
    atteindre la quantité S en utilisant un système de capacité V.

    Parameters:
    ----------
    S : int
        La quantité cible à atteindre.
    V : list[int]
        Liste des capacités des pots disponibles.
    k : int
        Le nombre de types de pots disponibles.

    Returns:
    -------
    tuple[int, list[int]]
        Un tuple contenant le nombre minimum de pots utilisés et la liste A,
        où A[i] indique le nombre de pots de capacité V[i] utilisés.
    """

    # Cas d'impossibilité: si S < 0 ou qu'il n'y a plus de pots disponibles
    if S < 0 or k == 0:
        return (inf, [])

    A = [0] * k
    M = [[(0, deepcopy(A)) for _ in range(k+1)] for _ in range(S+1)]

    # Remplir les premières cases de M
    for i in range(k+1):
        # Cas de base : S = 0
        M[0][i] = (0, [0] * k)
    for s in range(S+1):
        # Cas d'impossibilité : S < 0
        M[s][0] = (inf, [inf] * k)

    # Remplir les cases restantes de M
    for i in range(1, k+1):
        for s in range(1, S+1):
            m1, A1 = M[s][i-1]
            if s - V[i-1] < 0:
                m2, A2 = M[s][0]  # m2 = inf, A2 = [inf...inf]
            else:
                m2, A2 = M[s-V[i-1]][i]

            if m1 < m2 + 1:
                M[s][i] = m1, deepcopy(A1)
            else:
                M[s][i] = m2+1, deepcopy(A2)
                M[s][i][1][i-1] += 1

    return M[s][i]


def calc_A_aux(S: int, m: int, V: list[int], i: int, A: list[int]) -> list[int]:
    """
    Fonction récursif qui implémente l'algorithme du type 'retour sur trace'. 
    La fonction calcule une liste A tel que A[i] représente le nombre de bocaux de capacité V[i] à remplir.

    Parameters:
    ----------
    S : int
        La quantité cible à atteindre.
    m : int
        Le nombre de bocaux minimum. 
    V : list[int]
        Liste des capacités des pots disponibles.
    k : int
        Le nombre de types de pots disponibles.
    A : list[int]
        Liste à calculer. Doit être de même taille que la liste V. À l'entrée doit contenir que des 0.
    Returns:
    -------
    tuple[int, list[int]]
        Un tuple contenant le nombre minimum de pots utilisés et la liste A,
        où A[i] indique le nombre de pots de capacité V[i] utilisés.
    """

    # Cas d'impossibilité. Doit pas arriver
    if m < 0 or S < 0:
        return []
    # Solution trouvée
    if m == 0 and S == 0:
        return A

    # N'est pas une solution.
    if m == 0 or S < 0 or i == 0:
        return []

    # Cas 1 : Ne pas prendre le bocal de capacité V[i]
    A1 = calc_A_aux(S, m, V, i-1, A)
    # Si A1 n'est pas vide, prendre A1 en compte
    if A1:
        return A1
    # A1 n'est pas une solution, passer à l'autre cas

    # Cas 2 : prendre le bocal de capacité V[i]
    A[i-1] += 1
    A2 = calc_A_aux(S-V[i-1], m-1, V, i, A)
    # Si A2 n'est pas vide, prendre A2 en compte
    if A2:
        return A2
    # A2 n'est pas une solution
    A[i-1] -= 1


def min_Jars_ite_backtrack(S: int, V: list[int], k: int) -> tuple[int, list[int]]:
    """
    Fonction itérative qui appelle la fonction récursif. 
    Partie itérative : calcul du nombre minimum de pots nécessaires pour atteindre la quantité S en utilisant
        un système de capacité V.
    Partie récursive : calcul de la liste A tel que A[i] représente le nombre de bocaux de capacité V[i] à remplir.

    Parameters:
    ----------
    S : int
        La quantité cible à atteindre.
    V : list[int]
        Liste des capacités des pots disponibles.
    k : int
        Le nombre de types de pots disponibles.

    Returns:
    -------
    tuple[int, list[int]]
        Un tuple contenant le nombre minimum de pots utilisés et la liste A,
        où A[i] indique le nombre de pots de capacité V[i] utilisés.
    """

    # Cas d'impossibilité: si S < 0 ou qu'il n'y a plus de pots disponibles
    if S < 0 or k == 0:
        return inf, []

    M = [[0 for _ in range(k+1)] for _ in range(S+1)]

    # Remplir les premières cases de M
    for i in range(k+1):
        # Cas de base : S = 0
        M[0][i] = 0
    for s in range(S+1):
        # Cas d'impossibilité : S < 0
        M[s][0] = inf

    # Remplir les cases restantes de M
    for i in range(1, k+1):
        for s in range(1, S+1):
            if s - V[i-1] < 0:
                M[s][i] = M[s][i-1]
            else:
                M[s][i] = min(M[s][i-1], M[s-V[i-1]][i] + 1)

    m = M[s][i]  # nombre de bocaux minimum
    A = [0] * k if k else []
    A = calc_A_aux(S, m, V, k, A)  # fonction récursive
    return m, A


def algorithm_Glouton_aux(S: int, V: list[int], k: int) -> tuple[int, list[int]]:
    """
    Algorithme glouton pour déterminer le nombre minimum de pots nécessaires 
    pour atteindre la quantité S à partir d'un système de capacités V glouton-compatible.

    Parameters:
    ----------
    S : int
        La quantité cible à atteindre.
    V : list[int]
        Liste des capacités des pots disponibles (doit être triée par ordre décroissant).
    k : int
        Le nombre de types de pots disponibles.

    Returns:
    -------
    tuple[int, list[int]]
        Un tuple contenant le nombre minimum de pots utilisés et la liste A,
        où A[i] indique le nombre de pots de capacité V[i] utilisés.
    """
    # Initialisation du nombre total de pots utilisés et de la liste des quantités utilisées
    n: int = 0
    A: list[int] = [0] * k

    # Cas d'impossibilité : s'il n'y a pas de pots ou que la quantité S est négative
    if k == 0 or S < 0:
        return inf, []

    # Algorithme glouton
    for i in range(k - 1, -1, -1):  # Parcours des pots en partant de la plus grande capacité
        while S >= V[i]:  # Tant qu'on peut prendre le pot de capacité V[i]
            S -= V[i]
            n += 1
            A[i] += 1

    return n, A


def test_Glouton_Compatible(k: int, V: list[int]) -> bool:
    """
    Vérifie si un système de capacités est glouton-compatible.

    Parameters:
    ----------
    V : list[int]
        Liste des capacités des pots disponibles (doit être triée par ordre décroissant).
    k : int
        Le nombre de types de pots disponibles.

    Returns:
    -------
    bool
        True si le système V, k est glouton-compatible, False sinon.
    """
    if (k >= 3):
        for s in range(V[2] + 2, V[k - 2] + V[k - 1]):
            for j in range(1, k + 1):
                if (V[j - 1] < s and algorithm_Glouton_aux(s, V, k)[0] > algorithm_Glouton_aux(s - V[j - 1], V, k)[0] + 1):
                    return False
    return True


def algorithm_Glouton(S: int, V: list[int], k: int) -> tuple[int, list[int]]:
    """
    Algorithme glouton pour déterminer le nombre minimum de pots nécessaires 
    pour atteindre la quantité S à partir d'un système de capacités V quelconque.

    Parameters:
    ----------
    S : int
        La quantité cible à atteindre.
    V : list[int]
        Liste des capacités des pots disponibles (doit être triée par ordre décroissant).
    k : int
        Le nombre de types de pots disponibles.

    Returns:
    -------
    tuple[int, list[int]]
        Un tuple contenant le nombre minimum de pots utilisés et la liste A,
        où A[i] indique le nombre de pots de capacité V[i] utilisés.
    """
    return algorithm_Glouton_aux(S, V, k) if test_Glouton_Compatible(k, V) else min_Jars_ite(S, V, k)
