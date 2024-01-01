from file_lock import file_lock

if __name__ == "__main__":
    lock =  file_lock('\\\\SERVER\\Projects\\Fat Boy Home Network (FBHN)\\Import Media\\test environment\\import_queue')
    
    
    lock.unlock()
    #lock.lock()
