import os 
import shutil
import logging

from import_queue import queue as import_queue 

#from converters import path_converter as media_path  ## server context 
from converters import path_converter__DEV as media_path    ## development context 
#from converters import media_converter as media_converter
from converters import media_converter__DEV as media_converter ## skip the convert, and control media type 
from converters import folder_converter

import media_normaliser 
#from media_normaliser import normaliser
from media_normaliser import normaliser_DEV as normaliser

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
    
    ################################################################################################
    # 
    # queue -- add a media item to the import queue transaction method
        
    def queue(self, item_path):
        
        mp = media_path(item_path) 
        
        if not mp.is_unc_path():
            item = media_path(item_path).adminshare()
            self.__import_queue.add(item)
            logging.debug('Queued: %s.' % item)
        else:
            logging.error('UNC Path: %s.' % item_path)
            
    def __copyitem(self, src, dst):
        
        shutil.rmtree(dst, ignore_errors=True) 
        
        try:
            if os.path.isfile(src):
                os.mkdir(dst)
                shutil.copy(src, dst)
                return True
            else:
                shutil.copytree(src, dst) 
                return True
            
        except OSError: 
            return False
        
    def __normalise_directory(self, root, model, norm_model):
        
        # rename in the tmp directory to match normalised directory 
        for o, n in zip(model , norm_model):
            n_path = os.path.join(root, n)
            o_path = os.path.join(root, o)
            os.rename(o_path, n_path)

################################################################################################
# 
# import item -- import into media library transaction method
            
    def import_item(self):
    
        src = self.__import_queue.next()
        
        # can src be accessed? 
        if not os.path.exists(src):
            logging.error('Not found: %s.' % src)
            # add to end of queue, goto 
            return 
        
        # Copy src to working location 
        media_name = os.path.split(src)[1]
        tmp = os.path.join(self.PATHS.WORKING, media_name)
        
        if not self.__copyitem(src, tmp):
            logging.error('Copy: %s.' % src)
            shutil.rmtree(tmp, ignore_errors=True)
            # add to end of queue, goto 
            return 
            
        # Folder Conversion
        fc = folder_converter(tmp)
        tmp = fc.convert() # converter will modify the directory 
        
        # Media Conversion 
        mc = media_converter(tmp)
        media_type = mc.convert() 
        
        if media_type == None or media_type == mc.TYPES.NOT_SUPPORTED:
            logging.error('Not supported: %s.' % src)
            self.__import_queue.remove(src)
            shutil.rmtree(tmp, ignore_errors=True) 
            return 
        
        if media_type == mc.TYPES.AUDIO:
            logging.info('Audio: %s.' % tmp)
            ## TODO copy tmp to iTurn auto import folder
            shutil.rmtree(tmp, ignore_errors=True) 
            self.__import_queue.remove(src)
            return  
        
        # normalise 
        model = media_normaliser.create_path_model(self.PATHS.WORKING, media_name)
        norm_model = normaliser(model).normalise()
        self.__normalise_directory(self.PATHS.WORKING, model, norm_model) 
        
        # copy from working dir into media library
        media_name_norm = os.path.split(os.path.split(os.path.split(norm_model[0])[0])[0])[1] # a bit shit, but needs to be OS safe 
        normalised_tmp = os.path.join(self.PATHS.WORKING, media_name_norm)
        self.__copyitem(normalised_tmp, os.path.join(self.PATHS.MEDIA, media_name_norm))
        
        # clean out tmp & queue 
        shutil.rmtree(normalised_tmp, ignore_errors=True)
        self.__import_queue.remove(src)
        
        logging.debug('Imported: %s.' % src)
            