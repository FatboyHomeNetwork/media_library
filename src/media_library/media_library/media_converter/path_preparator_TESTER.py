from  media_item_path import  media_item_path 

if __name__ == "__main__":
    mi_path = media_item_path('\\\\SERVER\\Projects\\Fat Boy Home Network (FBHN)\\Import Media\\test environment\\TorrentDownload-1\\five')
    
    print (mi_path.is_network_drive())
    
    mi_path.prepare_path()
    
    print(mi_path.likely_mime_type())
    
    
    