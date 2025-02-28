import time

def est_valide(plateau, ligne, col, n):
    """ Vérifie si une reine peut être placée en (ligne, col) """
    for i in range(ligne):
        if plateau[i] == col or abs(plateau[i] - col) == abs(i - ligne):
            return False  # Même colonne ou même diagonale
    return True


def calculer_contraintes(plateau, ligne, n):
    """ Retourne une liste de colonnes triées par ordre croissant du nombre de cases bloquées """
    contraintes = []
    for col in range(n):
        if est_valide(plateau, ligne, col, n):
            # Compter combien de cases seront bloquées en plaçant une reine ici
            cases_bloquees = 0
            for i in range(ligne + 1, n):  # Vérifier les lignes suivantes
                for j in range(n):
                    if not est_valide(plateau[:i] + [j], i, j, n):
                        cases_bloquees += 1
            contraintes.append((col, cases_bloquees))

    # Trier les colonnes par nombre croissant de cases bloquées
    contraintes.sort(key=lambda x: x[1])
    return [col for col, _ in contraintes]  # Retourne la liste des colonnes triées


def placer_reines(plateau, ligne, n):
    """ Place les reines en suivant l'heuristique LVD """
    if ligne == n:
        print(plateau)  # Affiche une solution trouvée
        return

    colonnes_ordonnees = calculer_contraintes(plateau, ligne, n)  # Trier les colonnes avec LVD
    for col in colonnes_ordonnees:
        plateau[ligne] = col  # Placer la reine
        placer_reines(plateau, ligne + 1, n)  # Passer à la ligne suivante
        plateau[ligne] = -1  # Backtracking (annuler le choix)


def resoudre(n):
    """ Initialise le plateau et lance la résolution avec LVD """
    plateau = [-1] * n
    start_time = time.time()
    placer_reines(plateau, 0, n)
    end_time = time.time()
    print(end_time - start_time," ms")


# Exécuter avec l'heuristique LVD pour n = 4
resoudre(12)
