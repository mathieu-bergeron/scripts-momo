#unzip *.zip

sh remplacer_espaces.sh || exit

for i in $(find . -mindepth 2 -name "*.zip");
do
    repertoire=$(dirname $i)
    fichier=$(basename $i)
    pushd "$repertoire"
    unzip $fichier
    popd
done

for i in $(find . -mindepth 2 -name "*.rar");
do
    repertoire=$(dirname $i)
    fichier=$(basename $i)
    pushd "$repertoire"
    unrar e $fichier
    popd
done

for i in $(find . -mindepth 2 -name "*.7z");
do
    repertoire=$(dirname $i)
    fichier=$(basename $i)
    pushd "$repertoire"
    7z e $fichier
    popd
done
