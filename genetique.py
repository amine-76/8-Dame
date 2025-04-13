import random
import time

# Définition de la taille de la grille
tailleGrille = 4  
population_size = 4

# 📌 Initialisation aléatoire de la population (liste de permutations)
def initialiser_population():
    return [random.sample(range(tailleGrille), tailleGrille) for _ in range(population_size)]

# 📌 Fonction pour compter les conflits
def compter_nombre_de_prise(reines):
    nb_prise = 0
    for i in range(len(reines)):
        for j in range(i + 1, len(reines)):
            if reines[i] == reines[j] or abs(reines[i] - reines[j]) == abs(i - j):
                nb_prise += 1
    return nb_prise

# 📌 Normalisation et proportion
def normalise(fitness_pop):
    return [1 - fitness for fitness in fitness_pop]

def proportion(fitness_pop):
    return [fitness / population_size for fitness in fitness_pop]

def proportion2(prop_pop):
    somme = sum(prop_pop)
    print("Somme de la proportion normalisée :", somme)
    return [p / somme for p in prop_pop]

# 📌 Sélection par roulette wheel
def selection(tab_proba, valeur_alea, pop):
    tableau_inverser = sorted(tab_proba, reverse=True)
    print("Trie décroissante : ", tableau_inverser)
    somme = 0
    index = 0
    for i, proba in enumerate(tab_proba):
        somme += proba
        if somme > valeur_alea:
            index = i
            break
    print("Somme des probabilités arrêtée à :", somme)
    print("Probabilité sélectionnée :", tab_proba[index])
    return pop[index]

#  Fonction principale regroupant tout le processus de sélection
def executer_selection():
    start_time = time.time()
    
    #  1. Initialisation de la population
    pop = initialiser_population()
    print("Population initiale :", pop)
    
    #  2. Calcul de la fitness
    fitness_pop = [compter_nombre_de_prise(individu) for individu in pop]
    print("Fitness de la population :", fitness_pop)
    
    #  3. Normalisation
    prop_pop = proportion(fitness_pop)
    print("Proportion des fitness :", prop_pop)

    norm_pop = normalise(prop_pop)
    print("Population normalisée :", norm_pop)

    norm_pop2 = proportion2(norm_pop)
    print("Proportion 2 :", norm_pop2)

    #  4. Sélection de deux parents
    random_value1 = random.uniform(0, 1)
    parent1 = selection(norm_pop2, random_value1, pop)

    random_value2 = random.uniform(0, 1)
    parent2 = selection(norm_pop2, random_value2, pop)

    while parent1 == parent2:  # Assurer deux parents distincts
        random_value2 = random.uniform(0, 1)
        parent2 = selection(norm_pop2, random_value2, pop)

    print("Parent 1 sélectionné :", parent1)
    print("Parent 2 sélectionné :", parent2)
    
    end_time = time.time()
    print(f"Temps d'exécution : {end_time - start_time:.4f} secondes")

    return parent1, parent2



def croisssement(parent1, parent2):
    # Étape 1 : L'enfant est une copie du parent1
    enfant = parent1[:]
    print("Enfant initial (copie de Parent 1) :", enfant)
    
    # Étape 2 : Choisir une colonne aléatoire
    ligne_aleatoire = random.randint(0, len(parent2) - 1)
    print("Ligne aléatoire sélectionnée :", ligne_aleatoire)
    
    # Étape 3 : Copier la valeur de la colonne du parent2 dans l'enfant
    valeur_a_copier = parent2[ligne_aleatoire]
    print("Valeur à copier depuis Parent 2 :", valeur_a_copier)

    
    if valeur_a_copier in enfant:
        # Étape 4 : Si la valeur existe déjà, effectuer une permutation
        index_a_permuter = enfant.index(valeur_a_copier)
        enfant[index_a_permuter], enfant[ligne_aleatoire] = enfant[ligne_aleatoire], enfant[index_a_permuter]
    else:
        # Sinon, assigner directement la valeur
        enfant[ligne_aleatoire] = valeur_a_copier
    
    return enfant

#  Exécution de la sélection
if __name__ == "__main__":
    parent1,parent2 = executer_selection()
    enfant = croisssement(parent1,parent2)
    print("Enfant final :", enfant)