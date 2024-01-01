################################################################################################
#
#  media_library_mgn_TESTER
#
################################################################################################\

import os

from media_library_mgn import media_library_mgn
from media_path_normaliser.library_directories import library_directories as library_directories

if __name__ == "__main__":
    
    mgn = media_library_mgn(str(os.getenv('MEDIA_LIBRARY')))
    
    ## add new items to queue 
    mgn.queue("path one")
    mgn.queue("path two")
    mgn.queue("path three")
    
    
    
    
                                        