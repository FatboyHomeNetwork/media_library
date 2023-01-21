import media_item_library as mi
from media_item_library import media_library
import os


#
# Model tester baby!
#


#print ('************************************************')

#series = mi.series('\\\\SERVER\\Projects\\Fat Boy Home Network (FBHN)\\Import Media\\test environment\\TorrentDownload-1\\series name (1988)')

#print (series)

lib_path = '\\\\SERVER\\Projects\\Fat Boy Home Network (FBHN)\\Import Media\\test environment\\media_library'

tmp_path = '\\\\SERVER\\Projects\\Fat Boy Home Network (FBHN)\\Import Media\\test environment\\media_library\\tmp\\'
#
series_path = '\\\\SERVER\\Projects\\Fat Boy Home Network (FBHN)\\Import Media\\test environment\\TorrentDownload-1\\series name 1988'

#import shutil

#shutil.copytree(series_path, os.path.join(tmp_path, os.path.basename(series_path)))

lib =  media_library(lib_path)
lib.add(series_path)