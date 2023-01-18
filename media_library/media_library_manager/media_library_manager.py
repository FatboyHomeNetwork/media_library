import logging
import os 
import sys 

from enum import Enum    

#import Import_item.import_queue
from media_library.media_library.import_item import importer 

class mime_type(Enum):
    IMAGE = 1
    VIDEO = 2
    AUDIO = 3
    TEXT = 4
        
    NOT_SUPPORTED = 99

class media_library_manager:

    def __init__(self, library_path):
        
        self.library_path = library_path
        self.queue = Import_item.import_queue.import_queue(self.queue_file(library_path))
        
        logging.basicConfig(filename=self.log_file(library_path), format='%(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)


    def log_file(self):
        return os.path.join(self.library_path, 'system', 'media_library.log')

    def tmp_path(self):
        return os.path.join(self.library_path, 'system','temp')

    def queue_file(self):
        return os.path.join(self.library_path, 'system','import.queue')

    def media_path(self):
        return os.path.join(self.library_path, 'media')

    
    def queue(self, item_path):
        self.queue.add(item_path)
        logging.debug('Queued: %s.' % item_path)
    
    
    def import_next(self):
        
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
    