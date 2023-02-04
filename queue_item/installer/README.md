# Dev Env Notes #




+ `edit__test_msi.bat` Opens MSI editor - Dev
+ `build__test_msi.bat` add the `*.cab` to the msi. Done each time the *msi file has been updated. 
+ `install__test_msi.bat` Runs as install
+ Output of run is in `test.log`
+ `uninstall__test_msi.bat` Runs as uninstall
+ Output of run  is in `test.log`

## Build Cab File

+ `make_cab.bat` build a cab from `.\..\bin\`. Only need to do this if the *.cab file has been updated.
+ `add_cab__test_msi.bat` adds `.\src\test.cab` to the `.\src\test.msi` file  
