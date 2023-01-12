################################################################################################
#
#  media_library_manager - proxy pattern 
#
################################################################################################

import logging
import os 

from import_queue import import_queue
from  unc_path import  unc_path 

class media_library_manager:

    def __init__(self, library_path, working_path):
        
        self.library_path = library_path
        self.working_path = working_path
        self.queue = import_queue(self.library_path)
        self.log_file_path = os.path.join(self.library_path, 'media_library.log')
        
        logging.basicConfig(filename=self.log_file_path, format='%(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)

    
    def queue(self, path):
        
        item_path = unc_path(path).as_unc()
        self.queue.add(item_path)
        logging.debug('Queued: %s.' % item_path)

    
    def import_next(self):
    
        item = self.queue.next()
        logging.debug('Import: %s.' % item)
        
        # copy to working area
        
        # clean path 
        
        # convert media 
        
        # normalise the path 
        
        # copy to the library         
        
        # delete from tmp area
        
        
        item = self.queue.remove(item)    
        
        return item
    
        
        
    