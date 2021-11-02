DEPOTS=$(sh ls_depots.sh)

for depot in $DEPOTS; do
    echo $depot
    cd $depot
    git checkout -f master
    cd ..
done
