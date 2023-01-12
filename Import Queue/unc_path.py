################################################################################################
#
#  unc path
#
################################################################################################
   

import win32wnet
import platform

class unc_path(object):
    
    def __init__(self, path):
        
        self.path = path
    
    
    def __is_unc_path(self):
        # see: file path formats on windows systems.pdf 
        
        if len(self.path) > 3 and self.path[0:2] == '\\\\' and self.path[2:3] != '?' and self.path[2:3] != '.':
            return True 
        else:
            return False


    def __as_admin_share(self):
         # C:\Dir\subDir\etc. -> \\<machine name>\C$\Dir\subDir\etc. 
         
        return  '\\\\' +  platform.node() + '\\' + self.path.replace(':','$',1)
    
    
    def as_unc(self):
        
        if self.__is_unc_path(): 
            return self.path 
        
        try: # is a drive letter than can mapp to a unc share
            return win32wnet.WNetGetUniversalName(self.path, 1)  
            
        except: # is not shared; access via admin share
            return self.__as_admin_share()
        
