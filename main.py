import threading
import time

tailleGrille = 4  # Définition correcte

def resoudre(reines=[]):
    th1 = threading.Thread(target=thread1, args=(len(reines), True, reines))
    th1.start()

    reines = []
    th2 = threading.Thread(target=thread2, args=(len(reines), False, reines))
    th2.start()

    reines = []
    th3 = threading.Thread(target=thread3, args=(len(reines), reines))
    th3.start()


def thread1(taille, bool, tableau):
    start_time1 = time.time()
    heuristique(taille, bool, tableau)
    start_time2 = time.time()
    printPosition(tableau)
    print("Temps d'exécution 1er heuristique (moins de cases bloquantes) : %s secondes" % (start_time2 - start_time1))

def thread2(taille, bool, tableau):
    start_time1 = time.time()
    heuristique(taille, bool, tableau)
    start_time2 = time.time()
    printPosition(tableau)
    print("Temps d'exécution 2ème heuristique (plus de cases bloquantes) : %s secondes" % (start_time2 - start_time1))

def thread3(taille, tableau):
    start_time1 = time.time()
    backtrack(taille, tableau)
    start_time2 = time.time()
    printPosition(tableau)
    print("Temps d'exécution Backtracking simple : %s secondes" % (start_time2 - start_time1))


def heuristique(ligne, croissant, reines):
    if len(reines) == tailleGrille:
        return True
    placements = {}

    for i in range(tailleGrille):
        if estValide(i, reines):
            placements[i] = notation(i, ligne)

    tries = {k: v for k, v in sorted(placements.items(), key=lambda item: item[1], reverse=croissant)}
    for i in tries:
        reines.append(i)
        if heuristique(ligne + 1, croissant, reines):
            return True
        reines.pop()
    return False

def notation(val, ligne):
    res = (tailleGrille - ligne)
    for i in range(tailleGrille):
        res += 1
        if val <= i:
            res += 1
        if val >= i:
            res += 1
    return res


def backtrack(ligne, reines):
    if len(reines) == tailleGrille:
        return True

    for i in range(tailleGrille):
        if estValide(i, reines):
            reines.append(i)
            if backtrack(ligne + 1, reines):
                return True
            reines.remove(i)
    return False

def estValide(val, reines):
    for i in range(len(reines)):
        if reines[i] == val:
            return False
        if val == (reines[i] - (len(reines) - i)) or val == (reines[i] + (len(reines) - i)):
            return False
    return True

def printPosition(reines):
    grille = [[0] * tailleGrille for _ in range(tailleGrille)]
    output = ""
    it = 0

    for i in reines:
        grille[it][i] = 1
        it += 1

    for i in range(tailleGrille):
        for j in range(tailleGrille):
            if grille[i][j] == 1:
                output += "👸 "
            else:
                output += "_ "
        output += "\n"

    print(output)

if __name__ == "__main__":
   #for i in range(10):
        tailleGrille = 8
        print("Taille de la grille :", tailleGrille)
        resoudre()



