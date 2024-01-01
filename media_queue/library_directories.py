################################################################################################
#
#  library_directories
#
################################################################################################

import os

class library_directories:

    def __init__(self, path):
        
        self.__MEDIA_LIBRARY = path
        
        self.SYSTEM = os.path.join(self.__MEDIA_LIBRARY, 'system') # LIBRARY\system
        self.WORKING = os.path.join(self.SYSTEM, 'tmp')  # LIBRARY\system\tmp
