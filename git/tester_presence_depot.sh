groupe=$1
echo DÉPÔTS MANQUANTS
sh numeros_etudiants.sh $groupe | while read numero;
do
    ls -d $numero 1>/dev/null 2>/dev/null || echo $numero
done



