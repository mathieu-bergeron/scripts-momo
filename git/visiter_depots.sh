# améliorer: visiter par groupe
depots=$(sh ls_depots.sh)

for depot in $depots;
do
    ls -d $depot && (
        cd $depot
        pwd
        ls 
        #git log
        bash
    )
done






