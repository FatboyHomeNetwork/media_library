import sys
import os
import logging

import media_library as ml
#from media_library.media_library_manager import media_library_manage as mgn

if __name__ == "__main__":
    
    if len(sys.argv) == 3: # send_to_media_library.py.py "<media_library_path>" "<item_path>"
        
        mlp = sys.argv[1]
        item = sys.argv[2]
        
        logging.basicConfig(filename=ml.log_file(mlp), format='%(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)
        
        if os.path.exists(mlp):
            mgn = mgn(mlp)
            mgn.queue(item)
        
        else:    
            logging.critical('Send To: media library not found. %s.' % mlp)
        
        
