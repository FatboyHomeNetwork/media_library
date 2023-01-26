# queue_item installer 

## Overview 

The queue_item installer does the following. Elevated permission are needed to run all these steps

1. set the `MEDIA_LIBRARY` environment value based on users selection 
2. copy `queue_item.exe`  to  program files
2. create a send_to short cut in the windows explorer context menu

## Build Process 

1. use `cz_Freeze` to create an exe with all the libraries. Since the install  comes with all the libraries it needs it take any any dependencies on the host machine to have particular versions of libraries, etc. Taking away what was once called DLL hell. 

    This is a is the how to build build. https://cx-freeze.readthedocs.io/en/latest/script.html#script

## Installer Process

All steps, except the last will be done by the windows installer. The last step, torrent complete,  will probably need to be manual and different for different torrent clients.  

1. **Enable Admin Shares** in some later version of windows admin share access to non domain services bas turned off. some  registry  are needed to turn it all back on. 
2. **create media_library user**. this account will be used to perform admin share access in cases where the item path is local on the users machine.
1. **Set MEDIA_LIBRARY path**.  This will require a user to select the media_library folder. Should it look for a specific file? Make it easier to know if you are in the correct directory or not. 
1. **queue_item Installer**. Installs the queue_item.exe created by the build process. Install steps: 
   1. Create Destination Dir  `%PROGRAMFILES%\Fatboy Media Library`. this will need to run will elevated permissions. 
   2. Copy bin (create in build process) to dir created in a. will also need elevated permissions

3. **send to ...** adds a send to Media Library context menu option in explorer. The short cut needs to be called `Media Library`. That will then e the name that is shown in the send to menu 
   1. copy / create a  short cut to` %APPDATA%\Microsoft\Windows\SendTo`. The destination for this will be `%PROGRAMFILES%\Fatboy Media Library\queue_item.exe`



4. **Torrent Complete** This is called bya torrent client once torrent is ready to be imported into the media library. configure torrent client to execute queue_item.exe once a torrent has been down loaded. queue_item.exe support multiple formats formats:

   1. `queue_item.exe item_path`
   2. `queue_item.exe item_file item_name ` 
   3. `queue_item.exe root item_dir item_name`.  Path items are joined using os.path.join()



