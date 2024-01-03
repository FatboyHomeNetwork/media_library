################################################################################################
#
#  media_library_mgn -- client entry point into media library. 
#
################################################################################################

import os
import sys
from media_library_mgn import media_library_mgn

ENV_VAR = 'MEDIA_LIBRARY'

if __name__ == "__main__":
    
    media_library_path = str(os.getenv(ENV_VAR))
    
    if not os.path.exists(media_library_path):
        raise Exception('Media library not found.  %s = %s.' %  (ENV_VAR, media_library_path))

    library = media_library_mgn(media_library_path) 

    if len(sys.argv) == 2 and sys.argv[1].lower() == r'/i': # Import next queued item 
        library.import_next()  
    
    elif len(sys.argv) == 3 and sys.argv[1].lower() == r'/q': # queued item 
        library.queue(sys.argv[2])
    
    else: 
        raise Exception('Incorrect arguments.')

    
    