import math
import random
import time
import threading

# Définition de la taille de la grille
tailleGrille = 300  # Peut être modifié pour une autre taille d'échiquier

# 📌 Initialisation des reines en diagonale [0,1,2,3,...,N-1]
def initialiser_diagonale(tailleGrille):
    return list(range(tailleGrille))  # Place les reines sur la diagonale principale

# 🔥 Algorithme de recuit simulé
def recuit_simuler():
    reines = initialiser_diagonale(tailleGrille)  # Initialisation en diagonale
    nb_prises = compter_nombre_de_prise(reines)
    print("Nombre initial de conflits :", nb_prises)

    T, D, Nt = 1.0, 0.99, 5  # Température initiale, taux de refroidissement, itérations par température

    while nb_prises > 0:
        for _ in range(Nt):
            new_reines = reines[:]
            i, j = random.sample(range(tailleGrille), 2)  # Échange deux reines
            new_reines[i], new_reines[j] = new_reines[j], new_reines[i]

            new_prise = compter_nombre_de_prise(new_reines)
            delta = new_prise - nb_prises

            if delta < 0 or random.random() < math.exp(-delta / T):
                reines = new_reines
                nb_prises = new_prise

        T *= D  # Refroidissement

    print("Solution trouvée :", reines)
    printPosition(reines)
    return reines

# 📌 Fonction pour compter les conflits
def compter_nombre_de_prise(reines):
    nb_prise = 0
    for i in range(len(reines)):
        for j in range(i + 1, len(reines)):
            if reines[i] == reines[j] or abs(reines[i] - reines[j]) == abs(i - j):
                nb_prise += 1
    return nb_prise

# 📌 Affichage du plateau d'échecs avec les reines
def printPosition(reines):
    grille = [['_' for _ in range(tailleGrille)] for _ in range(tailleGrille)]
    for i in range(tailleGrille):
        grille[i][reines[i]] = '👸'

    for ligne in grille:
        print(" ".join(ligne))
    print("\n")

# 📌 Fonction principale
if __name__ == "__main__":
    start_time = time.time()
    recuit_simuler()
    end_time = time.time()
    print(f"Temps d'exécution : {end_time - start_time:.4f} secondes")
