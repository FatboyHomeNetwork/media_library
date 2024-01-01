################################################################################################
#
#  media path -- wraps some simple path conversion to path
#
################################################################################################

import os
import win32wnet
import platform

class media_path(object):
    
    path = ''
    ospath = os.path()
    
    def __init__(self, path):
        self.path = path
        self.ospath = os.path(self.path) # use media_path.path to get all the path goodness 
        
    def __is_unc_path(self):
        # see: file path formats on windows systems.pdf 
        
        if len(self.path) > 3 and self.path[0:2] == '\\\\' and self.path[2:3] != '?' and self.path[2:3] != '.':
            return True 
        else:
            return False

    def adminshare(self):
        # C:\Dir\subDir\etc. -> \\<machine name>\C$\Dir\subDir\etc. 
        
        if  not self.__is_unc_path(): # eg, is C:\Dir\subDir\etc
            return  '\\\\' +  platform.node() + '\\' + self.path.replace(':','$',1)
        else: 
            raise Exception('Cannot convert UNC to admin share format.')
    
    def unc(self):
        
        if self.__is_unc_path(): 
            return self.path
        else: # is a drive letter than can map to a unc share, will throw exception if it can't be converted
            return win32wnet.WNetGetUniversalName(self.path, 1)  
        
