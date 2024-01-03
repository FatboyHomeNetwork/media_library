
from decoder import decoder


def test__decode():

    file = open(r'\\SERVER\Users\Paul\Documents\Projects\FBHN_SW\media_library\test_normaliser\test_media_folders.list', "r")
    
    d = decoder()
    while True:
        line  = file.readline().splitlines()
        
        if not line:
            break
        
        e = d.decode(line[0])

        e_str = ''
        for t in e:
            e_str  += t.as_string() + ' ' 
        
        print ('LINE: %s' % line[0]) 
        print('ELEMENTS: %s' % e_str)
    
    file.close()


################################################################################################
#
#  Test Entry Point
#
################################################################################################

if __name__ == "__main__":
    
    test__decode()
    