import logging
import os 
import sys
import win32wnet
import platform 
import shutil

from shutil import copy2 as copy_file
from  distutils.dir_util import copy_tree, remove_tree
from enum import Enum    

from media_library.media_queue import media_queue 
from media_library.media_converter.path_preparator import path_preparator 
from media_library.media_converter.media_converter import media_converter
from media_library.media_converter.decoder import decoder

#
# Media library files and folders
#

def log_file(media_library):
    return os.path.join(media_library, 'system', 'media_library.log')

def media_queue_file(media_library):
    return os.path.join(media_library, 'system','media.queue')

def temp_path(media_library):
    return os.path.join(media_library, 'system','temp')

def media_path(media_library):
    return os.path.join(media_library, 'media')


class mime_type(Enum):
    IMAGE = 1
    VIDEO = 2
    AUDIO = 3
    TEXT = 4
        
    NOT_SUPPORTED = 99

class media_path(object):
    
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
        except: # is local, so access via admin share
            return self.__as_admin_share()

class media_library_manager:

    def __init__(self, library_path):
        self.library_path = library_path
        self.queue = media_queue.media_queue(media_queue_file(self.library_path))
        
        logging.basicConfig(filename=log_file(self.library_path), format='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%Y %H:%M:%S', encoding='utf-8', level=logging.DEBUG)


    def queue_media(self, item):
        
        try:
            path = media_path(item)
            self.queue.add(path.as_unc())
            logging.info('Queued: %s.' % path.as_unc())
        
        except:
            logging.exception('Item: %s.' % item)
            logging.exception(str(sys.exc_info()))    
  
 
    #
    # Media library transactions 
    #
    
    def import_next_media(self):
        item = None
        
        try:
            item = self.queue.next()
            logging.info('Import started: %s.' % item)

            if os.path.exists(item):
                
                item_name, ext = os.path.splitext(os.path.basename(item))
                item_temp_path = os.path.join(temp_path(self.library_path), item_name)
                
                if os.path.isdir(item):
                    copy_tree(item, item_temp_path)
                else:
                    os.makedirs(os.path.dirname(item_temp_path), exist_ok=True)
                    copy_file(item, item_temp_path)
                
                item_temp_path = path_preparator.prepare(item_temp_path)
                media_converter.convert(item_temp_path)
                
                media_library_path = os.path.join(media_path(self.library_path), item_name)
                
                copy_tree(item_temp_path, media_library_path)
                remove_tree(item_temp_path)
                
                self.queue.remove(item)    
                
                logging.info('Imported completed: %s.' % item)
            else:
                logging.warning('Import path not found: %s.' % item)
        
        except:
            logging.exception('Item: %s.' % item)
            logging.exception(str(sys.exc_info()))    
            return ''
            
        return item
    
    def client_remove_media(self, item):
        
        logging.info('Removed from client: %s.' % item)
