# Plex Channel for Jupiter Broadcasting

- http://dev.plexapp.com/docs/channels/index.html
- https://github.com/RobLoach/plugin.video.jupiterbroadcasting

## Installing the development version from source

```
sudo mkdir /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/JupiterBroadcasting.bundle
sudo mkdir /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/JupiterBroadcasting.bundle/Contents
sudo chown plex:plex /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/JupiterBroadcasting.bundle
sudo chmod 755 /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/JupiterBroadcasting.bundle
sudo bindfs --owner=plex --group=plex --perms=755 /home/leon/Workspaces/prive/com.plexapp.plugins.jupiterbroadcasting /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/JupiterBroadcasting.bundle/Contents/
```
## Removing ##

```
umount /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/JupiterBroadcasting.bundle/Contents/
killall bindfs
rm -rf /var/lib/plexmediaserver/
```
