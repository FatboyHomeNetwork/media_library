################################################################################################
#
#  media_preparator
#
################################################################################################
    
import os
import unicodedata
import shutil
import stat 

class media_preparator(object):
    
    #def __init__(self):
    #
    # Prepare path
    #
        
    def __open_permissions(self, path):
        
        if os.path.isdir(path):
            
            OPEN = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH 
            
            for subdir, dirs, files in os.walk(path):
                os.chmod(subdir, OPEN)
                
                for file in files:
                    os.chmod(os.path.join(subdir, file), OPEN)
        
        elif os.path.isfile(path):
            
            os.chmod(path, OPEN)


    def __strip_unicode(self, path):
            
        if len(path) != len(path.encode()):
            clean_path = unicodedata.normalize('NFKD', path).encode('ascii', 'ignore').decode('ascii').strip()
            
            os.rename(path, clean_path)
            
            path =  clean_path

    
    def __ensure_path_len(self, path):
        
        MAX_LEN = 254
        
        if len(path) > MAX_LEN:
            filename, file_extension = os.path.splitext(path)
            filename = filename[0:len(path) - (len(path) - MAX_LEN)]
            new_path = filename + file_extension
            
            os.rename(path, new_path)
            
            path = new_path
        

    def __ensure_is_directory(self, path):
        
        if os.path.isfile(path):
            
            tmp = path + '-tmp'
            os.rename(path, tmp)
            
            os.mkdir(path)
            shutil.copy2(tmp, path)
            os.remove(tmp)
            
            tmp_copy = os.path.join(path, os.path.basename(tmp))
            os.rename(tmp_copy, tmp_copy[:len(tmp_copy)-4])

    
    def prepare(self, path):
        
        if os.path.exists(path):
        
            self.__open_permissions(path)
            self.__strip_unicode(path)
            self.__ensure_path_len(path)
            self.__ensure_is_directory(path)
        
        return path        