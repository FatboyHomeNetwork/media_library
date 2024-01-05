import os

from media_normaliser import normaliser 
import  media_normaliser

TEST_PATH = r'\\SERVER\Users\Paul\Documents\Projects\FBHN_SW\media_library\test_normaliser\test_folder_model'
DEV_TEST = r'\\SERVER\Users\Paul\Documents\Projects\FBHN_SW\media_library\test_normaliser\normaliser\dev.list'

# creates the model from a data file, not an actual folder. Only useful for testing  
def create_path_model(src_path):
    
    model = []
    
    file = open(src_path, "r")
    
    while True:
        line  = file.readline().splitlines()
        
        if not line:
            break
        
        model.append(line)
    
    return model

################################################################################################
#
#  Test Entry Point. test__XXX test a function or method, other functions support 
#
################################################################################################

if __name__ == "__main__":
    
    ## Model Testing 
    
    ## Create model from folder path 
    #model = media_normaliser.create_path_model(TEST_PATH)
    
    # Create model from test data file 
    model = create_path_model(DEV_TEST)
    
    #for p in model:
    #    print (p)
        
    
    ## Normaliser testing
    
    n = normaliser(model)
    norm_model = n.normalise()
    
    for p in norm_model:
        print (p)
    