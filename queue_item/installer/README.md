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

### Installer Actions & Properties (aka the template pattern)


## Send To Example 

This uses Send To as an example for what a very simple *.msi looks like. 

### Directory files 

| File | Description | path to source | path to target |
|---|---|---|---|
|queue_item.exe|where the action is at!| [SourceDir]\installer\Program Files\Queue Item | [ProgramFilesFolder]\Queue Item\queue_item.exe|
|Media Library.lnk | send to short cut | [SourceDir]\installer\send to\Media Library.lnk | [SendTo]\Media Library.lnk |


### Registry Updates 


**TODO** Mostly about turning on admin shares in windows 10 


### Short cuts 

| Name | source | target |
|---|---|---|
| media_library_lnk | [SendTo]\Media Library.lnk | [ProgramFilesFolder]\Queue Item\queue_item.exe 'arg1 arg2'|

Shortcut are installed as resources associated  with 

### Components

| Component | Resource |
|---| ---|
|SendTo| send_to_lnk, queue_item.exe |





