################################################################################################
#
#  library_directories
#
################################################################################################

import os

class library_directories:

    def __init__(self, path):
        
        self.__MEDIA_LIBRARY = path
        self.LIBRARY = os.path.join(self.__MEDIA_LIBRARY, 'system') # LIBRARY\system
        self.LOG_FILE_PATH = self.LIBRARY  # LIBRARY\system 
        self.WORKING = os.path.join(self.SYSTEM, 'tmp')  # LIBRARY\system\tmp
