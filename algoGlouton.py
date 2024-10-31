# Les imports
import random
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


def ecart(pmax: int, kmax: int, f: int = 100) -> tuple[float, int]:
    """
    Calcule l'écart moyen et maximal entre deux algorithmes sur des systèmes non glouton compatibles.

    Cette fonction génère des ensembles aléatoires de `k` entiers pour chaque `k` compris entre 1 et `kmax`.
    Si un ensemble n'est pas glouton compatible, elle calcule l'écart entre deux algorithmes (min_Jars_ite et algorithm_Glouton)
    en comparant leur résultat sur une série de tests avec des valeurs différentes. L'écart maximal et moyen est alors retourné.

    Parameters
    ----------
    pmax : int
        La valeur maximale que les entiers générés peuvent prendre.
    kmax : int
        Le nombre maximal d'entiers dans chaque ensemble généré.
    f : int, optional
        Facteur multiplicatif utilisé pour ajuster les valeurs testées (par défaut 100).

    Returns
    -------
    tuple[float, int]
        Un tuple contenant l'écart moyen et l'écart maximal entre les deux algorithmes.
    """
    max_ecart: int = 0
    total_ecart: int = 0
    count: int = 0

    # Boucle sur chaque valeur de `k` de 1 à `kmax`
    for k in tqdm(range(1, kmax + 1)):  # Correction : Inclure kmax dans la boucle
        print(k)
        for _ in range(10):
            V = gen_alea_sys(pmax, k)
            
            # Si le système n'est pas glouton compatible
            if not test_Glouton_Compatible(k, V):
                # Comparaison des deux algorithmes sur plusieurs valeurs de `s`
                for s in (pmax, pmax * f):
                    y1, _ = min_Jars_ite(s, V, k)
                    y2, _ = algorithm_Glouton_aux(s, V, k)
                    
                    print(y1, y2)
                    # Calcul des écarts
                    ecart_actuel = abs(y1 - y2)
                    max_ecart = max(max_ecart, ecart_actuel)
                    total_ecart += ecart_actuel
                    count += 1

    if count == 0:
        return (0, 0)
    
    # Retourne l'écart moyen et l'écart maximal
    return (total_ecart / count, max_ecart)
