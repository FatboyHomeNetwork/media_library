import os
from media_library_mgn import media_library_mgn

################################################################################################
#
#  media_library_mgn_TESTER
#
################################################################################################



mgn = media_library_mgn(r'\\SERVER\Users\Paul\Documents\Projects\FBHN_SW\media_library\test_media_library')


IMPORT_QUEUE = 'import.queue'

def clear_queue():
    
    if os.path.exists(os.path.join(mgn.PATHS.LIBRARY, IMPORT_QUEUE)):
        os.remove(os.path.join(mgn.PATHS.LIBRARY, IMPORT_QUEUE))
    open(os.path.join(mgn.PATHS.LIBRARY, IMPORT_QUEUE),'x')
    
def test__queue_next():    

    # mgn.queue(r'\\SERVER\Users\Paul\Documents\Projects\FBHN_SW\media_library\test_media_library\__test_data\five')
    # mgn.queue(r'\\SERVER\Users\Paul\Documents\Projects\FBHN_SW\media_library\test_media_library\__test_data\one')
    # mgn.queue(r'\\SERVER\Users\Paul\Documents\Projects\FBHN_SW\media_library\test_media_library\__test_data\empty_bitmap_file.bmp')
    # mgn.queue(r'\\SERVER\Users\Paul\Documents\Projects\FBHN_SW\media_library\test_media_library\__test_data\six')
    
    mgn.queue(r'\\SERVER\Users\Paul\Documents\Projects\FBHN_SW\media_library\test_media_library\__test_data\series name (1988)')
    

def test__import():
    
    mgn.import_item()
    
################################################################################################
#
#  Test Entry Point
#
################################################################################################

if __name__ == "__main__":
    
    clear_queue()
    test__queue_next()
    test__import()                                      