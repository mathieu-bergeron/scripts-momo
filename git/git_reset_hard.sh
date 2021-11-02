DEPOTS=$(sh ls_depots.sh)

for depot in $DEPOTS; do
    echo $depot
    cd $depot
    git checkout master
    git reset --hard
    cd ..
done
