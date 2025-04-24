import random as rd

# 📌 Paramètres
n = 4 
nb_particules = 10

# 📌 Génération de l'espace de recherche
def initialisation_espaces(nb_particules, n):
    tab_particules = []
    tableau_vitesses = []

    for i in range(nb_particules):
        position = rd.sample(range(n), n)  # permutation unique, pas de doublon de colonnes
        vitesse = [rd.uniform(0, 1) for _ in range(n)]

        tab_particules.append(position)
        tableau_vitesses.append(vitesse)
    return tab_particules, tableau_vitesses

# 📌 Fonction de fitness (nombre de conflits)
def calcule_fitness(particule):
    nb_prise = 0
    for i in range(len(particule)):
        for j in range(i + 1, len(particule)):  
            if abs(particule[i] - particule[j]) == abs(i - j):  # diagonale uniquement
                nb_prise += 1
    return nb_prise

# 📌 Main
if __name__ == "__main__":
    tab_particules, tableau_vitesses = initialisation_espaces(nb_particules, n)

    for i in range(nb_particules):
        fitness = calcule_fitness(tab_particules[i])
        print(f"Fitness de la particule {i} : {fitness}")
