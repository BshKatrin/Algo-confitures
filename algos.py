# Les imports
import math as m

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
    # Cas de base: si S est exactement 0, on n'a besoin d'aucun pot
    if S == 0:
        return 0
    
    # Cas d'impossibilité: si S est négatif ou qu'il n'y a plus de pots disponibles
    if S < 0 or k == 0:
        return m.inf
    
    # Cas récursif : on choisit soit de ne pas prendre le pot k-1, soit de le prendre
    return min(min_Jars_rec(S, V, k - 1), min_Jars_rec(S - V[k - 1], V, k) + 1)
  
def min_Jars_ite(S: int, V: list[int], k: int) -> int:
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
    int
        Le nombre minimum de pots nécessaires pour atteindre la quantité S, ou
        infini si ce n'est pas possible.
    """
    pass

def algorithm_Glouton(S: int, V: list[int], k: int) -> tuple[int, list[int]]:
    """
    Algorithme glouton pour déterminer le nombre minimum de pots nécessaires 
    pour atteindre la quantité S à partir des capacités disponibles dans V.

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
        return m.inf, []
    
    # Algorithme glouton
    for i in range(k - 1, -1, -1):  # Parcours des pots en partant de la plus grande capacité
        while S >= V[i]:  # Tant qu'on peut prendre le pot de capacité V[i]
            S -= V[i]
            n += 1
            A[i] += 1

    return n, A
