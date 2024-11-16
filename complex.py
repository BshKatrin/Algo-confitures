import time
from typing import Callable
import pandas as pd
from algos import min_Jars_rec, min_Jars_ite, min_Jars_ite_backtrack, algorithm_Glouton


def time_cpu(Smax: int, kmax: int, func: Callable, d: int, max_time: int = None) -> pd.DataFrame:
    """
    Cette fonction crée un DataFrame pour stocker les temps d'exécution d'une fonction
    d'algorithme appliquée à des quantités de confiture et des capacités de bocaux.

    Parameters:
    -----------
    Smax : int
        La quantité maximale de confiture. Les lignes du DataFrame correspondent aux
        multiples de 10 allant de 10 à Smax, exclusif.

    kmax : int
        Le nombre maximum de bocaux. Les colonnes du DataFrame correspondent aux
        indices de 1 à kmax - 1.

    func : function 
        L'algorithme à exécuter pour chaque combinaison de valeurs de s (quantité de confiture)
        et k (nombre de bocaux). Cette fonction doit prendre trois arguments :
          - s (int) : la quantité de confiture pour l'itération actuelle.
          - V (list) : une liste représentant les capacités des bocaux pour cette itération.
          - k (int) : le nombre de bocaux utilisés pour cette itération.
    d : int
        La valeur pour remplir le système de capacité V (V[i] = d^{i})

    max_time : int (default = None)
        Temps CPU maximum pour l'exécution de func (en secondes).
        Les calculs pour les valeurs supérieures s'arrêtent si le temps d'exécution de func dépasse max_time.
        Les lignes restantes du DataFrame retourné seront vides.

    Returns:
    --------
    df : pd.DataFrame
        Un DataFrame Pandas contenant les temps d'exécution de la fonction func
        pour chaque combinaison de valeurs de s (lignes) et k (colonnes).
        Les lignes sont associées aux valeurs de S (10, 20, ..., Smax-10). 
        Les colonnes sont associées aux valeurs de k (1, 2, ..., kmax-1).
    """

    # Créer des lignes associées aux valeurs de s (10, 20, ..., Smax-10)
    rows = [f'{s}' for s in range(10, Smax, 10)]

    # Créer des colonnes associées aux valeurs de k (1, 2, ..., kmax-1)
    columns = [f'{k}' for k in range(1, kmax, 2)]

    # Créer un DataFrame vide avec les lignes (rows) et colonnes (columns)
    df = pd.DataFrame(index=rows, columns=columns)

    # Flag de l'arrêt d'exécution si le temps dépasse max_time
    stop_exec = False

    # Boucle sur chaque valeur de s (incréments de 10) et k (incréments de 1)
    for s in range(10, Smax, 10):
        for k in range(2, kmax+1):

            # Créer la liste V : les capacités des pots (d est utilisé)
            V = [d ** i for i in range(k)]
            # Chronométrer l'exécution de la fonction func(x, V, y)
            timeStart = time.time()  # Démarrer le chrono
            func(s, V, k)
            timeEnd = time.time()    # Arrêter le chrono

            # Stocker la durée d'exécution (sec) dans la cellule correspondante du DataFrame
            df.loc[f'{s}', f'{k}'] = timeEnd - timeStart

            # Arrêt des calculs si le temps d'execution > max_time
            if max_time and timeEnd - timeStart > max_time:
                stop_exec = True
                break

        # Arrêt des calculs si le temps d'execution > max_time
        if stop_exec:
            break

    # Retourner le DataFrame avec les temps d'exécution (sec)
    return df


if __name__ == "__main__":
    S = 10000
    k = 6
    d = 3
    func = min_Jars_ite_backtrack
    f_name = {algorithm_Glouton: "glouton", min_Jars_ite: "ite",
              min_Jars_rec: "rec", min_Jars_ite_backtrack: "backtrack"}

    df = time_cpu(S, k, func, d, max_time=30)
    # df.to_csv(f"data/{f_name[func]}_s{S}_k{k}_d{d}.csv")
