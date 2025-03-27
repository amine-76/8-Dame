import random
import math
import time  # Importer le module pour mesurer le temps

# Définir la taille de la grille (nombre de reines)
tailleGrille = 300

# Fonction de calcul de l'énergie de la solution (fitness), ici basée sur le nombre de conflits
def F(reines):
    conflicts = 0
    for i in range(len(reines)):
        for j in range(i + 1, len(reines)):
            # Vérifie les conflits entre reines
            if reines[i] == reines[j] or abs(reines[i] - reines[j]) == abs(i - j):
                conflicts += 1
    return conflicts

# Génère un voisin aléatoire en permutant deux positions de reines
def voisin(X):
    Y = X[:]
    idx1, idx2 = random.sample(range(len(X)), 2)  # Choisit deux indices au hasard
    Y[idx1], Y[idx2] = Y[idx2], Y[idx1]  # Échange les deux reines
    return Y

# Fonction d'acceptation selon la différence d'énergie et la température
def accepte(dF, T):
    if dF < 0:
        return True  # Si le voisin a moins de conflits, on l'accepte toujours
    else:
        A = math.exp(-dF / T)
        return random.random() < A  # Accepte avec une probabilité liée à la température

# Fonction de décroissance de la température
def decroissance(T, D):
    return T * D  # Par exemple, température réduite de D à chaque itération

# Algorithme de recuit simulé
def recuit(X0, Tinit, D, Nt, condition_d_arret):
    X = X0
    T = Tinit
    while not condition_d_arret(X):  # Continue tant que la condition d'arrêt n'est pas remplie
        for _ in range(Nt):
            Y = voisin(X)  # Génère un voisin
            dF = F(Y) - F(X)  # Calcul de la différence de l'énergie (fitness)
            if accepte(dF, T):  # Décide si le voisin est accepté
                X = Y  # Met à jour la solution actuelle avec le voisin
        T = decroissance(T, D)  # Réduit la température en utilisant la décroissance D
    return X

# Fonction d'arrêt simple : on arrête lorsque la solution n'a plus de conflits
def condition_d_arret(X):
    return F(X) == 0  # Arrêt lorsque la solution est valide (0 conflits)

# Initialisation de la solution de manière aléatoire
def initialiser_aleatoirement(tailleGrille):
    solution = list(range(tailleGrille))  # Chaque reine est placée sur une ligne distincte
    random.shuffle(solution)  # Mélange aléatoire pour éviter une structure rigide
    return solution  # Cela produit une permutation aléatoire des indices

# Exemple d'exécution
if __name__ == "__main__":
    # Initialisation de la solution de manière aléatoire
    X0 = initialiser_aleatoirement(tailleGrille)  # Solution initiale aléatoire
    Tinit = 1.0  # Température initiale
    D = 0.99  # Décroissance de la température
    Nt = 5  # Nombre d'itérations par température
    
    # Mesurer le temps d'exécution
    start_time = time.time()  # Heure de début
    
    # Exécution de l'algorithme de recuit simulé
    solution = recuit(X0, Tinit, D, Nt, condition_d_arret)
    
    # Mesurer le temps à la fin de l'exécution
    end_time = time.time()  # Heure de fin
    
    # Affichage de la solution trouvée
    print("Solution trouvée : ", solution)
    print("Nombre de conflits : ", F(solution))
    
    # Calcul et affichage du temps d'exécution
    execution_time = end_time - start_time  # Temps d'exécution
    print(f"Temps d'exécution : {execution_time:.4f} secondes")
