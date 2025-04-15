import random
import time

# 📌 Paramètres
tailleGrille = 4  
population_size = 4
max_generation = 50
taux_mutation = 0.2

# 📌 Initialisation aléatoire de la population (liste de permutations)
def initialiser_population():
    return [random.sample(range(tailleGrille), tailleGrille) for _ in range(population_size)]

# 📌 Fonction pour compter les conflits (fitness)
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
    return [p / somme for p in prop_pop]

# 📌 Sélection par roulette wheel
def selection(tab_proba, valeur_alea, pop):
    somme = 0
    for i, proba in enumerate(tab_proba):
        somme += proba
        if somme > valeur_alea:
            return pop[i]
    return pop[-1]  # En cas de problème d'arrondi

# 📌 Croisement (crossover)
def croisssement(parent1, parent2):
    enfant = parent1[:]
    ligne_aleatoire = random.randint(0, len(parent2) - 1)
    valeur_a_copier = parent2[ligne_aleatoire]

    if valeur_a_copier in enfant:
        index_a_permuter = enfant.index(valeur_a_copier)
        enfant[index_a_permuter], enfant[ligne_aleatoire] = enfant[ligne_aleatoire], enfant[index_a_permuter]
    else:
        enfant[ligne_aleatoire] = valeur_a_copier

    return enfant

# 📌 Mutation simple : échange de deux positions
def mutation(individu, taux_mutation=taux_mutation):
    if random.random() < taux_mutation:
        i, j = random.sample(range(len(individu)), 2)
        individu[i], individu[j] = individu[j], individu[i]
    return individu

# 📌 Affichage du plateau d'échecs
def printPosition(reines):
    grille = [['_' for _ in range(tailleGrille)] for _ in range(tailleGrille)]
    for i in range(tailleGrille):
        grille[i][reines[i]] = '👸'
    for ligne in grille:
        print(" ".join(ligne))
    print("\n")

# 📌 Algorithme génétique complet
def algo_genetique():
    population = initialiser_population()

    for generation in range(max_generation):
        fitness_pop = [compter_nombre_de_prise(ind) for ind in population]

        # ✅ Si une solution est trouvée
        if 0 in fitness_pop:
            index_solution = fitness_pop.index(0)
            print(f"✅ Solution trouvée à la génération {generation} :")
            printPosition(population[index_solution])
            return population[index_solution]

        # 🔁 Générer nouvelle population
        prop = proportion(fitness_pop)
        norm = normalise(prop)
        norm2 = proportion2(norm)

        nouvelle_population = []

        while len(nouvelle_population) < population_size:
            rand1 = random.uniform(0, 1)
            rand2 = random.uniform(0, 1)

            parent1 = selection(norm2, rand1, population)
            parent2 = selection(norm2, rand2, population)

            while parent1 == parent2:
                rand2 = random.uniform(0, 1)
                parent2 = selection(norm2, rand2, population)

            enfant = croisssement(parent1, parent2)
            enfant = mutation(enfant)
            nouvelle_population.append(enfant)

        population = nouvelle_population

    print("❌ Aucune solution trouvée après", max_generation, "générations.")
    return None

# 📌 Lancement
if __name__ == "__main__":
    start = time.time()
    solution = algo_genetique()
    end = time.time()
    
    if solution:
        print("Solution finale trouvée :", solution)
    else:
        print("Pas de solution trouvée.")
    
    print(f"⏱ Temps d'exécution : {end - start:.4f} secondes")
