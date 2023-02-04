# Send to Installer 

## Overview 

Needs to:
* Sets `MEDIA_LIBRARY` environmental variable to point to media library. The location of media library is selected by teh user at install time 
* Install `queue_item.exe` in program files. Do we care if this is selectable by the user - Fatboy / Queue Item -or- Fatboy Queue Item 
* Copies or creates teh send to short cut in the Send To special dir
* Create the media_library user. this is the account the media_library importer will use to copy the data from the client machine to the server
* turn on admin shares for non domain server machines. turned on in later version of windows 10. 

Will use std windows local installer. so the older *.msi format, not later *.msix. *.msix is web store deployable. Not suitable for this project. 

## How windows installer works

Windows installer is a part of windows. The Send To install is an  *.msi file. The *.msi file contains all the info the Windows needs to install send to, including all the info it needed to find `queue_item.exe` 

### Concepts

App 1 -> M Features 1 -> M Components 1 ->  many things it could own.

Features atomic. are what a user add or remove within an app. 


### MSI files 

+database
+cab and other files


**`*.cab files`**

Part of the instal is to install the 'queue_item.exe' app in the programs the directory and to copy a short cut to a know location. Both those files need to be zipped up ina '*.cab' file.  

1. *.cab

Use `makecab`  - std windows tool- to make a cab file forma file, directory

2. add *.cab to *.msi

Use Msidb.exe to add the cabinet file Mycab.cab msi

`Msidb.exe -d mydatabase.msi -a mycab.cab.` 

3. add to config table

In  Media tables should contain the string: `#mycab.cab.`

### Installer Actions & Properties (aka the template pattern)


## Send To Example 

This uses Send To as an example for what a very simple *.msi looks like. 

### files & directory Structures

| File | Description | path to source | path to target |
|---|---|---|---|
|queue_item.exe|where the action is at!| [SourceDir]\installer\Program Files\Queue Item | [ProgramFilesFolder]\Media Library\send_to_media_library.exe|
|python3.exe|python run time | [SourceDir]\installer\Program Files\Queue Item | [ProgramFilesFolder]\Media Library\send_to_media_library.exe|
|python3.exe|python run time | [SourceDir]\installer\Program Files\Queue Item | [ProgramFilesFolder]\Media Library\send_to_media_library.exe|
|.\lib |python libs to support. can be huge! | [SourceDir]\installer\Program Files\Queue Item | [ProgramFilesFolder]\Media Library\send_to_media_library.exe|

### Registry Updates 


**TODO** Mostly about turning on admin shares in windows 10 


### Short cuts 

| Name | source | target |
|---|---|---|
| media_library_lnk | [SendTo]\Media Library.lnk | [ProgramFilesFolder]\Queue Item\queue_item.exe 'arg1 arg2'|

Shortcut are installed as resources associated  with 

### Users 

To support admin share access a `media_library` account is created. this is an admin account used when accessing media on the client computer 

**TODO**. ideally this account requires the same p/w across both server and client.

## Development Environment Tools

DYI environment. big set of tools. **TODO** check out the make file to see what a basic tool change for building an msi file would look like 

| Tool | Description | 
| ---  | --- |
|Instmsi.exe|Redistributable package for installing the Windows Installer on Windows operating systems earlier than Windows Me. |
|Msicert.exe|Populates the MsiDigitalSignature table and MsiDigitalCertificate table with the digital signature information belonging to external cabinet files in the Media table. |
|Msidb.exe|Imports and exports database tables and streams, merges databases, and applies transforms. |
|Msifiler.exe|Populates the File table with file versions, languages, and sizes based upon a source directory. It can also update the MsiFileHash table with file hashes. |
|Msiinfo.exe|Edits or displays summary information stream. |
|Msimerg.exe|Merges one database into another. |
|Msimsp.exe	|Patch creation tool. The recommended method for generating a patch package is to use a patch creation tool such as Msimsp.exe with PATCHWIZ.DLL. |
|Msistuff.exe|Displays or configures the resources in the Setup.exe bootstrap executable. |
|Msitool.mak |Makefile that can be used to make tools and custom actions. |
|Msitran.exe |Generates a transform or applies a transform file to a database. |
|Msival2.exe |Runs one or a suite of Internal Consistency Evaluators - ICEs.|
|Msizap.exe |Removes Windows Installer information for a product or all products installed on a machine. |
|Orca.exe	|Database editor. Creates and edits .msi files and merge modules. |
|PATCHWIZ.DLL|Generates a Windows Installer patch package from a patch creation properties file (.pcp file). The recommended method for generating a patch package is to use a patch creation tool such as Msimsp.exe with PATCHWIZ.DLL. |
|Wilogutl.exe|Assists the analysis of log files from a Windows Installer installation and displays suggested solutions to errors. |

Above list taken from (https://learn.microsoft.com/en-us/windows/win32/msi/windows-installer-development-tools). These tools are available in the windows 10 SDK. 







### Windows ® Installer. V 5.0.19041.2193 

msiexec /Option <Required Parameter> [Optional Parameter]

## Install Options
```
 </package | /i> <Product.msi>
 Installs or configures a product
 /a <Product.msi>
 Administrative install - Installs a product on the network
 /j<u|m> <Product.msi> [/t <Transform List>] [/g <Language ID>]
 Advertises a product - m to all users, u to current user
 </uninstall | /x> <Product.msi | ProductCode>
 Uninstalls the product
```

### Display Options
```
 /quiet
 Quiet mode, no user interaction
 /passive
 Unattended mode - progress bar only
 /q[n|b|r|f]
 Sets user interface level
 n - No UI
 b - Basic UI
 r - Reduced UI
 f - Full UI (default)
 /help
 Help information
 ```

## Restart Options
```
 /norestart
 Do not restart after the installation is complete
 /promptrestart
 Prompts the user for restart if necessary
 /forcerestart
 Always restart the computer after installation
 ```

## Logging Options
```
 /l[i|w|e|a|r|u|c|m|o|p|v|x|+|!|*] <LogFile>
 i - Status messages
 w - Nonfatal warnings
 e - All error messages
 a - Start-up of actions
 r - Action-specific records
 u - User requests
 c - Initial UI parameters
 m - Out-of-memory or fatal exit information
 o - Out-of-disk-space messages
 p - Terminal properties
 v - Verbose output
 x - Extra debugging information
 + - Append to existing log file
 ! - Flush each line to the log
 * - Log all information, except for v and x options
 /log <LogFile>
 Equivalent of /l* <LogFile>
 ```

## Update Options
```
 /update <Update1.msp>[;Update2.msp]
 Applies update(s)
 /uninstall <PatchCodeGuid>[;Update2.msp] /package <Product.msi | ProductCode>
 Remove update(s) for a product
 ```

## Repair Options
```
 /f[p|e|c|m|s|o|d|a|u|v] <Product.msi | ProductCode>
 Repairs a product
 p - only if file is missing
 o - if file is missing or an older version is installed (default)
 e - if file is missing or an equal or older version is installed
 d - if file is missing or a different version is installed
 c - if file is missing or checksum does not match the calculated value
 a - forces all files to be reinstalled
 u - all required user-specific registry entries (default)
 m - all required computer-specific registry entries (default)
 s - all existing shortcuts (default)
 v - runs from source and recaches local package
```
## Setting Public Properties
```
 [PROPERTY=PropertyValue]
```

Consult the Windows ® Installer SDK for additional documentation on the
command line syntax.

Copyright © Microsoft Corporation. All rights reserved.
Portions of this software are based in part on the work of the Independent JPEG Group.
