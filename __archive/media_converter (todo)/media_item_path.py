################################################################################################
#
#  media item path
#
################################################################################################
    
import os
import win32wnet
import unicodedata
import shutil
import stat 
import platform



class media_item_path(object):
    
    def __init__(self, path):
        
        self.path = path
    
    #
    # Identify and normalise network paths 
    #
    
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
     
     
     
     
    
       

    #
    # Prepare path
    #
        
    def __open_permissions(self):
        
        if os.path.isdir(self.path):
            
            OPEN = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH 
            
            for subdir, dirs, files in os.walk(self.path):
                os.chmod(subdir, OPEN)
                
                for file in files:
                    os.chmod(os.path.join(subdir, file), OPEN)
        
        elif os.path.isfile(self.path):
            
            os.chmod(self.path, OPEN)


    def __strip_unicode(self):
            
        if len(self.path) != len(self.path.encode()):
            clean_path = unicodedata.normalize('NFKD', self.path).encode('ascii', 'ignore').decode('ascii').strip()
            
            os.rename(self.path, clean_path)
            
            self.path =  clean_path

    
    def __ensure_path_len(self):
        
        MAX_LEN = 254
        
        if len(self.path) > MAX_LEN:
            filename, file_extension = os.path.splitext(self.path)
            filename = filename[0:len(self.path) - (len(self.path) - MAX_LEN)]
            new_path = filename + file_extension
            
            os.rename(self.path, new_path)
            
            self.path = new_path
        

    def __ensure_is_directory(self):
        
        if os.path.isfile(self.path):
            
            tmp = self.path + '-tmp'
            os.rename(self.path, tmp)
            
            os.mkdir(self.path)
            shutil.copy2(tmp, self.path)
            os.remove(tmp)
            
            tmp_copy = os.path.join(self.path, os.path.basename(tmp))
            os.rename(tmp_copy, tmp_copy[:len(tmp_copy)-4])

    
    def prepare_path(self):
        
        if os.path.exists(self.path):
        
            self.__open_permissions()
            self.__strip_unicode()
            self.__ensure_path_len()
            self.__ensure_is_directory()

       
    