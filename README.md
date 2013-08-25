# Plex Channel for Jupiter Broadcasting

![Screenshot of iPad: shows view](Resources/Screenshots/iPad-shows.jpg?raw=true)
![Screenshot of web interface: episodes view](Resources/Screenshots/Web-episodes.jpg?raw=true)

- http://dev.plexapp.com/docs/channels/index.html
- https://github.com/RobLoach/plugin.video.jupiterbroadcasting

## Installing the development version from source

```
mkdir /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/JupiterBroadcasting.bundle
mkdir /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/JupiterBroadcasting.bundle/Contents
chown plex:plex /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/JupiterBroadcasting.bundle
chmod 755 /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/JupiterBroadcasting.bundle
bindfs --owner=plex --group=plex --perms=755 /home/leon/Workspaces/prive/com.plexapp.plugins.jupiterbroadcasting /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/JupiterBroadcasting.bundle/Contents/
```
## Removing ##

```
umount /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/JupiterBroadcasting.bundle/Contents/
killall bindfs
rm -rf /var/lib/plexmediaserver/
rm /var/log/upstart/plexmediaserver.log
```

## Problems ##

- Live Stream doesn't work on Plex webinterface
- Getting redirect urls is a bit slow
