COMMANDE=$1

DEPOTS=$(sh ls_depots.sh)

for depot in $DEPOTS; do
    cd $depot

    test -e verifier_glog.py || ln -v -s ~/montmorency/cours/5b5/scripts/verifier_glog.py

    echo -n $depot
    python verifier_glog.py

    cd ..
done
