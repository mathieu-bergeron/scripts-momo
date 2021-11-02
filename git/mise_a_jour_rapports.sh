groupes="1 2"
evaluation=$1

if [ "$evaluation" = ""  ]; then
    echo "usage: sh $0 evaluation"
    exit
fi

for groupe in $groupes;
do
    sh mise_a_jour_rapports_un_groupe.sh $groupe $evaluation
done
