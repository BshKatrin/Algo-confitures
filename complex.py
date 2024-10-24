# Les imports
import time
from typing import Callable
import pandas as pd
from algos import min_Jars_rec, min_Jars_ite, algorithm_Glouton, algorithm_Glouton_aux


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
        L'algorithme à exécuter pour chaque combinaison de valeurs de x (quantité de confiture)
        et y (nombre de bocaux). Cette fonction doit prendre trois arguments :
          - x (int) : la quantité de confiture pour l'itération actuelle.
          - V (list) : une liste représentant les capacités des bocaux pour cette itération.
          - y (int) : le nombre de bocaux utilisés pour cette itération.

    Returns:
    --------
    df : pd.DataFrame
        Un DataFrame Pandas contenant les temps d'exécution de la fonction `func`
        pour chaque combinaison de valeurs de x (lignes) et y (colonnes).
        Les lignes sont nommées `s10`, `s20`, ..., `s{Smax-10}` et les colonnes sont nommées `k1`, `k2`, ..., `k{kmax-1}`.
    """

    # Créer les noms des lignes sous la forme s10, s20, ..., jusqu'à Smax
    rows = [f'{x}' for x in range(10, Smax, 10)]

    # Créer les noms des colonnes sous la forme k1, k2, ..., jusqu'à kmax-1
    columns = [f'{x}' for x in range(1, kmax)]
    # Créer un DataFrame vide avec les lignes (rows) et colonnes (columns)
    df = pd.DataFrame(index=rows, columns=columns)

    stop_exec = False
    # Boucle sur chaque valeur de x (incréments de 10) et y (incréments de 1)
    for x in range(10, Smax, 10):
        print(x)
        for y in range(1, kmax):
            # Créer la liste V : les capacités des pots (d est utilisé)
            V = [d ** i for i in range(y)]
            # print(V)
            # Chronométrer l'exécution de la fonction func(x, V, y)
            timeStart = time.time()  # Démarrer le chrono
            func(x, V, y)            # Appeler la fonction `func`
            timeEnd = time.time()    # Arrêter le chrono

            # Stocker la durée d'exécution (sec) dans la cellule correspondante du DataFrame
            df.loc[f'{x}', f'{y}'] = timeEnd - timeStart
            # Arret des calculs si le temps d'execution > max_time
            if max_time and timeEnd - timeStart > max_time:
                stop_exec = True
                break

        if stop_exec:
            break

    # Retourner le DataFrame avec les temps d'exécution (sec)
    return df


def save_csv(csv_name: str, df: pd.DataFrame) -> None:
    # df.to_csv(csv_name, names = )
    df.to_csv(csv_name)


if __name__ == "__main__":
    df = time_cpu(5000, 8, algorithm_Glouton_aux, d=4, max_time=10)
    save_csv("data/test4.csv", df)
    # k = 5
    # V = [3 ** i for i in range(k)]

    # assert (algorithm_Glouton(s, V, k) == min_Jars_ite(s, V, k))
