sh git_pull.sh

echo ""
echo ""
echo "------------------"
echo "NOUVELLES REPONSES"
echo "------------------"

python a_distance_ajouter_questions_repondues.py

echo ""
echo ""
echo "-------------------"
echo "NOUVELLES QUESTIONS"
echo "-------------------"

python a_distance_mise_a_jour_questions_en_attente.py
