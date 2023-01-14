################################################################################################
#
#  media_library_manager - facade pattern 
#
################################################################################################

import logging
import os 
import sys 

import media_library as ml

from media_library.Import_item import queue
from media_library.Import_item import importer 


class media_library_manager:

    def __init__(self, library_path):
        
        self.queue = queue(ml.queue_file(library_path))
        logging.basicConfig(filename=ml.log_file(library_path), format='%(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)

    
    def queue(self, item_path):
        self.queue.add(item_path)
        logging.debug('Queued: %s.' % item_path)
    
    
    def next(self):
        
        try:
            item = self.queue.next()
            logging.info('Start Import: %s.' % item)

            if os.path.exists(item):
                importer.import_item(item)
                self.queue.remove(item)    
                logging.info('Complete Import: %s.' % item)
            else:
                logging.warning('Path not found: %s.' % item)
        
        except:
            logging.exception('Exception: %s.' % item)
            logging.exception(str(sys.exc_info()))    
            return ''
            
        return item
    