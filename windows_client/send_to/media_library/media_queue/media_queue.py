import os
import json
import datetime
import time
import random

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
        

MAX_ATTEMPTS = 10  

class media_queue(object):

    def __init__(self, path):
        self.queue_file_path = path
    
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
            #elif v[1] == MAX_ATTEMPTS write to log if an item has been i the queue for too long? 
        
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
