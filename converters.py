import os
import win32wnet
import platform
import unicodedata
import shutil
import stat 
import magic
import ffmpy
import operator

FFMPEG_PATH = r'C:\Program Files\ffmpeg\bin\ffmpeg.exe'
MAX_PATH_LENGTH = 254

################################################################################################
#
#  path_converter__PROD
#
################################################################################################

class path_converter__PROD(object):
    
    __path = ''
    
    def __init__(self, path):
        self.__path = path
        
    def is_unc_path(self):
        # see: file path formats on windows systems.pdf 
        
        if len(self.__path) > 3 and self.__path[0:2] == '\\\\' and self.__path[2:3] != '?' and self.__path[2:3] != '.':
            return True 
        else:
            return False

    def adminshare(self):
        # C:\Dir\subDir\etc. -> \\<machine name>\C$\Dir\subDir\etc. 
        
        if  not self.is_unc_path(): # eg, is C:\Dir\subDir\etc 
            return  '\\\\' +  platform.node() + '\\' + self.__path.replace(':','$',1)
        else: 
            raise Exception('Cannot convert UNC to admin share format.')
    
    def unc(self):
        
        if self.is_unc_path(): 
            return self.__path
        else: # is a drive letter than can map to a unc share, will throw exception if it can't be converted
            return win32wnet.WNetGetUniversalName(self.__path, 1)  

################################################################################################
#
#  path_converter__DEV -- dev sub to used to replace server context with local context 
#
################################################################################################

class path_converter__DEV(object):
    
    __path = ''
    
    def __init__(self, path):
        self.__path = path
        
    def is_unc_path(self):
        return False 
        
    def adminshare(self):
        return self.__path
    
    def unc(self):
        return self.__path


################################################################################################
#
#  folder_converter
#
################################################################################################

class folder_converter(object):

    __path = ''
    
    def __init__(self, folder_path):
        self.__path = folder_path


    def __open_permissions(self):
        
        if os.path.isdir(self.__path):
            
            OPEN = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH 
            
            for subdir, dirs, files in os.walk(self.__path):
                os.chmod(subdir, OPEN)
                
                for file in files:
                    os.chmod(os.path.join(subdir, file), OPEN)
        
        elif os.path.isfile(self.__path):
            
            os.chmod(self.__path, OPEN)


    def __strip_unicode(self):
            
        if len(self.__path) != len(self.__path.encode()):
            clean_path = unicodedata.normalize('NFKD', self.__path).encode('ascii', 'ignore').decode('ascii').strip()
            
            os.rename(self.__path, clean_path)
            self.__path = clean_path

    
    def __ensure_path_len(self):
        
        if len(self.__path) > MAX_PATH_LENGTH:
            filename, file_extension = os.path.splitext(self.__path)
            filename = filename[0:len(self.__path) - (len(self.__path) - MAX_PATH_LENGTH)]
            new_path = filename + file_extension
            
            os.rename(self.__path, new_path)
            self.__path =   new_path
        

    def __ensure_is_directory(self):
        
        if os.path.isfile(self.__path):
            
            tmp = self.__path + '-tmp'
            os.rename(self.__path, tmp)
            
            os.mkdir(self.__path)
            shutil.copy2(tmp, self.__path)
            os.remove(tmp)
            
            tmp_copy = os.path.join(self.__path, os.path.basename(tmp))
            os.rename(tmp_copy, tmp_copy[:len(tmp_copy)-4])
    
    
    def convert(self):
        
        if os.path.exists(self.__path):

            self.__strip_unicode()
            self.__ensure_path_len()
            self.__open_permissions()
            self.__ensure_is_directory()
     
        return self.__path

################################################################################################
#
#  media_converter
#
################################################################################################

class mime_type(object):
    
    IMAGE = 1
    VIDEO = 2
    AUDIO = 3
    TEXT = 4
    APPLICATION = 5
    NOT_SUPPORTED = 99

class media_converter:

    def __init__(self, media_path):
        self.__media_path = media_path
        self.TYPES = mime_type()

    def __count_mime_type(self, mime_type_sizes, tag, value):
        
        if tag in mime_type_sizes: 
            mime_type_sizes[tag] = mime_type_sizes[tag] + value
        else:
            mime_type_sizes[tag] = value

        return mime_type_sizes
    
    
    def __highest_mime_type(self, mime_type_sizes):
                
        mime_type_sizes_sorted = sorted(mime_type_sizes.items(), key=operator.itemgetter(1))

        if len(mime_type_sizes_sorted) > 0:
            return mime_type_sizes_sorted[0][0]
        else:
            return None
  
    
    def __set_destination_ext(self, mime_type, src):

        if mime_type == self.TYPES.IMAGE: 
            return os.path.splitext(src)[0] + '.jpg'
        elif mime_type == self.TYPES.VIDEO:
            return os.path.splitext(src)[0] + '.mp4'
        elif mime_type == self.TYPES.AUDIO:
            return os.path.splitext(src)[0] + '.mp3'
        else:
            return src
    
    def __get_mime_type(self, file):
        
        TYPE = 0
        SUBTYPE = 1

        item_path = os.path.join(self.__media_path, file)
        mime_type = magic.from_file(item_path, mime=True).split('/')
        
        if mime_type[TYPE] == 'image': 
            return self.TYPES.IMAGE
        
        elif mime_type[TYPE] == 'video':
            return self.TYPES.VIDEO
        
        elif mime_type[TYPE] == 'audio':
            return self.TYPES.AUDIO
        
        elif mime_type[TYPE] == 'application' and mime_type[SUBTYPE]  == 'octet-stream': ## TODO: also include extensions
            return self.TYPES.AUDIO
        
        elif mime_type[TYPE] == 'text':
            return self.TYPES.TEXT
        
        else:
            return self.TYPES.NOT_SUPPORTED
    
    def mime_type(self):
        # In a collection of tiles mime_type is  largest by bytes mime type in a collection.  
        # For a single file, mime_type is the type of the file 
        
        counter = {}
        
        if os.path.isdir(self.__media_path):
            for subdir, dirs, files in os.walk(self.__media_path):
                
                for file in files:
                    file_path = os.path.join(subdir,file)
                    mime_type = self.__get_mime_type(file_path)
                    counter = self.__count_mime_type(counter, mime_type, os.path.getsize(file_path))
            
            return self.__highest_mime_type(counter)
        
        else:
            return self.__get_mime_type(file_path)
    
    def convert(self):

        for subdir, dirs, files in os.walk(self.__media_path, topdown=False):
            for file in files:
                                
                src = os.path.join(subdir, file)
                type = self.__get_mime_type(file)
                
                if type in [self.TYPES.IMAGE, self.TYPES.VIDEO, self.TYPES.AUDIO]: 
                    dst = self.__set_destination_ext(type, src)
                    
                    if os.path.splitext(src)[1] != os.path.splitext(dst)[1]:
                        ff = ffmpy.FFmpeg(executable=FFMPEG_PATH, inputs={src: None}, outputs={dst: '-y'})
                        #ff.run()
                        print ('** shutil.copy(src, dst) **')
                        shutil.copy(src, dst)
                        os.remove(src)
        
        return self.mime_type()
