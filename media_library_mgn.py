################################################################################################
#
#  media_library
#
################################################################################################

import logging
import os 

from media_queue.media_queue import queue as queue 
from media_path_normaliser.media_path import media_path
from media_path_normaliser.library_directories import library_directories

LOG_FILE_NAME = 'media_library.log'

class media_library_mgn:
    
    PATHS = None
        
    def __init__(self, path):
        
        PATHS = library_directories(path)
        self.queue = queue(PATHS.LIBRARY)
        logging.basicConfig(filename=os.path.join(self.LOG_FILE_PATH, LOG_FILE_NAME), format='%(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)
    
    def queue(self, path):
        
        item = media_path(path).adminshare()
        self.queue.add(item)
        logging.debug('Queued: %s.' % item)
    
    def import_next(self):
    
        item = self.queue.next()
        logging.debug('Import: %s.' % item)
        
        # Get next
        
        # copy to working area
        
        # clean path 
        
        # convert media 
        
        # normalise the path 
        
        # copy to the library         
        
        # delete from tmp area
        
        # remove form queue
        
        
        item = self.queue.remove(item)    
        
        return item
    
        
        
    