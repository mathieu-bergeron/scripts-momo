groupe=$1
cat 4205B5MO-00000$groupe.csv | egrep -o '[0-9]{9}' | sed s/20//
