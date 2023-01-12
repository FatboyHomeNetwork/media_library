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
|Audio| mp3 |
|Video| mp4 |
|Image| jpg |

### Network name standard formats

| Media Type  | Network Name Format |
|---|---|
|Movies| title (year) |
|TV Show, Series| Series_Name year S01E02 Episode_Name | 
|Music| Artist /  Album / 01 track title |

## Design Concept 

The media library will be a shared folder within SERVER. Importing into the library will use an import queue and server pull approach. Items to be imported will first be added to network queue. A windows scheduled task will periodically check the queue, and start the the copy, convert and import into media library process for any new items found in the queue. 

The copy process will run on SERVER and SERVER will be responsible for restarting the copy in the event of failure. 

Media conversion will use standard libraries.  

Sharing the media library within the network will be implemented using standard components and services. To support all network users, the shares will be configured to support anonymous sharing. 

### Importing in to the media library 

#### Windows Users

Add an option *Import Media* to the **Send To** function in windows explorer. This option would add the network unc path for the item to the import queue. Once in the queue, the item would be imported imported in the library as part of the scheduled network import function. 

**Sent to** is a windows explorer context menu function. When selected it presents a list of various *destinations* the item could be sent to. These destinations are short cuts that link to an executable able to take files and folders a command line options. 

Using the **Sent to** function, users will be able to select any item that can access - on their local or shared drives - and chose to send it to the import queue. 

The implementation will be a python script and icons needed to create a new destination in the users send to function

*Send to location:* shell:sendto or C:\Users\<user>\AppData\Roaming\Microsoft\Windows\SendTo

#### Torrent and Network Rip Services

Other network services will also need to import items into the media library. Torrent services and network rip would both need to import items.

The design concept is simple to the windows user. At completion of download or rip, the service would add a unc path to the item to the import queue. Once it the queue the item would be processed like any other. 

The implementation of this will be a wrapper that interfaces between each services and the Media Library Manager module. Media Library Manager module provides the code interface (API) for the media library. 

### Media Converting

`ffmpeg.e` all the way!

### Name Normalisation  

Three distinct types of media names to normalise: 

1. Movies
2. Music
3. Episodic (TV shows, news series, etc)

Music item normalisaiton will be performed by iTuens as part of the HomeShare Server implementation. Movie and Episodic items will be normalised by a custom decoder. 

### Share as various services 

The media library is a windows drive. As a windows drive it can be shared in different ways, in most cases by simply configuring a services. 

Where ever possible the design will be to automate the install and config of different ways the library will be shared.

1. NFS
2. SMB/CIFS
3. HomeShare

#### HomeShare what and why? 

- support apple tv audio player. cooler audio player free for apple tv. 
- only works with homeshare.

On windows HomeShare runs as services in iTunes; run iTunes, have HomeShare available for apple tv. Which is great if you always want to run a foreground process on your laptop.

However, by configuring and running iTunes as a windows background process on SERVER, HomeShare can be managed as any other service used to access the media library.


### Scheduled Backup

Backup will be performed by the network back up solution. 


