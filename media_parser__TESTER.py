import os

from media_parser import parser


def gen_test_file(src_path, data_file):
    
    df = open(data_file, "w")
    
    for subdir, dirs, files in os.walk(src_path):
        df.write(os.path.split(subdir)[1] + '\n')      
        for file in files:
            df.write(file + '\n')      
    df.close()    

    
def review_test_file(fn):

    file = open(fn, "r")
    
    while True:
        line  = file.readline().splitlines()
        
        if not line:
            break
        
        e = parser.parse(line[0])

        e_str = ''
        for t in e:
            e_str  += t.debug_string() + ' ' 
        
        print ('    LINE: %s' % line[0]) 
        if len(e_str) > 0:
            print('ELEMENTS: %s\n' % e_str)
        else:
            print('ELEMENTS: ** No Elements **\n')
    
    file.close()


################################################################################################
#
#  Test Entry Point
#
################################################################################################

MEDIA_FOLDER =r'\\SERVER\Users\Paul\Documents\Projects\FBHN_SW\media_library\test_normaliser\wild_media_folders.list'
MEDIA_FILE_NAMES = r'\\SERVER\Users\Paul\Documents\Projects\FBHN_SW\media_library\test_normaliser\wild_media_filenames.list'
STRUCTURED_NAMES = r'\\SERVER\Users\Paul\Documents\Projects\FBHN_SW\media_library\test_normaliser\structured_names.list'

DEV_TEST = r'\\SERVER\Users\Paul\Documents\Projects\FBHN_SW\media_library\test_normaliser\normaliser\dev.list'

if __name__ == "__main__":
    
  #  gen_test_file(r'M:\Media',MEDIA_FILE_NAMES)

    review_test_file(DEV_TEST)

    #review_test_file(MEDIA_FOLDER)
    #review_test_file(MEDIA_FILE_NAMES)
    #review_test_file(STRUCTURED_NAMES)
