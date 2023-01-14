import sys
import os
import logging

import media_library as ml
from media_library.media_library_manager import media_library_manage as mgn

if __name__ == "__main__":
    
    if len(sys.argv) == 2: # import_task.py "<media_library_path>"
        
        mlp = sys.argv[1]
        logging.basicConfig(filename=ml.log_file(mlp), format='%(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)
        
        if os.path.exists(mlp):
            mgn = mgn(mlp)
            mgn.import_next()
        
        else:    
            logging.critical('Import task: media library not found. %s.' % mlp)
        
