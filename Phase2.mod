# -------------------------------------------------------
# DÉFINITION DES ENSEMBLES
# -------------------------------------------------------

set P;           # Types de transactions
set K2;          # Périodes utiles (issues de Phase 1)
set R{K2};       # Robots disponibles à chaque période k
set P2{K2};      # Types de transactions actifs à la période k


# -------------------------------------------------------
# PARAMÈTRES
# -------------------------------------------------------

param x{P, K2} >= 0;    # Nombre de transactions de type p à traiter à la période k (issues de Phase 1)
param l{K2} >= 0;       # Durée de la période k (en secondes)
param t{P} >= 0;        # Temps d'exécution d'une transaction de type p (en secondes)


# -------------------------------------------------------
# VARIABLES DE DÉCISION
# -------------------------------------------------------

# Nombre de transactions de type p exécutées à la période k par le robot r
var q{k in K2, p in P2[k], r in R[k]} >= 0, integer;

# -------------------------------------------------------
# FONCTION OBJECTIF
# -------------------------------------------------------
maximize total_transactions:
    sum{k in K2, p in P2[k], r in R[k]} q[k, p, r];


# -------------------------------------------------------
# CONTRAINTES
# -------------------------------------------------------

subject to Contrainte10{k in K2, p in P2[k]}:
    sum{r in R[k]} q[k, p, r] <= x[p, k];

subject to Contrainte11{k in K2, r in R[k]}:
    sum{p in P2[k]} q[k, p, r] * t[p] <= l[k];
