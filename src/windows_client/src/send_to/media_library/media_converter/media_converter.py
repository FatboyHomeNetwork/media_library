
import os
import magic
import ffmpy
import operator


IMAGE = 1
VIDEO = 2
AUDIO = 3
TEXT = 4
APPLICATION = 5
        
NOT_SUPPORTED = 99

def get_mime_type(path):
        
        TYPE = 0
        SUBTYPE = 1

        mime_type = magic.from_file(path, mime=True).split('/')
        
        if mime_type[TYPE] == 'image': 
            return IMAGE
        
        elif mime_type[TYPE] == 'video':
            return VIDEO
        
        elif mime_type[TYPE] == 'audio':
            return AUDIO
        
        elif mime_type[TYPE] == 'application' and mime_type[SUBTYPE]  == 'octet-stream': ## TODO: also include extensions
            return AUDIO
        
        elif mime_type[TYPE] == 'text':
            return TEXT
        
        else:
            return NOT_SUPPORTED


class media_converter:

    #def __init__(self):
    #    

    def __add_to(self, mime_type_sizes, tag, value):
        
        if tag in mime_type_sizes: 
            mime_type_sizes[tag] = mime_type_sizes[tag] + value
        else:
            mime_type_sizes[tag] = value

        return mime_type_sizes
    
    
    def __get_top_tag(self, mime_type_sizes):
                
        mime_type_sizes_sorted = sorted(mime_type_sizes.items(), key=operator.itemgetter(1))

        if len(mime_type_sizes_sorted) > 0:
            return mime_type_sizes_sorted[0][0]
        else:
            return None
  
    def mime_type(self, source_path):
        
        mime_type_sizes = {}
        
        if os.path.isdir(source_path):
            for subdir, dirs, files in os.walk(source_path):
                
                for file in files:
                    file_path = os.path.join(subdir,file)
                    mime_type = get_mime_type(file_path)
                    mime_type_sizes = self.__add_to(mime_type_sizes, mime_type, os.path.getsize(file_path))
            
            return self.__get_top_tag(mime_type_sizes)
        
        else:
            return get_mime_type(file_path)

    def __set_destination_ext(self, mime_type, path):

        if mime_type == IMAGE: 
            return os.path.splitext(path)[0] + '.jpg'
        elif mime_type == VIDEO:
            return os.path.splitext(path)[0] + '.mp4'
        elif mime_type == AUDIO:
            return os.path.splitext(path)[0] + '.mp3'
        else:
            return path 
    
    def convert(self, path):

        FFMPEG_PATH = 'C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe'

        for subdir, dirs, files in os.walk(path, topdown=False):
            for file in files:
                                
                src = os.path.join(subdir, file)
                type = get_mime_type(src)
                
                if type in [IMAGE, VIDEO, AUDIO]: 
                    dst = self.__set_destination_ext(type, src)
                    
                    if os.path.splitext(src)[1] != os.path.splitext(dst)[1]:
                        ff = ffmpy.FFmpeg(executable=FFMPEG_PATH, inputs={src: None}, outputs={dst: '-y'})
                        ff.run()
                        os.remove(src)
                else: 
                    os.remove(src)