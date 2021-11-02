cat atelier02_ajouts.csv | while read i; do test $(grep -c "$i" atelier02.csv) -eq 0 && echo $i ; done >> atelier02.csv 
