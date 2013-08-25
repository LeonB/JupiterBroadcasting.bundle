# Plex Channel for Jupiter Broadcasting

You can view all of the running and discontinued shows of [Jupiter Broadcasting](http://www.jupiterbroadcasting.com) with this channel and view the JB live stream.

## Screenshots

Screenshot of iPad:

![Screenshot of iPad: shows view](Resources/Screenshots/iPad-shows.jpg?raw=true)

Screenshot of web interface:

![Screenshot of web interface: episodes view](Resources/Screenshots/Web-episodes.jpg?raw=true)

## Installing the development version from source on Ubuntu

``` shell
service plexmediaserver stop
mkdir /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/JupiterBroadcasting.bundle
git clone https://github.com/LeonB/com.plexapp.plugins.jupiterbroadcasting.git /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/JupiterBroadcasting.bundle/Contents
chown -R plex:plex /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/JupiterBroadcasting.bundle
chmod -R 755 /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/JupiterBroadcasting.bundle
service plexmediaserver start
```

## Problems ##

- Live Stream doesn't work on Plex webinterface
- Getting redirect urls is a bit slow
- No selecting of video/audio quality

## Thanks ##

- Rob Loach for the [XBMC Jupiter Broadcasting plugin](https://github.com/RobLoach/plugin.video.jupiterbroadcasting)
- Chris Fisher for the awesome Jupiter Broadcasting network
