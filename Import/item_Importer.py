################################################################################################
#
#  item_importer
#
################################################################################################


import sys
import os
import shutil
import distutils.dir_util
import media_library

def dst_path(path, media_item_name):

    m_type = mp.what_is_it(path)
        
    if m_type =='audio':
        return os.path.join(c.music_path, media_item_name)
    elif m_type == 'image':
        return os.path.join(c.image_path, media_item_name)
    elif m_type == 'video':
        return os.path.join(c.video_path, media_item_name)
    else:
        return os.path.join(c.other_path, media_item_name)

#
# main()
#

started_msg = 'started'
stopped_msg = 'stopped' 
clean_msg = 'cleaned'
dest_msg = 'destination'
not_found_msg = 'not found'


class item_importer:

    def __init__(self, unc_path):
        
        self.unc_path = unc_path
    
    
    def __likely_type(self):
        return None # what are the std types? movies, media, music,  pictures, video, unknown type
    
    def import_item (self):
        
        try:
            src = media_queue.next(c.import_queue_path)

            if src != None:
                if os.path.exists(src):

                    log.message(c.import_log_path, started_msg, src)
                            
                    media_item_name = os.path.basename(src)
                    tmp = os.path.join(c.tmp_path, media_item_name)
                    
                    if os.path.isdir(src):
                        distutils.dir_util.copy_tree(src, tmp)
                    else:
                        shutil.copy2(src,tmp)
                    
                    tmp = prep_path(tmp)
                    mp.convert(tmp)
                    
                    if mp.what_is_it(tmp) == 'video':
                        log.message(c.import_log_path, clean_msg, tmp)
                        clean_media_path(tmp)
                            
                    dst = dst_path(tmp, media_item_name)
                    log.message(c.import_log_path, dest_msg, dst)
                    
                    # move
                    distutils.dir_util.copy_tree(tmp, dst)
                    distutils.dir_util.remove_tree(tmp)
                    
                    log.message(c.import_log_path, stopped_msg, src)
                else:
                    log.message(c.import_log_path, not_found_msg, src)    
                    
                media_queue.remove(c.import_queue_path, src) 

        except Exception as e:
            print('e baby!',e)
            log.crash_report(__file__, e, sys.exc_info())