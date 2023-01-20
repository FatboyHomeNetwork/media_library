import logging
import os 
import sys
import win32wnet
import platform 


from enum import Enum    

import media_library.media_queue.media_queue as queue
#import media_library.importer.importer as importer

class mime_type(Enum):
    IMAGE = 1
    VIDEO = 2
    AUDIO = 3
    TEXT = 4
        
    NOT_SUPPORTED = 99

class unc_path(object):
    
    def __init__(self, path):
        
        self.path = path
    
    def __is_unc_path(self):
        # see: file_path_formats_on_windows_systems.pdf
        
        if len(self.path) > 3 and self.path[0:2] == '\\\\' and self.path[2:3] != '?' and self.path[2:3] != '.':
            return True 
        else:
            return False


    def __as_admin_share(self):
         # C:\Dir\subDir\etc. -> \\<machine name>\C$\Dir\subDir\etc. 
         
        return  '\\\\' +  platform.node() + '\\' + self.path.replace(':','$',1)
    
    
    def as_unc(self):
        
        if self.__is_unc_path(): 
            return self.path # come as you are 
        
        try: # is a drive letter that has been mapped to a unc share?
            return win32wnet.WNetGetUniversalName(self.path, 1)  # yes
        
        # no, so ...
        except: # we'll access via admin share
            return self.__as_admin_share()


class media_library_manager:

    def __init__(self, library_path):
        
        self.library_path = library_path
        self.queue = queue(self.media_queue_file(library_path))
        
        logging.basicConfig(filename=self.log_file(library_path), format='%(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)

    #
    # Media Library Paths 
    #
    
    def log_file(self):
        return os.path.join(self.library_path, 'system', 'media_library.log')

    def temp_path(self):
        return os.path.join(self.library_path, 'system','temp')

    def media_queue_file(self):
        return os.path.join(self.library_path, 'system','import.queue')

    def media_path(self):
        return os.path.join(self.library_path, 'media')

    #
    # Media Library Transactions 
    #
    
    def queue_media(self, item_path):
        as_unc_path = unc_path(item_path)
        self.queue.add(as_unc_path.as_unc())
        
        logging.info('Queued: %s.' % as_unc_path)
    
    def import_next_media(self):
        
        try:
            item = self.queue.next()
            logging.info('Start Import: %s.' % item)

            if os.path.exists(item):
                #importer.import_item(item)
                self.queue.remove(item)    
                logging.info('Complete Import: %s.' % item)
            else:
                logging.warning('Path not found: %s.' % item)
        
        except:
            logging.exception('Exception: %s.' % item)
            logging.exception(str(sys.exc_info()))    
            return ''
            
        return item
    
    def remove_media(self, item):
        logging.info('Removed from client: %s.' % item)
