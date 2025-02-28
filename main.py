import time

def est_valide(plateau, ligne, col, n):
    """ Vérifie si une reine peut être placée en (ligne, col) """
    for i in range(ligne):
        if plateau[i] == col or abs(plateau[i] - col) == abs(i - ligne):
            return False  # Même colonne ou même diagonale
    return True

def calculer_contraintes(plateau, ligne, n, inverse=False):
    """ Retourne une liste de colonnes triées selon l'heuristique choisie """
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

    # Trier les colonnes par nombre croissant (LVD) ou décroissant (HVD) de cases bloquées
    contraintes.sort(key=lambda x: x[1], reverse=inverse)
    return [col for col, _ in contraintes]  # Retourne la liste des colonnes triées

def placer_reines(plateau, ligne, n, inverse=False):
    """ Place les reines en suivant l'heuristique choisie """
    if ligne == n:
        # print(plateau)  # Décommentez si vous voulez voir les solutions
        return

    colonnes_ordonnees = calculer_contraintes(plateau, ligne, n, inverse)  # Trier selon l'heuristique
    for col in colonnes_ordonnees:
        plateau[ligne] = col  # Placer la reine
        placer_reines(plateau, ligne + 1, n, inverse)  # Passer à la ligne suivante
        plateau[ligne] = -1  # Backtracking (annuler le choix)

def resoudre(n):
    """ Compare les temps d'exécution des deux heuristiques """
    plateau = [-1] * n

    # Test avec LVD (Least Constraining Value)
    start_time = time.time()
    placer_reines(plateau, 0, n, inverse=False)
    end_time = time.time()
    print(f"Temps avec LVD (moins bloquant) pour n={n}: {end_time - start_time:.6f} s")

    # Test avec HVD (Most Constraining Value)
    start_time = time.time()
    placer_reines(plateau, 0, n, inverse=True)
    end_time = time.time()
    print(f"Temps avec HVD (plus bloquant) pour n={n}: {end_time - start_time:.6f} s")

# Exécuter la comparaison pour n = 12
resoudre(16)
