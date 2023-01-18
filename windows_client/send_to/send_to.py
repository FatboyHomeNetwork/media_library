import sys
import os
import logging

import media_library.media_library_manager as mlm  

if __name__ == "__main__":
    
    if len(sys.argv) == 2: # send_to.py "<item_path>" 
                        
        item = sys.argv[1]
        media_library_path = str(os.getenv('MEDIA_LIBRARY'))
        
        logging.basicConfig(filename=__file__+'.error.log', format='%(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)
        
        if os.path.exists(media_library_path):
            lib_mgn = mlm(media_library_path)
            lib_mgn.queue(item)
        
        else:    
            logging.critical('Send To: media library not found. MEDIA_LIBRARY=%s.' % media_library_path)
        
        
