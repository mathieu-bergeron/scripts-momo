numero=0
find . -maxdepth 1 -type d | while read i;
do
    if [ "$i" != "." ]; then
        nouveau_dossier=$(printf "%02d" $numero)
        echo $nouveau_dossier $i  >> noms.txt
        mv -v $i $nouveau_dossier
        numero=$(($numero+1))
    fi
done
