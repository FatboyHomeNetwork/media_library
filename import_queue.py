import os
import time
import random
import json
import datetime

################################################################################################
#
#  File lock
#
################################################################################################

LOCK_FILE_PATH = '.lock'
MAX_SECONDS = 5 # Seconds

class file_lock(object):

    def __init__(self, file):
        self.lock_path = file + LOCK_FILE_PATH

    def __wait (self):
        return random.randint(1, MAX_SECONDS)  # pause 1 to MAX_SECONDS seconds

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
#  import_queue
#
################################################################################################

MAX_ATTEMPTS = 2 
QUEUE_FILE_NAME = 'import.queue'

class queue(object):

    def __init__(self, path):
        
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
