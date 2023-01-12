################################################################################################
#
#  File lock
#
################################################################################################

import os
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
