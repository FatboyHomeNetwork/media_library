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

    mgn.queue_next(r'\\SERVER\Users\Paul\Documents\Projects\FBHN_SW\media_library\test_media_library\__test_data\five')
    mgn.queue_next(r'\\SERVER\Users\Paul\Documents\Projects\FBHN_SW\media_library\test_media_library\__test_data\one')
    mgn.queue_next(r'\\SERVER\Users\Paul\Documents\Projects\FBHN_SW\media_library\test_media_library\__test_data\empty_bitmap_file.bmp')
    mgn.queue_next(r'\\SERVER\Users\Paul\Documents\Projects\FBHN_SW\media_library\test_media_library\__test_data\six')

def test__import_next():
    
    mgn.import_next()
    mgn.import_next()
    mgn.import_next()
    mgn.import_next()

################################################################################################
#
#  Test Entry Point
#
################################################################################################

if __name__ == "__main__":
    
    clear_queue()
    test__queue_next()
    test__import_next()                                      