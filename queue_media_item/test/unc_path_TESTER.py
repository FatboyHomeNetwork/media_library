from  unc_path import  unc_path 

if __name__ == "__main__":

    
    # An existing share
    #PATH = '\\\\SERVER\\Users\\Paul\\Documents\\Projects\\Fat Boy Home Network (FBHN)\\01 Media Library\\50 TestEnvironment\\_test_data\\five'
    
    # a drive letter mapped to a unc share 
    PATH = 'I:\\Folder'
    
    # A local drive mapped to an admin share unc path 
    #PATH = "C:\\intel"
        
    print (unc_path(PATH).as_unc())
    
    