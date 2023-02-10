

msiinfo src\test.msi -c 1252 -a "Fatboy" -g 400 -w 2 -p "Intel;1033" -v "{80D117E3-3BB3-4658-8092-B4851F6D82E4}" -u 2 -l "Fatboy"

REM The name of the MSI 
msiinfo src\test.msi -t "Installation Database for Fatboy Media Library - Client" 

REM Product Name 
msiinfo src\test.msi  -j "Fatboy Media Library - Client" 

REM Comments Summary Property. Set by doc
msiinfo src\test.msi -o "This installer database contains the logic and data required to install Fatboy Media Library - Client."  

REM Keywords
msiinfo src\test.msi -k "Installer Fatboy Media Library" 

REM the name of the tool used to create the MSI
msiinfo src\test.msi -n "Fatboy"  



