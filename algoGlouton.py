# Les imports
import random
import matplotlib
matplotlib.use('Qt5Agg')

from  matplotlib import pyplot as plt
from tqdm import tqdm

from algos import test_Glouton_Compatible, algorithm_Glouton_aux, min_Jars_ite

def gen_alea_sys(pmax: int, k: int) -> list[int]:
    """
    Génère une liste de 'k' entiers aléatoires distincts et croissants dans la plage [1, pmax].
    
    La fonction crée une liste de longueur 'k' où chaque entier est choisi aléatoirement et 
    distinctement dans la plage donnée, puis la liste est triée de manière croissante.

    Parameters
    ----------
    pmax : int
        La valeur maximale que les entiers générés peuvent prendre.
    k : int
        Le nombre d'entiers distincts à générer.

    Returns
    -------
    list[int]
        Une liste triée contenant 'k' entiers aléatoires distincts et croissants.

    Raises
    ------
    ValueError
        Si 'k > pmax', il est impossible de générer 'k' entiers distincts dans l'intervalle [1, pmax].
    """
    
    # Vérification des conditions d'entrée
    if k > pmax:
        raise ValueError("k ne peut pas être supérieur à pmax")
    
    # Générer des entiers distincts en utilisant un ensemble pour éviter les doublons
    ens: set[int] = {1}
    
    # Tirage aléatoire jusqu'à ce que l'ensemble contienne k éléments
    while len(ens) < k:
        ens.add(random.randint(1, pmax))
    
    # Retourner la liste triée des éléments de l'ensemble
    return sorted(ens)

def proportion_sys_comp(pmax: int, kmax: int, x: int) -> float:
    """
    Calcule la proportion de systèmes glouton compatibles générés aléatoirement.

    Cette fonction génère `x` ensembles de `k` entiers aléatoires pour chaque `k` compris entre 1 et `kmax`.
    Pour chaque ensemble, elle vérifie si le système est glouton compatible, et calcule la proportion
    de systèmes qui satisfont cette condition.

    Parameters
    ----------
    pmax : int
        La valeur maximale que les entiers générés peuvent prendre.
    kmax : int
        Le nombre maximal d'entiers dans chaque ensemble généré.
    x : int
        Le nombre de simulations à réaliser pour chaque valeur de `k`.

    Returns
    -------
    float
        La proportion de systèmes glouton compatibles parmi les ensembles générés.
    """
    total_compatible: int = 0

    # Boucle sur chaque valeur de `k` de 1 à `kmax`
    for k in range(1, kmax + 1):  # Correction: début à 1 pour inclure kmax
        for _ in range(x):
            V = gen_alea_sys(pmax, k)
            total_compatible += 1 if test_Glouton_Compatible(k, V) else 0

    return total_compatible / (kmax * x)

def ecart(pmax: int, kmax: int, f: int = 100) -> None:
    """
    Calcule les écarts moyen et maximal entre deux algorithmes pour des systèmes non glouton-compatibles.

    Cette fonction génère des ensembles de capacités (`k` éléments) pour chaque valeur de `k` allant de 1 à `kmax`.
    Pour chaque ensemble généré, si celui-ci n'est pas glouton-compatible, la fonction compare les résultats de deux
    algorithmes (`min_Jars_ite` et `algorithm_Glouton`) en appliquant ces algorithmes à une série de tests
    utilisant des valeurs différentes. Elle calcule ensuite l'écart entre les deux résultats obtenus.

    La fonction affiche un graphique présentant :
    - En abscisse : les différentes valeurs de `k`.
    - En ordonnée : l'écart moyen et l'écart maximal entre les résultats des deux algorithmes.

    Paramètres
    ----------
    pmax : int
        Valeur maximale que peuvent prendre les entiers dans les ensembles générés.
    kmax : int
        Nombre maximal d'éléments dans chaque ensemble généré.
    f : int, optionnel
        Facteur multiplicatif utilisé pour ajuster les valeurs de test (par défaut : 100).
    """
    
    X = list(range(1, kmax + 1))  # Les abscisses, converties en liste.
    Y1 = []    # Les ordonnées (Moyenne des écarts).
    Y2 = []    # Les ordonnées (Écart maximal).

    # Boucle sur chaque valeur de `k` de 1 à `kmax`
    for k in tqdm(X):
        max_ecart = 0
        total_ecart = 0
        count = 0

        for _ in range(10):
            V = gen_alea_sys(pmax, k)
            
            # Si le système n'est pas glouton compatible
            if not test_Glouton_Compatible(k, V):
                # Comparaison des deux algorithmes sur plusieurs valeurs de `s`
                for s in (pmax, pmax * f):
                    y1, _ = min_Jars_ite(s, V, k)
                    y2, _ = algorithm_Glouton_aux(s, V, k)
                    
                    print(k)
                    print(y1, y2)
                    # Calcul des écarts
                    ecart_actuel = abs(y1 - y2)
                    max_ecart = max(max_ecart, ecart_actuel)
                    total_ecart += ecart_actuel
                    count += 1

        if count == 0:
            Y1.append(0.0)
            Y2.append(0.0)
        else:
            Y1.append(total_ecart / count)
            Y2.append(max_ecart)

    # Tracer la courbe
    plt.figure(figsize=(8, 5))
    plt.plot(X, Y1, linestyle='-', color='b', marker='s', label='Écart moyen')
    plt.plot(X, Y2, linestyle='-', color='r', marker='o', label='Écart maximal')
    plt.xlabel('Nombre maximal de bocaux $k$')
    plt.ylabel('Écart moyen et écart maximal')
    plt.legend()  # Ajout des parenthèses ici
    plt.grid(True)
    plt.show()
