import sys
import os

from  media_library.media_library_manager import media_library_manager as library_manager

if __name__ == "__main__":
    
    #if len(sys.argv) == 2: # send_to.py "<item_path>" 
                        
        #item = sys.argv[1] 
        item = '\\\\SERVER\\Users\\Paul\\Documents\\GitHub\\media_library\\test\\_test_data\\five\media.mkv'
        media_library_path = str(os.getenv('MEDIA_LIBRARY'))
        
        if os.path.exists(media_library_path):
            library_manager(media_library_path).queue_media(item)
        else:    
            raise Exception('Media library not found. MEDIA_LIBRARY=%s.' % media_library_path)