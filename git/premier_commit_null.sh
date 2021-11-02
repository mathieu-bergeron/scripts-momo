for depot in $(sh ls_depots.sh); do

	cd $depot

	si_null=$(cat premier_commit.txt | grep null)

	if [ "$si_null" == "null" ]; then
		
		echo $depot
	fi	

	cd ..
done

