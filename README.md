#Media Library

Part of the Fatboy Home Network. Provides a network wide library of media -- movies, tv shows, music, home moves, & pictures -- to network clients via a variety of standard network services.


##Modules

+media_library_manager
+queue_media_item
+media_converter
+media_name_normalise
+on_torrent_complete
+send_to
+scheduled_import



##Media Library Folders

MEDIA_LIBRARY  -- root media library directory, everything is a sub dir of this. This value can be set per install.  

MEDIA_LIBRARY\system -- Hidden, top level system directory. 
MEDIA_LIBRARY\system\media.queue -- media queue file
MEDIA_LIBRARY\system\media_library.log -- log file, records copies & convert activity 
MEDIA_LIBRARY\system\tmp -- location used to hold media being copied and processed 

MEDIA_LIBRARY\Media -- destination for all video files. User access point. 
MEDIA_LIBRARY\Pictures -- destination for all image files. User access point.
MEDIA_LIBRARY\Videos -- destination for sub set of video files. User access point.
MEDIA_LIBRARY\Music --  destination for all music. User access point. Shortcut to iTunes managed directory space 
