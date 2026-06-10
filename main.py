from amplpy import AMPL
import json

#region --- PHASE 1 ---
ampl1 = AMPL()
ampl1.read("Phase1.mod")
ampl1.read_data("Phase1.dat")

ampl1.set_option("solver", "highs")
ampl1.solve()
#endregion --- PHASE 1 ---

#region --- Resultat Phase 1 --> .dat de phase 2 ---
# Notre set_P (identique a celui d'avant)
set_P = ampl1.get_set("P").get_values().to_list()

# Résultat de la phase (variable n et x)
res_n = ampl1.get_variable("n").get_values().to_dict()  # {k: valeur}
res_x = ampl1.get_variable("x").get_values().to_dict()  # {(k, p): valeur}

# récupère les périodes où des robot son actif
K2 = [k for k, n_robots in res_n.items() if n_robots > 0]

# notre set R
# {k: list des robots actif}
R_dict = {k: list(range(1, int(res_n[k]) + 1)) for k in K2}

# notre P2 : Types de transactions actifs à la période k
P2_dict = {}
for k in K2:
    P2_dict[k] = [p for (k_idx, p), qty in res_x.items() if k_idx == k and qty > 0]

# les trois paramètres
param_x_phase2 = {(p, k): qty for (k, p), qty in res_x.items() if k in K2 and qty > 0}

param_l_complet = {int(k): val for k, val in ampl1.get_parameter("l").get_values().to_dict().items()}
param_l_phase2 = {k: param_l_complet[k] for k in K2 if k in param_l_complet}
param_t_phase2 = ampl1.get_parameter("t").get_values().to_dict()
#endregion --- Resultat Phase 1 --> .dat de phase 2 ---

#region --- PHASE 2 ---
ampl2 = AMPL()
ampl2.read("Phase2.mod")

# Déclaration des ensembles de base et indexés
ampl2.get_set("P").set_values(set_P)
ampl2.get_set("K2").set_values(K2)
ampl2.get_set("R").set_values(R_dict)
ampl2.get_set("P2").set_values(P2_dict)

# Déclaration des paramètres
ampl2.get_parameter("l").set_values(param_l_phase2)
ampl2.get_parameter("t").set_values(param_t_phase2)
ampl2.get_parameter("x").set_values(param_x_phase2)

ampl2.set_option("solver", "highs")
ampl2.solve()
#endregion --- PHASE 2 ---

#region --- Extraction de q : {(k, p, r): quantité} ---

# Ici q_dict_raw est un dictionnaire avec des couples
#   key = tuple q : (k, p, r)
#   value = int volume : volume traiter par q
q_dict_raw = ampl2.get_variable("q").get_values().to_dict()

resultats = []
for q, volume in q_dict_raw.items():
    qty = round(float(volume))
    if qty <= 0:
        continue
    k, p, r = (int(x) for x in q)
    resultats.append({"periode": k, "transaction": p, "robot": r, "qte_volume": qty})
#endregion --- Extraction de q : {(k, p, r): quantité} ---

#region --- Sérialisation des paramètres ---
output = {
    "transactions": resultats,
    "duree_periode": {str(k): v for k, v in param_l_phase2.items()},
    "nb_robot_periode": {str(int(k)): int(v) for k, v in res_n.items() if v > 0},
    "duree_transaction": {str(int(k)): v for k, v in param_t_phase2.items()},
}

"""
Le Fichier json générer contient 4 information :
Transaction       : Tout les transaction effectuer par les robots au différente période. (q)
duree_periode     : La durée de chacune des périodes du K2
nb_robot_periode  : Le nombre de robot a chaque période K2
duree_transaction : La durée nécéssaire pour traiter chaque type de transaction
"""

with open("resultats.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)
#endregion --- Sérialisation des paramètres ---