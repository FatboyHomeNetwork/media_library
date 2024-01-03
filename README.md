# Media Library

Part of the Fatboy Home Network. Provides a network wide library of media -- movies, tv shows, music, home moves, & pictures -- to network clients via a variety of standard network services.

## Modules

### Functional

- media_library_manager -- coordinates the queue, converter and normaliser to process, convert and adds items to the queue.     
- import_queue -- Record a queue of items to be imported, adds & removes items, has a next function 
- converters -- *media_converter* -- converts the media formats to support applet TV & windows, provides some utility functions to support formats checks, etc.  *Path_converter* -- items to paths and formats, converts to UNC paths and to admin share paths
- media_name_normaliser -- normalizes the items path and file name names to std media library formats, the std formats support client to down load correct item meta data (TV and Movie items only -- audio is managed by iTunes)

### UI 

- media_library -- command line interface for  media_library_manager & client library functions - add item, import next queued item.

**Wrappers over `media_library`**

- on_torrent_complete -- called by torrent server to add newly imported item to import_queue
- send_to -- called by user to add select item to import_queue
- scheduled_import -- called by task scheduler to import the next queued item

## Media Library Folders 

- **MEDIA_LIBRARY**  -- root media library directory, everything is a sub dir of this. This value is set as a environmental variable and can be configured per install.

### System Locations -- set to hidden 

- **MEDIA_LIBRARY\system** -- Top level system directory.
- **MEDIA_LIBRARY\system\media.queue** -- media queue file
- **MEDIA_LIBRARY\system\media_library.log** -- log file, records copies & convert activity 
- **MEDIA_LIBRARY\system\tmp** -- location used to hold media being copied and processed 

### User Entry Points -- visible as shared folders on server / library   

- **MEDIA_LIBRARY\Media** -- destination for all video files. User access point. 
- **MEDIA_LIBRARY\Pictures** -- destination for all image files. User access point.
- **MEDIA_LIBRARY\Videos** -- destination for sub set of video files. User access point.
- **MEDIA_LIBRARY\Music** --  destination for all music. User access point. Shortcut to iTunes managed directory space. 
