COMMANDE=$1

DEPOTS=$(sh ls_depots.sh)

for depot in $DEPOTS; do
    echo $depot
    cd $depot
    $COMMANDE
    cd ..
done
