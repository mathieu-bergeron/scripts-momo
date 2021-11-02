#ls -1 | egrep '[0-9]{7}'
find . -maxdepth 1 -type d | grep -v "\.$" | grep -v tutoriels_java
