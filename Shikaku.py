# Fonction pour lire les données d'un fichier texte (x,y,valeur)
import random as rd 
import math 
import time 
from collections import defaultdict


# ✅ Couleurs de FOND ANSI (background) pour chaque rectangle
BG_COLORS = [
    "\033[41m",  # Rouge
    "\033[42m",  # Vert
    "\033[43m",  # Jaune
    "\033[44m",  # Bleu
    "\033[45m",  # Magenta
    "\033[46m",  # Cyan
    "\033[47m",  # Blanc
    "\033[100m", # Gris foncé
    "\033[101m", # Rouge clair
    "\033[102m", # Vert clair
    "\033[103m", # Jaune clair
    "\033[104m", # Bleu clair
]
RESET = "\033[0m"

def afficher_solution_coloree(solution, largeur, hauteur):
    """
    Affiche une grille avec chaque case colorée avec un fond différent par zone
    """
    grille = [['' for _ in range(largeur)] for _ in range(hauteur)]

    for idx, (_, _, _, (x0, y0, w, h)) in enumerate(solution):
        couleur = BG_COLORS[idx % len(BG_COLORS)]
        lettre = chr(65 + (idx % 26))
        for dy in range(h):
            for dx in range(w):
                grille[y0 + dy][x0 + dx] = f"{couleur} {lettre} {RESET}"

    print("\n🧩 Grille Shikaku colorée (fond) :\n")
    ligne_sep = "+" + "+".join(["───"] * largeur) + "+"
    print(ligne_sep)
    for ligne in grille:
        row = "|".join(cell if cell else "   " for cell in ligne)
        print(f"|{row}|")
        print(ligne_sep)


def lire_grille_depuis_fichier(nom_fichier):
   with open(nom_fichier, 'r') as f:
      lignes = f.readlines()

      # Lecture des dimensions 
      width, height = map(int, lignes[0].strip().split())

      #Lecture des cases avec valeur 
      cases = []
      for ligne in lignes[1:]:
         x, y, valeur = map(int, ligne.strip().split())
         print(f"Lecture de la case : ({x}, {y}) avec valeur {valeur}")
         cases.append((x, y, valeur))

   return width, height, cases

def afficher_grille(largeur, hauteur, cases):
   #Initialiser une grille vide
   grille = [[0 for _ in range(largeur)] for _ in range(hauteur)]

   # Remplir la grille avec les valeurs
   for x, y, valeur in cases:
      grille[y][x] = str(valeur)
      print(f"Placement de la valeur {valeur} à la position ({x}, {y})")
   
   #Afficher la grille
   for ligne in grille:
      print(" ".join(str(cell).rjust(2) for cell in ligne))
      

# generer rectangles valides
def generer_rectangles_valides(x, y, valeur, largeur, hauteur):
    rectangles = []
    for w in range(1, valeur + 1):
        # w * h doit être exactement égal à valeur
        if valeur % w != 0:
            continue
        h = valeur // w

        for dx in range(w):
            for dy in range(h):
                x0 = x - dx  # Calcul du coin supérieur en X
                y0 = y - dy  # Calcul du coin supérieur en Y

                # Vérifie que le rectangle reste entièrement dans la grille
                if 0 <= x0 and x0 + w <= largeur and 0 <= y0 and y0 + h <= hauteur:
                    rectangles.append((x0, y0, w, h))

    return rectangles

def calculer_toutes_possibilites(cases,largeur,hauteur):
      possibilites = {}
      
      for idx, (x,y,val) in enumerate(cases): 
         rectangles = generer_rectangles_valides(x,y,val,largeur,hauteur)
         possibilites[idx] = rectangles
      return possibilites    
     
      

# générer une solution initial de départ pour le récuit simuler 
def generer_solution_initial(cases, possibilites) : 
   solution = []
   for idx,(x,y,val) in enumerate(cases) : 
      rects = possibilites[idx]
      if rects : 
         choisi = rd.choice(rects)
         solution.append((x,y,val,choisi))
      else : 
         print(f"Attention: Aucun rectangle possible pour la case ({x},{y}) avec valeur {val}")
   return solution   
      
# Calcule de la matrice indiquant combien de fois chaque cellule est couverte par un rectangle de la solution
def calculer_matrice_couverture(solution, largeur, hauteur):
    # Initialisation de la matrice à 0
    couverture = [[0 for _ in range(largeur)] for _ in range(hauteur)]

    # Pour chaque rectangle de la solution
    for _, _, _, (x0, y0, w, h) in solution:
        # Marquer les cellules du rectangle
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                if 0 <= y < hauteur and 0 <= x < largeur:
                    couverture[y][x] += 1
    return couverture
 
 
# fonction qui va calculer la fitness c'est à dire le nombre de cheveauchement, et les cellules non couvertes            
def calculer_fitness(solution, largeur, hauteur):
    couverture = calculer_matrice_couverture(solution, largeur, hauteur)
    score_chevauchement = 0
    score_non_couvert = 0

    # parcours de matrice de couverture
    for y in range(hauteur):
        for x in range(largeur):
            if couverture[y][x] == 0:
                # Cellule non couverte
                score_non_couvert += 1
            elif couverture[y][x] > 1:
                # Cellule chevauchée
                score_chevauchement += couverture[y][x] - 1
    # Le score total sera la somme pondérée des deux scores
    # On double le score du chevauchement car il est plus complexe de résoudre un chevauchement
    return 2 * score_chevauchement + score_non_couvert

def generer_solution_voisine(solution, index_case, possibilites):
    nouvelle_solution = solution.copy()

    # Sélectionner le rectangle à changer
    x, y, val = solution[index_case][:3]

    # Trouver un nouveau rectangle possible
    rects = possibilites[index_case]
    if len(rects) > 1:
        # Choisir un rectangle différent de l'actuel
        ancien_rect = solution[index_case][3]
        nouveaux_rects = [r for r in rects if r != ancien_rect]
        if nouveaux_rects:
            nouveau_rect = rd.choice(nouveaux_rects)
            nouvelle_solution[index_case] = (x, y, val, nouveau_rect)
    return nouvelle_solution

def recuit_simulter(cases, largeur, hauteur, temp_initiale=100.0, temp_finale=0.1, alpha=0.995):
    # Prétraitement: calculer toutes les possibilités de rectangles
    possibilites = calculer_toutes_possibilites(cases, largeur, hauteur)

    # Générer une solution initiale
    solution_courante = generer_solution_initial(cases, possibilites)
    meilleure_solution = solution_courante.copy()
    meilleure_fitness = calculer_fitness(meilleure_solution, largeur, hauteur)

    # Calcule la qualité de la solution initiale
    fitness_courante = calculer_fitness(solution_courante, largeur, hauteur)

    # Variables pour suivre l'évolution
    T = temp_initiale
    nb_iterations = 0
    nb_stagnation = 0
    derniere_amelioration = 0
    Nt = 10 *len(cases)

    print(f"Fitness initiale: {fitness_courante}")

    # Boucle principale de récuit simulé
    start_time = time.time()
    while T > temp_finale and nb_stagnation < 10000:
        for _ in range(Nt):
            nb_iterations += 1

            # Générer une solution voisine
            index_case = rd.randint(0, len(cases) - 1)
            solution_voisine = generer_solution_voisine(solution_courante, index_case, possibilites)

            # Calculer la fitness voisine
            fitness_voisine = calculer_fitness(solution_voisine, largeur, hauteur)

            # Différence de fitness de la solution voisine
            dif_fitness = fitness_voisine - fitness_courante

            # Décision d'acceptation
            if dif_fitness <= 0:
                solution_courante = solution_voisine
                fitness_courante = fitness_voisine
                derniere_amelioration = nb_iterations
                nb_stagnation = 0
                # Mise à jour de la nouvelle solution
                if fitness_courante < meilleure_fitness:
                    meilleure_solution = solution_courante.copy()
                    meilleure_fitness = fitness_courante
                    print(f"Nouvelle meilleure fitness: {meilleure_fitness} à l'itération {nb_iterations}")

                    # Si on a trouvé une solution parfaite
                    if meilleure_fitness == 0:
                        print("Solution parfaite trouvée !")
                        return meilleure_solution
            else:
                # On accepte avec une probabilité selon la température
                proba_acceptation = math.exp(-dif_fitness / T)
                if rd.random() < proba_acceptation:
                    solution_courante = solution_voisine
                    fitness_courante = fitness_voisine

            # Compteur de stagnation
            if nb_iterations - derniere_amelioration > 1000:
                nb_stagnation += 1

        # Refroidissement
        T *= alpha

        # Afficher la progression
        if nb_iterations % 1000 == 0:
            temps_ecoule = time.time() - start_time
            print(f"Itération {nb_iterations}, Température: {T:.4f}, "
                  f"Fitness courante: {fitness_courante}, Meilleure: {meilleure_fitness}, "
                  f"Temps écoulé: {temps_ecoule:.2f}s")

    temps_total = time.time() - start_time
    print(f"\nRecherche terminée après {nb_iterations} itérations ({temps_total:.2f}s)")
    print(f"Meilleure solution trouvée avec fitness: {meilleure_fitness}")
    return meilleure_solution
            
  #Vérifié la validité de la solution
def valider_solution(solution, largeur, hauteur):

   couverture = calculer_matrice_couverture(solution, largeur, hauteur)
   
   for y in range(hauteur):
      for x in range(largeur):
         if couverture[y][x] != 1:
               return False
   
   return True

 
def main(): 
   nom_fichier = input("Entrez le chemin du fichier de grille selon la difficulté (Si non chemin par défaut (grids/easy/250220): ")
   nom_fichier ="grids/"+ nom_fichier
   print(f"Lecture du fichier : {nom_fichier}")
   if nom_fichier == "grids/":
      print("Aucun chemin spécifié, utilisation du chemin par défaut : grids/easy/250220")
      nom_fichier = nom_fichier+"easy/250220"
    
   largeur, hauteur, cases = lire_grille_depuis_fichier(nom_fichier)
   print(f"Dimensions : {largeur} x {hauteur}")
   print(f"Nombre de cases : {len(cases)}")
   
   # Afficher la grille initiale
   afficher_grille(largeur, hauteur, cases)
   
   # Lancer le recuit simulé
   print("\n🔄 Lancement du recuit simulé...")
   solution = recuit_simulter(cases, largeur, hauteur)
   
   #Vérfier la validité de la solution
   if valider_solution(solution, largeur, hauteur):
      print("\n✅ Solution valide trouvée !")
   else:
      print("\n❌ Solution invalide ! Fitness :",calculer_fitness(solution, largeur, hauteur))
   
   
   # Afficher la solution 
   afficher_solution_coloree(solution, largeur, hauteur)
 
            
if __name__ == "__main__":
   main()
   
