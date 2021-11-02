cd $(dirname $(readlink -f $0))

sh git_pull.sh

python a_distance_ajouter_questions_repondues.py

python a_distance_mise_a_jour_questions_en_attente.py

python a_distance_etat_du_prof.py

cp a_distance_etat_prof.md ~/montmorency/cours/4b6/

