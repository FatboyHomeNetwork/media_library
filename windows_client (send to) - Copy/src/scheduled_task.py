import sys
import os

from media_library.media_library_manager import media_library_manager as library_manager

if __name__ == "__main__":
    
    media_library_path = str(os.getenv('MEDIA_LIBRARY'))
    
    if os.path.exists(media_library_path):
        library_manager(media_library_path).import_next_media()
    else:    
        raise Exception('Media library not found. MEDIA_LIBRARY=%s.' % media_library_path)