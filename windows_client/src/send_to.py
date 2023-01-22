import sys
import os

from media_library.media_library_manager import media_library_manager 

if __name__ == "__main__":
    
    if len(sys.argv) == 2: # send_to.py "<item_path>" 
                        
        item = sys.argv[1] 
        media_library_path = str(os.getenv('MEDIA_LIBRARY'))
        
        if os.path.exists(media_library_path):
            media_library_manager(media_library_path).queue_media(item)
        else:    
            raise Exception('Media library not found. MEDIA_LIBRARY=%s.' % media_library_path)
        