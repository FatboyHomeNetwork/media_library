import os
import win32wnet
import platform
import unicodedata
import shutil
import stat 


################################################################################################
#
#  path_converter
#
################################################################################################

class path_converter(object):
    
    __path = ''
    
    def __init__(self, path):
        self.__path = path
        
    def __is_unc_path(self):
        # see: file path formats on windows systems.pdf 
        
        if len(self.__path) > 3 and self.__path[0:2] == '\\\\' and self.__path[2:3] != '?' and self.__path[2:3] != '.':
            return True 
        else:
            return False

    def adminshare(self):
        # C:\Dir\subDir\etc. -> \\<machine name>\C$\Dir\subDir\etc. 
        
        if  not self.__is_unc_path(): # eg, is C:\Dir\subDir\etc
            return  '\\\\' +  platform.node() + '\\' + self.__path.replace(':','$',1)
        else: 
            raise Exception('Cannot convert UNC to admin share format.')
    
    def unc(self):
        
        if self.__is_unc_path(): 
            return self.__path
        else: # is a drive letter than can map to a unc share, will throw exception if it can't be converted
            return win32wnet.WNetGetUniversalName(self.__path, 1)  
        
    def __open_permissions(self, path):
        
        if os.path.isdir(path):
            
            OPEN = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH 
            
            for subdir, dirs, files in os.walk(path):
                os.chmod(subdir, OPEN)
                
                for file in files:
                    os.chmod(os.path.join(subdir, file), OPEN)
        
        elif os.path.isfile(path):
            
            os.chmod(path, OPEN)
            
        return path

    def __strip_unicode(self, path):
            
        if len(path) != len(path.encode()):
            clean_path = unicodedata.normalize('NFKD', path).encode('ascii', 'ignore').decode('ascii').strip()
            
            os.rename(path, clean_path)
            
            return clean_path

    
    def __ensure_path_len(self, path):
        
        MAX_LEN = 254
        
        if len(path) > MAX_LEN:
            filename, file_extension = os.path.splitext(path)
            filename = filename[0:len(path) - (len(path) - MAX_LEN)]
            new_path = filename + file_extension
            
            os.rename(path, new_path)
            
            return  new_path
        

    def __ensure_is_directory(self, path):
        
        if os.path.isfile(path):
            
            tmp = path + '-tmp'
            os.rename(path, tmp)
            
            os.mkdir(path)
            shutil.copy2(tmp, path)
            os.remove(tmp)
            
            tmp_copy = os.path.join(path, os.path.basename(tmp))
            os.rename(tmp_copy, tmp_copy[:len(tmp_copy)-4])
    
    
    def prepare(self):
        
        if os.path.exists(self.__path):
        
            ## TODO these need to be applied to a media collection, not just a single path 
            self.__path = self.__strip_unicode(self.__path)
            self.__path = self.__ensure_path_len(self.__path)
            ## TODO
                        
            self.__path = self.__open_permissions(self.__path)
            self.__path = self.__ensure_is_directory(self.__path)
    
    
    def path(self):
        return self.__path
    