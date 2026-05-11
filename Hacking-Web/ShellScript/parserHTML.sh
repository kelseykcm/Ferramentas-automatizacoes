#/bin/bash

ARQLOG=ARQLOG.txt

echo "Digite o dominio : "
read -p domain
 
wget -vc $domain
at index.html | grep href | grep http | cut -d "/" -f 3 | grep "\." | grep -v " " | grep -v "replace" | sort -u
