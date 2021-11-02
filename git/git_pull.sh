DEPOTS=$(sh ls_depots.sh)

for depot in $DEPOTS; do
    echo $depot
    cd $depot
    git pull
    cd ..
done
