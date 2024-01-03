################################################################################################
#
#  media_queue__TESTER
#
################################################################################################

import os

from media_queue import queue
from library_directories import library_directories

if __name__ == "__main__":

    paths = library_directories(str(os.getenv('MEDIA_LIBRARY')))
    q = queue(paths.SYSTEM)
    
    i = q.next()
    print(i)
    
    #queue.remove(i)
    #print(queue.peek())
    
    #queue.add('item1')
    #queue.add('item2')
    #queue.add('item3')
    #queue.add('item4')
    