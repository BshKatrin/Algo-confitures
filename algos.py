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
    Algorithme récursif pour trouver le nombre minimum de pots nécessaires pour 
    distribuer la quantité S selon le système de capacité V.

    Parameters:
    ----------
    S : int
        Volume total de la confiture.
    V : list[int]
        Liste des capacités des pots disponibles.
    k : int
        Le nombre de types de pots disponibles, k = len(V).

    Returns:
    -------
    int
        Le nombre minimum de pots nécessaires pour distribuer la quantité S. 
        Infini si la solution n'existe pas.
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
    Algorithme de programmation dynamique (bottom-up) pour trouver le nombre minimum de pots nécessaires pour
    distribuer la quantité S selon le système de capacité V.
    Les solutions des sous-problèmes incluent le nombre minimum de pots nécessaires ainsi qu'une liste A.

    Parameters:
    ----------
    S : int
        Volume total de la confiture.
    V : list[int]
        Liste des capacités des pots disponibles.
    k : int
        Le nombre de types de pots disponibles, k = len(V).

    Returns:
    -------
    tuple[int, list[int]]
        Un tuple contenant
            - le nombre minimum de pots utilisés
            - une liste A, où A[i] indique le nombre de pots de capacité V[i] utilisé

        Un tuple (inf, []) si la solution n'existe pas.
    """

    # Cas d'impossibilité: si S < 0 ou qu'il n'y a plus de pots disponibles
    if S < 0 or k == 0:
        return (inf, [])

    # Initialisation de la matrice
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


def _calc_A_aux(S: int, m: int, V: list[int], k: int, A: list[int], M: list[list[int]]) -> list[int]:
    """
    Fonction auxiliaire pour 'min_Jars_ite_backtrack'. Elle implémente un algorithme du type
    'retour sur trace'. Cet algorithme calcule une liste A sachant le nombre minimum de pots nécessaires.

    Parameters:
    ----------
    S : int
        Volume total de la confiture.
    m : int
        Le nombre de bocaux minimum.
    V : list[int]
        Liste des capacités des pots disponibles.
    k : int
        Le nombre de types de pots disponibles, k = len(V).
    A : list[int]
        Liste à calculer. Doit être de même taille que la liste V. À l'entrée doit contenir que des 0.
    M: list[list[int]]
        La matrice déjà remplie par des solutions aux sous-problèmes pour 0 <= s <= S, 0 <= i <= k. 
            Elle a été utilisée pour trouver le nombre minimum de pots nécessaires pour S et k.

    Returns:
    -------
    list[int]
        Une liste A, où A[i] indique le nombre de pots de capacité V[i] utilisé.
        A = [] si la solution n'existe pas.
    """

    # Cas d'impossibilité. Doit pas arriver
    if m < 0 or S < 0:
        return []

    # Solution trouvée
    if m == 0 and S == 0:
        return A

    # N'est pas une solution.
    if m == 0 or S < 0 or k == 0:
        return []

    # Trouver min{(S, i-1), (S-V[i], i)}
    m1 = M[S][k-1]
    m2 = inf
    if S - V[k-1] >= 0:
        m2 = M[S-V[k-1]][k]

    # Cas 1: ne pas prendre le bocal de capacite V[i]
    if m1 < m2:
        return _calc_A_aux(S, m, V, k-1, A, M)
    else:
        # Cas 2 : prendre le bocal de capacité V[i]
        A[k-1] += 1
        return _calc_A_aux(S-V[k-1], m-1, V, k, A, M)


def min_Jars_ite_backtrack(S: int, V: list[int], k: int) -> tuple[int, list[int]]:
    """
    Algorithme de programmation dynamique (bottom-up) pour calculer le nombre minimum de pots nécessaires
    distribuer la quantité S selon le système de capacités V.
    Les solutions des sous-problèmes incluent uniquement le nombre minimum de pots nécessaires.
    Une liste A pour (S, V, k) est calculée à l'aide d'un algorithme backtrack.

    Parameters:
    ----------
    S : int
        Volume total de la confiture.
    V : list[int]
        Liste des capacités des pots disponibles.
    k : int
        Le nombre de types de pots disponibles, k = len(V).

    Returns:
    -------
    tuple[int, list[int]]
        Un tuple contenant
            - le nombre minimum de pots utilisés
            - une liste A, où A[i] indique le nombre de pots de capacité V[i] utilisé

        Un tuple (inf, []) si la solution n'existe pas.
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
    A = _calc_A_aux(S, m, V, k, A, M)  # algorithme backtrack
    return m, A


def algorithm_Glouton_aux(S: int, V: list[int], k: int) -> tuple[int, list[int]]:
    """
    Algorithme glouton pour déterminer le nombre minimum de pots nécessaires
    pour distribuer la quantité S selon le système de capacités V qui est glouton-compatible.

    Parameters:
    ----------
    S : int
        Volume total de la confiture.
    V : list[int]
        Liste des capacités des pots disponibles (doit être triée par ordre croissant).
    k : int
        Le nombre de types de pots disponibles, k = len(V).

    Returns:
    -------
    tuple[int, list[int]]
        Un tuple contenant
            - le nombre minimum de pots utilisés
            - une liste A, où A[i] indique le nombre de pots de capacité V[i] utilisé

        Un tuple (inf, []) si la solution n'existe pas.
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
        Le nombre de types de pots disponibles, k = len(V).

    Returns:
    -------
    bool
        True si le système de capacités V est glouton-compatible, False sinon.
    """

    if (k >= 3):
        for s in range(V[2] + 2, V[k - 2] + V[k - 1]):
            for j in range(1, k + 1):
                if (V[j - 1] < s and algorithm_Glouton_aux(s, V, k)[0] > algorithm_Glouton_aux(s - V[j - 1], V, k)[0] + 1):
                    return False
    return True


def algorithm_Glouton(S: int, V: list[int], k: int) -> tuple[int, list[int]]:
    """
    Détermine le nombre minimum de pots nécessaires pour distribuer la quantité S
    selon un système de capacités V quelconque.

    La fonction vérifie si le système est glouton-compatible.
        - Si oui, la solution est obtenue à l'aide de l'algorithme glouton.
        - Si non, un algorithme de programmation dynamique (bottom-up) suivi d'un backtracking est utilisé.

    Parameters:
    ----------
    S : int
        Volume total de la confiture.
    V : list[int]
        Liste des capacités des pots disponibles (doit être triée par ordre décroissant).
    k : int
        Le nombre de types de pots disponibles, k = len(V).

    Returns:
    -------
    tuple[int, list[int]]
        Un tuple contenant
            - le nombre minimum de pots utilisés
            - une liste A, où A[i] indique le nombre de pots de capacité V[i] utilisé

        Un tuple (inf, []) si la solution n'existe pas.
    """

    return algorithm_Glouton_aux(S, V, k) if test_Glouton_Compatible(k, V) else min_Jars_ite_backtrack(S, V, k)
