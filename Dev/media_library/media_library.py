import os
from enum import Enum    

class mime_type(Enum):
    IMAGE = 1
    VIDEO = 2
    AUDIO = 3
    TEXT = 4
        
    NOT_SUPPORTED = 99

def log_file(lp):
    return os.path.join(lp, 'system', 'media_library.log')

def tmp_path(lp):
    return os.path.join(lp, 'system','temp')

def queue_file(lp):
    return os.path.join(lp, 'system','import.queue')


def media_path(lp):
    return os.path.join(lp, 'media')