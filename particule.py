import random as rd

# 📌 Paramètres
n = 4 
nb_particules = 10
w = 0.5  # Facteur d'inertie
max_iterations = 100  # Nombre maximal d'itérations
c1 = 1.5  # Coefficient d'attraction vers la meilleure position personnelle
c2 = 1.5  # Coefficient d'attraction vers la meilleure position

# 📌 Génération de l'espace de recherche
def initialisation_espaces(nb_particules, n):
    tab_particules = []
    tableau_vitesses = []

    for i in range(nb_particules):
        # Position : permutation des colonnes (1 reine par colonne)
        position = rd.sample(range(n), n)
        
        # Vitesse : liste de réels, une par colonne
        vitesse = [rd.uniform(0, 1) for _ in range(n)]

        tab_particules.append(position)
        tableau_vitesses.append(vitesse)
        
        print(f"Particule {i} : {position}")
        print(f"Vitesse   {i} : {vitesse}\n")
    
    return tab_particules, tableau_vitesses

# 📌 Fonction de fitness (nombre de conflits)
def calcule_fitness(particule):
    reines_en_conflit = set()
    
    for i in range(len(particule)):
        for j in range(i + 1, len(particule)):
            if abs(particule[i] - particule[j]) == abs(i - j):  # diagonale
                reines_en_conflit.add(i)
                reines_en_conflit.add(j)
    
    return len(reines_en_conflit)


# 📌 Trouver les voisins dans une topologie en anneau
def trouver_meilleur_voisin(particules,fitnesses, index) : 
    gauche =  (index - 1)% len(particules)
    droite = (index + 1)% len(particules)
    voisins  = [gauche,droite]
    meilleur_voisin = min(voisins, key=lambda i: fitnesses[i])
    return particules[meilleur_voisin]
   


# 📌 Main
if __name__ == "__main__":
    tab_particules, tableau_vitesses = initialisation_espaces(nb_particules, n)

    # Calcul de la fitness pour toutes les particules
    fitnesses = [calcule_fitness(particule) for particule in tab_particules]

    for i in range(nb_particules):
        print(f"Fitness de la particule {i} : {fitnesses[i]}")

    for i in range(nb_particules):
        meilleur_voisin = trouver_meilleur_voisin(tab_particules, fitnesses, i)
        print(f"Meilleur voisin de la particule {i} : {meilleur_voisin}")

        print("\n")

    for i in range(len(tab_particules)):
        lbest = trouver_meilleur_voisin(tab_particules, fitnesses, i)

        for j in range(n):
            nouvelle_vitesse = (
                w * tableau_vitesses[i][j] + 
                c1 * rd.uniform(0, 1) * (tab_particules[i][j] - lbest[j]) +
                c2 * rd.uniform(0, 1) * (lbest[j] - tab_particules[i][j])

            )
            tableau_vitesses[i][j] = nouvelle_vitesse
            tab_particules[i][j] += round(nouvelle_vitesse) 
