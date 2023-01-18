
import media_library_manager as mlm

if __name__ == "__main__":
    
    MEDIA_LIBRARY = '\\\\SERVER\\Users\Paul\\Documents\\GitHub\\media_library\\test\\media_library'
    
    # An existing share
    #PATH = '\\\\SERVER\\Users\\Paul\\Documents\\Projects\\Fat Boy Home Network (FBHN)\\01 Media Library\\50 TestEnvironment\\_test_data\\five'
    
    # a drive letter mapped to a unc share 
    #PATH = 'I:\\Folder'
    
    # A local drive mapped to an admin share unc path 
    PATH = "C:\\intel"
    
    mlm = media_library_manager(IMPORT_QUEUE_PATH)
    mlm.queue(PATH)
