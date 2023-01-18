
from import_queue import import_queue 

if __name__ == "__main__":
    queue = import_queue('\\\\SERVER\\Users\\Paul\\Documents\\Projects\\Fat Boy Home Network (FBHN)\\01 Media Library\\50 TestEnvironment\\media_library')
    
    i = queue.next()
    print(i)
    
    #queue.remove(i)
    #print(queue.peek())
    
    #queue.add('item1')
    #queue.add('item2')
    #queue.add('item3')
    #queue.add('item4')
    