# Network Media Library

## Requirements

Network wide library of media - movies, tv shows, music, home moves, & pictures

The Network Media Library will: 

1. Import  media from any node within the network into the network media library 
2. Convert imported media to network standard media formats 
3. Normalise imported media's file name to network name standard formats 
4. Share the media items via: SMB 1.0; NFS; Apple HomeShare within the network
5. Perform scheduled off site back up of media library

### Standard media formats 

| media type  | network format |
|---|---|
|Audio| ? |
|Video| ? |
|Image| ? |

### Network name standard formats

| Media Type  | Network Name Format |
|---|---|
|Movies| ? |
|TV Show, Series| ? |
|Music| ? |

## Design Concept 

The media library will be a shared folder within SERVER. Importing into the library will use an import queue and server pull approach. Items to be imported will first be added to network queue. A windows scheduled task periodically checks the queue, and kicks off the copy, convert and import process for any new items found in the queue. 

The copy process will run on SERVER and SERVER will be responsible for restarting the copy in the event of failure. 

Media conversion will use standard libraries.  

Sharing the media library within the network will be implemented using standard components and services. To support all network users, the shares will be configured to support anonymous sharing. 

### Importing in to the media library 

#### Windows Users

will use Send To ... windows explore shell function. 

#### Torrent and Network Rip Services

Other services: torrent services and network rip
Python wrapper add a item path to the queue. This would be triggered by the torrent service on the completion of a torrent download. 

### Name Normalisation  

Three distinct types of media names to normalise: 

1. Movies
2. Music
3. Episodic (TV shows, news series, etc)

Music item normalisaiton will be performed by iTuens as part of the HomeShare Server implementation. Movie and Episodic items will be normalised by a custom decoder. 

### Scheduled Backup

Backup will be performed by the network back up solution. 


