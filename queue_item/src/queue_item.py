import sys
import os

from media_library.media_library_manager import media_library_manager 

if __name__ == "__main__":
    
    # queue_item.py <item_path>
    # queue_item.py <item_folder> <item_name>
    
    if len(sys.argv) >= 2: 
        
        if len(sys.argv)== 2:
            item = sys.argv[1]
        else:
            item = os.path.join(sys.argv[1:])
        
        media_library_path = str(os.getenv('MEDIA_LIBRARY'))
        
        if os.path.exists(media_library_path):
            media_library_manager(media_library_path).queue_media(item)
        else:    
            raise Exception('queue_item.py. Media library not found. MEDIA_LIBRARY=%s.' % media_library_path)
    else:
        raise Exception('queue_item.py. Missing item path.')