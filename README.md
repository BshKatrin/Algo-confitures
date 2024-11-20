# Algo - Confitures

Ce dépôt contient le code source du projet réalisé dans le cadre de l'UE **Algorithmique II (LU3IN003)**. Ce projet explore plusieurs paradigmes algorithmiques :  
> - **Programmation récursive**.  
> - **Programmation dynamique**, avec et sans retour en arrière (backtracking).  
> - **Algorithmes gloutons**.  

---

## Bibliothèques utilisées

Pour exécuter le code, assurez-vous d'avoir installé les bibliothèques Python suivantes :  
> - `matplotlib`  
> - `pandas`  
> - `numpy`  
> - `tqdm`  

---

## Organisation des fichiers

- **`algos.py`** : Implémente les fonctions des trois algorithmes principaux :  
  > - Algorithme I : Récursif  
  > - Algorithme II : Programmation dynamique (avec et sans backtracking)  
  > - Algorithme III : Glouton  

- **`tests.py`** : Contient des tests pour évaluer chaque algorithme sur de petites instances de problème.

- **`complex.py`** : Gère la génération des données de temps d'exécution des algorithmes. Les résultats sont sauvegardés dans un **DataFrame** et exportés au format `.csv` (dans le dossier `data`).

- **`plot_data.py`** : Permet de générer des graphiques à l'aide de `matplotlib`.  
  > - Le code inclut une gestion des valeurs aberrantes (liées à des anomalies ponctuelles n'étant pas causées par les algorithmes).  
  > - Les graphiques produits sont sauvegardés dans le dossier `images`.  

- **`algoGlouton.py`** : Contient les fonctions suivantes :  
  > - Calcul de la proportion de systèmes compatibles avec l'approche gloutonne.  
  > - Évaluation de l'écart moyen et de l'écart maximal entre la solution optimale et celle fournie par l'algorithme glouton.  

---

## Auteurs

- **Ekaterina BOGUSH**  
- **Rayane NASRI**
