DEPOTS=$(sh ls_depots.sh)

for depot in $DEPOTS; do
    echo $depot
    cd $depot
    git checkout prof
    fichier_settings=$(ag -gsettings.gradle)
    sed "/rootProject/s/'\(.*\)'/'\1_prof'/" -i $fichier_settings
    cd ..
done
