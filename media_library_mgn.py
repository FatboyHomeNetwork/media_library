import os 
import shutil
import logging

from import_queue import queue as import_queue 
import converters
#from converters import path_converter__PROD as media_path  ## server context 
from converters import path_converter__DEV as media_path    ## development context 
from converters import media_converter
from converters import folder_converter
from media_name_normaliser import path_normaliser

LOG_FILE_NAME = 'media_library.log'

################################################################################################
#
#  library_directories -- builds out the library directory structure from the root dir
#
################################################################################################

class library_directories:

    def __init__(self, root):
        
        self.__ROOT = root
        
        # system area
        self.LIBRARY = os.path.join(self.__ROOT, 'system') # ROOT\system
        self.LOG_FILE = (self.__ROOT)  # ROOT
        self.WORKING = os.path.join(self.LIBRARY, 'tmp')  # ROOT\system\tmp
        
        # user entry point areas
        self.MEDIA = os.path.join(self.__ROOT, 'Media') # ROOT\Media

################################################################################################
#
#  media_library_mgn 
#
################################################################################################

class media_library_mgn:
    
    PATHS = None
    __import_queue = None
    
    def __init__(self, library_root):
        
        self.PATHS = library_directories(library_root)
        self.__import_queue = import_queue(self.PATHS.LIBRARY)
        logging.basicConfig(filename=os.path.join(self.PATHS.LOG_FILE, LOG_FILE_NAME), format='%(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)
    
    def queue_next(self, item_path):
        
        mp = media_path(item_path) # aka path_converter
        
        if not mp.is_unc_path():
            item = media_path(item_path).adminshare()
            self.__import_queue.add(item)
            logging.debug('Queued: %s.' % item)
        else:
            logging.error('UNC Path: %s.' % item_path)
        
    
    def __copyitem(self, src, dst):
        # use dirs_exist_ok=True to replace any previous attempt
        
        try:
            shutil.copytree(src, dst, dirs_exist_ok=True) 
            return True
        except OSError: 
            shutil.rmtree(dst, ignore_errors=True) 
            os.mkdir(dst)
            try:
                shutil.copy(src, dst)
                return True
            except:
                return False
        
    def import_next(self):
    
        src = self.__import_queue.next()
        
        # can the src be accessed? 
        if not os.path.exists(src):
            logging.error('Media not found: %s.' % src)
            # add to end of queue, goto 
            return 
        
        # Copy to working location 
        tmp = os.path.join(self.PATHS.WORKING, os.path.split(src)[1])
        successful = self.__copyitem(src, tmp)
        
        if not successful:
            logging.error('Copy interrupted: %s.' % src)
            # add to end of queue, goto 
            return 
            
        # Folder Conversion
        fc = folder_converter(tmp)
        tmp = fc.convert() # converter will modify the directory 
        
        # Media Conversion 
        mc = media_converter(tmp)
        media_type = mc.convert() 
        
        if media_type == None or media_type == mc.TYPES.NOT_SUPPORTED:
            logging.error('Media not supported: %s.' % src)
            self.__import_queue.remove(src)
            shutil.rmtree(tmp, ignore_errors=True) 
            return 
        
        if media_type == mc.TYPES.AUDIO:
            logging.debug('Audio imported: %s.' % src)
            ## TODO copy to iTurn auto import folder
            shutil.rmtree(tmp, ignore_errors=True) 
            self.__import_queue.remove(src)
            return  
        
        # Path Normalization
##    add    create_path_model() to create model from path.]
        pn = path_normaliser(tmp)
        
        normalised_path = pn.normalise() 
        
        # copy to library, remove from working folder and import queue
        self.__copyitem(tmp, os.path.join(self.PATHS.MEDIA, normalised_path))
        shutil.rmtree(tmp, ignore_errors=True)
        self.__import_queue.remove(src)
        
        logging.debug('Media imported: %s.' % src)
    