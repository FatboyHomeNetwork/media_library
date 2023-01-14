    
import os
import json
import datetime
import time
import random
import win32wnet
import platform

################################################################################################
#
#  File lock
#
################################################################################################

class file_lock(object):

    def __init__(self, file):
        self.lock_path = file + '.lock'

    def __wait (self):
        return random.randint(1, 5) # between 1 and 5 seconds

    def lock (self):
        blocked = True
        while (blocked):
            try:
                open(self.lock_path,'x')
                blocked = False
            except FileExistsError: 
                time.sleep(self.__wait())

    def unlock(self):
        blocked = True
        while (blocked):
            try:
                os.remove(self.lock_path)
                blocked = False
            except FileNotFoundError:
                blocked = False

################################################################################################
#
#  unc path
#
################################################################################################

class unc_path(object):
    
    def __init__(self, path):
        
        self.path = path
    
    def __is_unc_path(self):
        # see: file_path_fomats_on_windows_systems.pdf
        
        if len(self.path) > 3 and self.path[0:2] == '\\\\' and self.path[2:3] != '?' and self.path[2:3] != '.':
            return True 
        else:
            return False


    def __as_admin_share(self):
         # C:\Dir\subDir\etc. -> \\<machine name>\C$\Dir\subDir\etc. 
         
        return  '\\\\' +  platform.node() + '\\' + self.path.replace(':','$',1)
    
    
    def as_unc(self):
        
        if self.__is_unc_path(): 
            return self.path # come as you are 
        
        try: # is a drive letter that has been mapped to a unc share?
            return win32wnet.WNetGetUniversalName(self.path, 1)  # yes
        
        # no, so ...
        except: # we'll access via admin share
            return self.__as_admin_share()
        

################################################################################################
#
#  import_queue
#
################################################################################################

MAX_ATTEMPTS = 2 

class import_queue(object):

    def __init__(self, path):
        
        QUEUE_FILE_NAME = 'import.queue'
        
        self.queue_file_path = os.path.join(path, QUEUE_FILE_NAME)
        
    
    def __load_queue(self):
                
        if os.stat(self.queue_file_path).st_size != 0:
            with open(self.queue_file_path, 'r') as read_file:
                return json.load(read_file)
        else:
            return {}
        
    def __write_queue(self, queue):
        
        with open(self.queue_file_path, 'w') as write_file:
            write_file.write(json.dumps(queue, default=str))
    
    def add(self, item):

        lock = file_lock(self.queue_file_path)
        lock.lock()
                        
        queue = self.__load_queue()
        queue[item] = [datetime.datetime.now(), 0] # date when added, number of attempts to import 
        self.__write_queue(queue)
        
        lock.unlock()
    
    def next(self):

        lock = file_lock(self.queue_file_path)
        lock.lock()
        
        item = None
        
        queue = self.__load_queue()
                       
        for k, v in queue.items():
            if  v[1] < MAX_ATTEMPTS:
                v[1] = v[1] + 1
                queue[k] = v
                item = k
                break
        
        self.__write_queue(queue)
        
        lock.unlock()
        return item 
    
    def remove(self, item):
        
        lock = file_lock(self.queue_file_path)
        lock.lock()
        
        queue = self.__load_queue()
        
        if item in queue:
            queue.pop(item)
            self.__write_queue(queue)

        lock.unlock()
