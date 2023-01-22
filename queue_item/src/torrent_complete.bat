@echo off

REM called by Deluge when a torrent has finished downloading.  

set torrentid=%1
set torrentname=%2
set torrentpath=%3

start "Queue Torrent" "C:\Program Files\Python\Python39\pythonw.exe" "C:\Program Files\Import Media\queue_item.py" %torrentpath%"\"%torrentname% 
