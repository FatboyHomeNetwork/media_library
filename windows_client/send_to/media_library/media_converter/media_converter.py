################################################################################################
#
#  media_converter
#
################################################################################################

import os
import magic
import ffmpy
import operator

import media_library as ml


class media_converter:

    #
    # Mime type id
    #
            
    def __get_mime_type(path):
        
        TYPE = 0
        SUBTYPE = 1

        mime_type = magic.from_file(path, mime=True).split('/')
        
        if mime_type[TYPE] == 'image': 
            return ml.mime_type.IMAGE
        
        elif mime_type[TYPE] == 'video':
            return ml.mime_type.VIDEO
        
        elif mime_type[TYPE] == 'audio':
            return ml.mime_type.AUDIO
        
        elif mime_type[TYPE] == 'application' and mime_type[SUBTYPE]  == 'octet-stream': ## TODO: also include extensions
            return ml.mime_type.AUDIO
        
        elif mime_type[TYPE] == 'text':
            return ml.mime_type.TEXT
        
        else:
            return ml.mime_type.NOT_SUPPORTED


    def __add_to(mime_type_sizes, tag, value):
        
        if tag in mime_type_sizes: 
            mime_type_sizes[tag] = mime_type_sizes[tag] + value
        else:
            mime_type_sizes[tag] = value

        return mime_type_sizes
    
    
    def __get_top_tag(mime_type_sizes):
                
        mime_type_sizes_sorted = sorted(mime_type_sizes.items(), key=operator.itemgetter(1))

        if len(mime_type_sizes_sorted) > 0:
            return mime_type_sizes_sorted[0][0]
        else:
            return None
 
 
    def mime_type(path):
        mime_type_sizes = {}
        
        if os.path.isdir(path):
            for subdir, dirs, files in os.walk(path):
                
                for file in files:
                    file_path = os.path.join(subdir,file)
                    mime_type = converter.__get_mime_type(file_path)
                    mime_type_sizes = converter.__add_to(mime_type_sizes, mime_type, os.path.getsize(file_path))
            
            return converter.__get_top_tag(mime_type_sizes)
        
        else:
            return converter.__get_mime_type(path)

    #
    # Media Conversion Functions
    #
    
    def __get_destination_path(mime_type, path):

        if mime_type == ml.mime_type.IMAGE: 
            return os.path.splitext(path)[0] + '.jpg'
        
        elif mime_type == ml.mime_type.VIDEO:
            return os.path.splitext(path)[0] + '.mp4'
        
        elif mime_type == ml.mime_type.AUDIO:
            return os.path.splitext(path)[0] + '.mp3'
        
        else:
            return path # no conversion needed 
    
    def convert(src_path):

        FFMPEG_PATH = 'C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe'

        for subdir, dirs, files in os.walk(src_path, topdown=False):
            for file in files:
                                
                src = os.path.join(subdir, file)
                type = converter.__get_mime_type(src)
                
                if type != converter.Mime_Type.NOT_SUPPORTED:  
                    
                    destination_path = converter.__get_destination_path(type, src)
                    if destination_path.lower() != src.lower():
                        ff = ffmpy.FFmpeg(executable=FFMPEG_PATH, inputs={src: None}, outputs={destination_path: '-y'})
                        ff.run()
                else: 
                    os.remove(src)
                    