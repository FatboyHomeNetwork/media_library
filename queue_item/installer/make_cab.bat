REM Makes the cab file which contains the file / dir structure we want to install 




@echo off
dir .\..\bin\ /s /b /a-d >files.txt
makecab /d "CabinetName1=test.cab" /f files.txt
rem del /q /f files.txt