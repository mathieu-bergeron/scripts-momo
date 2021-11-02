output_dir=$(pwd)

depots_dir=$output_dir/../etudiants_5b5



cd $depots_dir

for depot in $(sh ls_depots.sh);
do

    depot=$(basename $depot)

    mkdir $output_dir/$depot 2>/dev/null

    fichiers="GUsagerCourant.java AAcceuil.java PPartie.java PParametres.java Observateur.java Donnees.java DPartie.java DParametres.java"
#fichiers="MPartie.java"
#fichiers="MPartie.java DPartie.java VGrille.java VCase.java"

    for fichier in $fichiers;
    do
      cp -v $(ag -l -G"^\./$depot.*$fichier") $output_dir/$depot/
    done


done

cd $current_dir
