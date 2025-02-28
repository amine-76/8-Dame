def isValide(plateau, ligne, col, n):
    for i in range(ligne):
        if plateau[i] == col:
            return False
        if abs(plateau[i] - col) == abs(i - ligne):
            return False
    return True


def compter_case_bloquees(plateau, ligne, col, n):
    """
    Calcule combien de cases seront bloquées sur la ligne suivante
    si on place une reine en (ligne, col).
    """
    cases_bloquees = set()
    prochaine_ligne = ligne + 1

    if prochaine_ligne < n:
        cases_bloquees.add(col)  # Bloque la même colonne
        if col - 1 >= 0:
            cases_bloquees.add(col - 1)  # Bloque la diagonale gauche
        if col + 1 < n:
            cases_bloquees.add(col + 1)  # Bloque la diagonale droite

    print(
        f"Si on place une reine en ({ligne}, {col}), cases bloquées en ligne {prochaine_ligne}: {len(cases_bloquees)}")
    return len(cases_bloquees)


def afficher_solution(plateau,n) :
    solution = []
    for i in range(n) :
        ligne_echiquier = ['.'] * n
        ligne_echiquier[plateau[i]] = 'Q'
        solution.append("".join(ligne_echiquier))
    return solution

def placer_reines(plateau, ligne, n, solutions):
    if ligne == n:
        solutions.append(afficher_solution(plateau, n))
        return

    for col in range(n):
        compter_case_bloquees(plateau, ligne, col, n)

        if isValide(plateau, ligne, col, n):
            plateau[ligne] = col
            placer_reines(plateau, ligne + 1, n, solutions)
            plateau[ligne] = -1  # Backtracking


def resoudre(n):
    plateau = [-1] * n
    solutions =[]
    placer_reines(plateau,0,n,solutions)
    return solutions

def afficher_all_solutions(solutions):
    print(f"Nombre de solutions : {len(solutions)}\n")
    for idx,solution in enumerate(solutions):
        print(f"Solution {idx +1}:")
        for ligne in solution:
            print(ligne)
        print("\n")



if __name__ == "__main__":
    n = 4
    solutions = resoudre(n)
    afficher_all_solutions(solutions)