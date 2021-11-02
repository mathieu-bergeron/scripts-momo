groupe=$1
evaluation=$2

if [ "$groupe" = "" -o "$evaluation" = ""  ]; then
    echo "usage: sh $0 groupe evaluation"
    exit
fi

depots=$(sh numeros_etudiants.sh $groupe | while read i; do test -e $i && echo $i; done)

git_pull(){

    git pull
}

lire_git_log(){

    if [[ ! -e lire_git_log.py ]]; then

        ln -s ~/montmorency/cours/5b5/progression_git/lire_git_log.py .
    fi

    ./lire_git_log.py HEAD DEBUT > /dev/null

    mv -v $depot.pickle ~/montmorency/cours/5b5/progression_git/eval0$evaluation/

}

generer_rapport(){

    pushd ~/montmorency/cours/5b5/progression_git/eval0$evaluation/

    set -x
    python ../visualiser_progres.py ../groupe0"$groupe"_eval0"$evaluation".pickle $depot.pickle
    set +x

    popd >/dev/null 2>/dev/null


}



mise_a_jour_un_etudiant(){

    depot=$1

    cd $depot

    git_pull

    lire_git_log

    generer_rapport

    cd ..

}


for depot in $depots; do

    mise_a_jour_un_etudiant $depot

done
