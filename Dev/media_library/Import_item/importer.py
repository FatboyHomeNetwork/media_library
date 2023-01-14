################################################################################################
#
#  importer
#
################################################################################################

import sys
import os
import shutil
import distutils.dir_util

import media_library as ml


from  media_library.Import_item import import_queue as queue
from  media_library.media_converter import path_preparator as preparator
from  media_library.media_converter import converter as media_converter


class importer:
    
    def __init__(self, library_path):
        
        self.tmp_path = ml.tmp_path(library_path)
        self.lp = library_path
    
    def __copy_item(self, item_path, tmp_path):
        
        if os.path.isdir(item_path):
            distutils.dir_util.copy_tree(item_path, tmp_path)
        else:
            shutil.copy2(item_path, tmp_path)
    
    def import_item (self, item_path):
                               
        item_name = os.path.basename(item_path)
        tmp_path = os.path.join(self.tmp_path, item_name)
        
        self.__copy_item(item_path, tmp_path)
        
        tmp_path = preparator.prepare(tmp_path)
        media_converter.convert(tmp_path)
        
        dest_dir  = ml.media_path(self.lp)
        item_name = os.path.basename(tmp_path)
        dest_path = os.path.join(dest_dir, item_name)
        
        distutils.dir_util.copy_tree(tmp_path, dest_path)
        distutils.dir_util.remove_tree(tmp_path)
