import os



from media_normaliser import normaliser 
import  media_normaliser
from decoder import tokeniser


import re

def dev__token_regex():
    
    season_pattern = re.compile(r'(season|s)\s*[0-9]{1,3}',flags=re.IGNORECASE) 
    episode_pattern = re.compile(r'(episode|e|part)\s*[0-9]{1,3}',flags=re.IGNORECASE)
    number_pattern = re.compile('[0-9]{1,3}')
        
        #012345678901234567890   
    #s = 'part 01 season 2'
    s = 's1e1.mpg'
    #s = 's02e91'
    #s = 'season 02 e 99'
    #s = 'season 02 episode 222'
    #s = 'season 02     episode 22111'
    #s = 'a man for all season.'
    #s = 'Episode.'
    #s = 'Episode 01 S2.'
    #s = 's 1 e 02'
    #s = 'blah blah blah'
    
    print(s)
    season_match = season_pattern.search(s)
    if season_match:
        print ('season', int(number_pattern.search(season_match.group()).group()))
    
    episode_match = episode_pattern.search(s)
    if episode_match:
        print ('episode', int(number_pattern.search(episode_match.group()).group()))


def test__tokeniser():
    
    #s = 'part 01 season 2'
    s = 's1e1.mpg'
    #s = 's02e91'
    #s = 'season 02 e 99'
    #s = 'season 02 episode 222'
    #s = 'season 02     episode 22111'
    #s = 'a man for all season.'
    #s = 'Episode.'
    #s = 'Episode 01 S2.'
    #s = 's 1 e 02'
    #s = 'blah blah blah'
    
    elements = tokeniser.tokenise(s)
    
    for e in elements:
        print(e)
    

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

# media_normaliser.create_path_model
TEST_PATH = r'\\SERVER\Users\Paul\Documents\Projects\FBHN_SW\media_library\test_normaliser\test_folder_model'
TEST_MEDIA = r'series'

DEV_TEST = r'\\SERVER\Users\Paul\Documents\Projects\FBHN_SW\media_library\test_normaliser\normaliser\dev.list'



if __name__ == "__main__":
    
    ## Tokeniser dev and test     
    # token_regex_dev()    
    # test__tokeniser()

    # exit()
    
    ## Model Creation Testing  
    # Create model from folder path 
    model = media_normaliser.create_path_model(TEST_PATH, TEST_MEDIA)
    # Create model from test data file 
    #model = create_path_model(DEV_TEST)
    
    #for p in model:
    #    print (p)
        
    
    ## Normaliser testing
    n = normaliser(model)
    norm_model = n.normalise()
    
    for p in norm_model:
        print (p)
    