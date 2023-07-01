# Queue Item 

## Overview

This is the entry point for getting items into the media library. This script will take an item's unc path and add it to the media library import queue. Delegates all functionality to `media_library_manager.py`. 

Supports the user interactions

- Send to ...
- Torrent Complete

Send To adds a *Send To Media Library* option in file explore's item context menu. The Send To uses the `queue_item.py` script to add the selected item to the import queue. Send To can be added to network clients and network server machines. 

Torrent Complete is an event thrown by the torrent client once a torrent has been downloaded. Torrent Complete event uses the `queue_item.py` script to add the completed  torrent item to the import queue. Torrent Complete only needs to be configured for the server running the torrent client.

## Installation 

### 1 Server & Client 

Install `queue_item.py` in program files. 

sets `MEDIA_LIBRARY` environmental variable to point to media library. At some point this will be wrapped in a windows native installer that would ask the user to select the location of the media library.Creating a slick user experience.  

### 2 Client 

Depends on `queue_item.py` & `MEDIA_LIBRARY`

Sent To add short cut to users sent to folder 

### 3 Server

Depends on `queue_item.py` & `MEDIA_LIBRARY`

Torrent Complete. Exact config is torrent client specific 



