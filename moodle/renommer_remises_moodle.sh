fichier_colnet=$1

if [ "$fichier_colnet" = "" ]; then
    echo "usage: sh $0 groupe_colnet.csv"
    exit
fi

echo "[AVERTISSEMENT] le script assume que chaque nom de famille est unique"


find . -type d | egrep '[0-9]{7}' | while read remise;
do


    nom_de_famille=$(echo $remise | cut -d" " -f2 | cut -d"_" -f1)

    ligne_csv=$(cat $fichier_colnet | grep $nom_de_famille)

    if [ "ligne_csv" == "" ]; then

        echo "[ERREUR] étudiant pas trouvé: $nom_de_famille"

    fi

    nom_de_famille=$(echo $ligne_csv | cut -d";" -f1)
    prenom=$(echo $ligne_csv | cut -d";" -f2)
    numero_etudiant=$(echo $ligne_csv | cut -d";" -f3 | egrep -o '[0-9]{7}$')

    nom_fichier=$numero_etudiant"_"$prenom"_"$nom_de_famille

    nom_fichier=$(echo $nom_fichier | sed 's/ /_/')

    mv -v "$remise" "$nom_fichier"

done
