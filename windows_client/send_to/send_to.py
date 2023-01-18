import sys
import os
import logging

import media_library_manager.media_library as ml

if __name__ == "__main__":
    
    if len(sys.argv) == 2: # send_to.py "<item_path>" 
                        
        item = sys.argv[1]
        mlp = print(os.getenv('MEDIA_LIBRARY'))
        print ('there?','MEDIA_LIBRARY' in os.environ)
        
        
        
        logging.basicConfig(filename=__file__+'.error.log', format='%(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)
        
        if os.path.exists(mlp):
            lib_mgn = ml(mlp)
            lib_mgn.queue(item)
        
        else:    
            logging.critical('Send To: media library not found. %s.' % mlp)
        
        
