# Plex Channel for Jupiter Broadcasting

You can view all of the running and discontinued shows of [Jupiter Broadcasting](http://www.jupiterbroadcasting.com) with this channel and view the JB live stream.

## Screenshots

Screenshot of iPad:

![Screenshot of iPad: shows view](Contents/Resources/Screenshots/iPad-shows.jpg?raw=true)

Screenshot of web interface:

![Screenshot of web interface: episodes view](Contents/Resources/Screenshots/Web-episodes.jpg?raw=true)

Screenshot of PleXBMC:

![Screenshot of Plex on XBMC: archive view](Contents/Resources/Screenshots/PleXBMC-archive.jpg?raw=true)

## Installing the development version on Ubuntu

``` shell
service plexmediaserver stop
mkdir /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/JupiterBroadcasting.bundle
git clone https://github.com/LeonB/com.plexapp.plugins.jupiterbroadcasting.git /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/JupiterBroadcasting.bundle
chown -R plex:plex /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/JupiterBroadcasting.bundle
chmod -R 755 /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/JupiterBroadcasting.bundle
service plexmediaserver start
```

## Installing the development version on FreeBSD

``` shell
service plexmediaserver stop
mkdir /usr/local/plexdata/Plex Media Server/Plug-ins/JupiterBroadcasting.bundle/
git clone https://github.com/LeonB/com.plexapp.plugins.jupiterbroadcasting.git /usr/local/plexdata/Plex Media Server/Plug-ins/JupiterBroadcasting.bundle
chown -R _plex:_plex /usr/local/plexdata/Plex Media Server/Plug-ins/JupiterBroadcasting.bundle/
find /usr/local/plexdata/Plex Media Server/Plug-ins/JupiterBroadcasting.bundle/ -type f -exec chmod 644 {} +
find /usr/local/plexdata/Plex Media Server/Plug-ins/JupiterBroadcasting.bundle/ -type d -exec chmod 755 {} +
service plexmediaserver start
```

## Problems ##

- Live Stream doesn't work on Plex webinterface
- No selecting of video/audio quality

## Thanks ##

- Rob Loach for the [XBMC Jupiter Broadcasting plugin](https://github.com/RobLoach/plugin.video.jupiterbroadcasting)
- Chris Fisher for the awesome Jupiter Broadcasting network
- Sander Spies for getting this channel in the Plexapp store
