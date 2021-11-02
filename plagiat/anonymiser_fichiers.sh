for i in $(find . -maxdepth 1 -type d);
do 
    echo $i
    ag "ca\.cours5b5\." $i -l | while read j; do sed s/ca.cours5b5.[^.]*./ca.cours5b5.anonyme./g -i $j; done
done
