import threading
import time
import random

tailleGrille = 4  # Définition correcte

def resoudre(reines=[]):
    #th1 = threading.Thread(target=thread1, args=(len(reines), True, reines))
    #th1.start()

    #reines = []
    #th2 = threading.Thread(target=thread2, args=(len(reines), False, reines))
    #th2.start()

    #reines = []
    #th3 = threading.Thread(target=thread3, args=(len(reines), reines))
    #th3.start()

    #reines = []
    #th4 = threading.Thread(target=thread4, args=(len(reines), reines))
    #th4.start()

    reines = []
    th5 = threading.Thread(target=thread5, args=(len(reines), reines))
    th5.start()




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

def thread4(taille, tableau):
    start_time1 = time.time()
    algoPermutationAleatoire(tableau)
    start_time2 = time.time()
    printPosition(tableau)
    print("Temps d'exécution algo permutation aléatoire simple : %s secondes" % (start_time2 - start_time1))

def thread5(taille, tableau):
    start_time1 = time.time()
    algoDescenteGradient(tableau)
    start_time2 = time.time()
    #printPosition(tableau)
    print("Temps d'exécution algo de gradiant : %s secondes" % (start_time2 - start_time1))            

# algo aléatoire 
def algoPermutationAleatoire(reines):
    # pose de reine sur la diagonale
    for i in range(tailleGrille):
        reines.append(i)
    # permutation aléatoire jusqu'a trouver la solution
    while est_en_prise(reines):
        #print("pas de solution")
        index1 = random.randint(0, tailleGrille - 1)
        index2 = random.randint(0, tailleGrille - 1)
        reines[index1], reines[index2] = reines[index2], reines[index1]
        #printPosition(reines)
    print("solution trouvée")    
    return reines 

def algoDescenteGradient(reines):
    # Initialisation des reines sur la diagonale
    for i in range(tailleGrille):
        reines.append(i)
    
    nb_prise = compter_nombre_de_prise(reines)
    print("Nombre initial de prises : ", nb_prise)
    
    while nb_prise > 0:
        copy_reines = reines.copy()
        index1 = random.randint(0, tailleGrille - 1)
        index2 = random.randint(0, tailleGrille - 1)
        
        # Éviter les permutations inutiles
        if index1 == index2:
            continue
        
        # Permutation des reines
        copy_reines[index1], copy_reines[index2] = copy_reines[index2], copy_reines[index1]
        nb_prise_copy = compter_nombre_de_prise(copy_reines)
        
        # Si la permutation améliore ou ne dégrade pas la situation, on l'accepte
        if nb_prise_copy < nb_prise:
            reines = copy_reines.copy()
            nb_prise = nb_prise_copy
            print("Mise à jour nombre de prises : ", nb_prise)
            printPosition(reines)
    
    print("Nombre final de prises : ", nb_prise)
    print("Solution trouvée : ", reines)
    
def est_en_prise(reines):
    for i in range(len(reines)):
        for j in range(i+1, len(reines)):
            if reines[i] == reines[j] or abs(reines[i] - reines[j]) == abs(i - j):
                return True
    return False

#algo qui test si une reine est en prise sur la reine de la ligne du dessus sauf la première reine
def compter_nombre_de_prise(reines):
    nb_prise = 0
    for i in range(1, len(reines)):
        if reines[i] == reines[i-1] or abs(reines[i] - reines[i-1]) == 1:
            nb_prise += 1
    return nb_prise
        

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
        tailleGrille = 20
        print("Taille de la grille :", tailleGrille)
        resoudre()


# Note :
# algo fde la déscente de gradient pour trouver la solution
# On pars de la pose de reine sur la diagonale c'est a dire un nombre de prise très importante
# on crée une copy du tableau de reine et on permute une paire de reine  
#algo aléa
# notion de qualité : on prend une combianaison de reine avec la meilleur note c'est a dire le moins de prise 
# algo de la descente de gradient : note de la qualité + permutation aléatoire



# Note :
# Eviter les permutations inutiles ? 
# Qualt

# Note :
#public class Solution {
#    double fitness(); 
#    Solution neighbor();
#    boolean isOk();
#}

# note :
# Tinit =1.0
# D =0.999
# Nt = 100