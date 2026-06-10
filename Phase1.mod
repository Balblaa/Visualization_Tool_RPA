# ---------------------------------------------------------
# 1. DÉFINITION DES ENSEMBLES
# ---------------------------------------------------------
set P;                      # Type des transactions
set K;                      # Periodes

# ---------------------------------------------------------
# 2. PARAMÈTRES
# ---------------------------------------------------------

param t {P};                # temps requis pour éxécute une transaction P
param d;                    # coût de démarage d'un robots
param c;                    # coût de reconfiguration d'un robot
param v {P};                # volume de transaction pour le type P
param w {K, P} in {0, 1};   # 1 si la transaction peu être fait a la periode K. 0 sinon
param l {K};                # longueur de la periode K
param M;                    # big-M value

# ---------------------------------------------------------
# 3. VARIABLES DE DÉCISION
# ---------------------------------------------------------

var x {K, P} integer >= 0;  # nombre de transaction de type P fait à la periode K
var n {K} integer >= 0;     # nombre de robot requis à la periode K
var y {K} integer >= 0;     # nombre de robot a démarrer à la periode K
var z {K, P} binary;        # 1 si la transaction de type P est éxécuter sur la periode K. 0 sinon

# ---------------------------------------------------------
# 4. FONCTION OBJECTIF
# ---------------------------------------------------------

minimize Nombre_robot:
    sum {p in P, k in K} (n[k] + y[k] * d + z[k, p] * c);

# ---------------------------------------------------------
# 5. CONTRAINTES
# ---------------------------------------------------------

# vérifie que toutes les transactions sont effectuées et au bonne période
subject to Volume {p in P}:
    sum {k in K} (x[k, p] * w[k, p]) == v[p];

# respect de la longueur d'une period
subject to DureePeriod {k in K}:
    sum {p in P} (x[k, p] * t[p] + z[k, p] * c) <= l[k] * n[k];

# démarrage des robots
subject to CoutDemarrage {k in K: k != 1}:
    n[k] - n[k-1] <= y[k];

subject to CoutDemarrage2:
    n[1] == y[1];

subject to CoutDemarrage3 {k in K, p in P}:
    x[k, p] - M * z[k, p] <= 0;