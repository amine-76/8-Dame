# Fonction pour lire les données d'un fichier texte (x,y,valeur)

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


if __name__ == "__main__":
   largeur, hauteur, cases = lire_grille_depuis_fichier("grids/easy/250220")
   print(f"Dimensions : {largeur} x {hauteur}")
   afficher_grille(largeur, hauteur, cases)
   