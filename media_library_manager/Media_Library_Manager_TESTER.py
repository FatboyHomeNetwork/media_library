from import_queue_manager import import_queue_manager


if __name__ == "__main__":
    
    IMPORT_QUEUE_PATH = '\\\\SERVER\\Users\\Paul\\Documents\\Projects\\Fat Boy Home Network (FBHN)\\01 Media Library\\50 TestEnvironment\\media_library'
    
    # An existing share
    #PATH = '\\\\SERVER\\Users\\Paul\\Documents\\Projects\\Fat Boy Home Network (FBHN)\\01 Media Library\\50 TestEnvironment\\_test_data\\five'
    
    # a drive letter mapped to a unc share 
    #PATH = 'I:\\Folder'
    
    # A local drive mapped to an admin share unc path 
    PATH = "C:\\intel"
    
    import_queue_manager = import_queue_manager(IMPORT_QUEUE_PATH)
    import_queue_manager.add(PATH)
