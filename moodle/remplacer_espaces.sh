remplacer_espaces(){
    nom_original="$1"
    nom_sans_espace=$(echo $nom_original | sed "s/[ ]/_/g")

    if [ "$nom_original" != "$nom_sans_espace" ]; then

        mv -v "$nom_original" $nom_sans_espace

    fi
}


parcourir(){
    repertoire_courant="$1"

    # remplacer dans ce répertoire
    find "$repertoire_courant" -mindepth 1 -maxdepth 1 | while read i; 
    do
        remplacer_espaces "$i"
    done

    # parcourir
    find "$repertoire_courant" -mindepth 1 -maxdepth 1 -type d | while read j; 
    do 
        parcourir "$j"
    done
}

parcourir "."


