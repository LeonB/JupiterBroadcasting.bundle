from StringIO import StringIO
import urllib2 #need for HEAD requests
import socket

ARCHIVE_SUMMARY   = 'Archived / discontinued shows'
ARCHIVE_THUMB     = 'jupiterbroadcasting.jpg'
ARCHIVE_TITLE     = 'Archived Shows'
JB_ART            = 'art-default.jpg'
JB_ICON           = 'icon-default.png'
JB_PRODUCER       = 'Jupiter Broadcasting'
LIVE_STREAM_THUMB = 'jupiterbroadcasting.jpg'
LIVE_STREAM_TITLE = 'The Jupiter Broadcasting Live Stream'
LIVE_STREAM_URL   = 'http://videocdn-us.geocdn.scaleengine.net/jblive-iphone/live/jblive.stream/playlist.m3u8'
TITLE             = 'Jupiter Broadcasting'
USER_AGENT        = 'Plex Jupiter Broadcasting Channel'

###############################################################################
def Start():
    # resetShowsCache() # only when debuggin
    # resetArchivedShowsCache() # only when debuggin
    Plugin.AddPrefixHandler("/video/jupiterbroadcasting", MainMenu, L('jupiterbroadcasting'), JB_ICON, JB_ART)
    Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
    Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')

    # Set up containers for all possible objects
    ObjectContainer.title1 = TITLE
    ObjectContainer.view_group = 'InfoList'
    ObjectContainer.art = R(JB_ART)
    DirectoryObject.thumb = R(JB_ICON)
    DirectoryObject.art = R(JB_ART)

    HTTP.CacheTime = CACHE_1HOUR
    HTTP.Headers['User-Agent'] = USER_AGENT

####################################################################################################
# Menus
####################################################################################################
@handler('/video/jupiterbroadcasting', TITLE)
def MainMenu():
    oc = ObjectContainer()

    # Add live stream
    title = LIVE_STREAM_TITLE
    oc.add(createEpisodeObject(
        url=LIVE_STREAM_URL,
        title=title,
        summary=title,
        thumb=R(LIVE_STREAM_THUMB),
        rating_key=title))

    # Add shows
    for show in getActiveShows():
        show_name = show['name']
        oc.add(DirectoryObject(
            key=Callback(ShowMenu, show_name=show_name),
            title=show_name,
            thumb=R(show['image']),
            summary=show['plot']))

    # Add archive
    oc.add(DirectoryObject(
        key=Callback(ArchiveMenu),
        title=ARCHIVE_TITLE,
        thumb=R(ARCHIVE_THUMB),
        summary=ARCHIVE_SUMMARY))

    return oc

@route('/video/jupiterbroadcasting/archive')
def ArchiveMenu():
    oc = ObjectContainer(title2='Archive', view_group='InfoList')

    for show in getArchivedShows():
        show_name = show['name']
        oc.add(DirectoryObject(
            key=Callback(ShowMenu, show_name=show_name),
            title=show_name,
            thumb=R(show['image']),
            summary=show['plot']))

    return oc

@route('/video/jupiterbroadcasting/show/{show_name}')
def ShowMenu(show_name, limit=None, offset=0):
    show = getShow(show_name)
    rss = getShowEpisodes(show)
    oc = ObjectContainer(title2=show_name, view_group='InfoList')
    offset = int(offset)

    if limit == None:
        limit = show['limit']
    else:
        limit = int(limit)

    Log.Debug("offset: %d" % offset)
    Log.Debug("limit: %d" % limit)

    for entry in rss.entries[offset:(offset+limit)]:
        Log.Debug(entry)

        show_name = show['name']
        title = entry.title
        summary = entry.subtitle if entry.has_key('subtitle') else None
        thumb = entry.media_thumbnail[0]['url'] if entry.has_key('media_thumbnail') else R(show['image'])
        date = Datetime.ParseDate(entry.updated)
        url = entry.enclosures[0]['href']
        if entry.has_key('itunes_duration'):
            duration = Datetime.MillisecondsFromString(entry.itunes_duration)
        else:
            duration = None

        Log.Debug("url: %s" % url)

        oc.add(createEpisodeObject(
            url=url,
            title=title,
            summary=summary,
            thumb=thumb,
            rating_key=title,
            originally_available_at=date,
            duration=duration,
            show_name=show_name))

    if show['pagination'] == True and (offset+limit) < len(rss.entries):
        oc.add(DirectoryObject(
            key=Callback(ShowMenu, show_name=show_name, limit=limit, offset=(offset+limit)),
            title="Page %d" % (((offset+limit)/limit)+1),
            thumb=R(show['image']),
            summary='View older episodes'))

    return oc

####################################################################################################

def getActiveShows():
    if not Data.Exists('shows'):
        Log.Debug('Loading shows from disk')
        data = Resource.Load('Shows.json', binary=False)
        shows = JSON.ObjectFromString(data)
        Data.SaveObject('shows', shows)
    else:
        Log.Debug('Loading shows from cache')
        shows = Data.LoadObject('shows')

    return shows

def resetShowsCache():
    if Data.Exists('shows'):
        Data.Remove('shows')

def getArchivedShows():
    if not Data.Exists('archived_shows'):
        Log.Debug('Loading archived shows from disk')
        data = Resource.Load('ArchivedShows.json', binary=False)
        archived_shows = JSON.ObjectFromString(data)
        Data.SaveObject('archived_shows', archived_shows)
    else:
        Log.Debug('Loading archived shows from cache')
        archived_shows = Data.LoadObject('archived_shows')

    return archived_shows

def resetArchivedShowsCache():
    if Data.Exists('archived_shows'):
        Data.Remove('archived_shows')

def getShow(show_name):
    shows = getActiveShows()
    shows = filter(lambda show: show['name'] == show_name, shows)

    if len(shows) == 1:
        return shows[0]

    archivedShows = getArchivedShows()
    archivedShows = filter(lambda show: show['name'] == show_name, archivedShows)
    return archivedShows[0]

def getShowEpisodes(show):
    # http://pythonhosted.org/feedparser/
    return RSS.FeedFromURL(show['feed'])

def createEpisodeObject(url, title, summary, thumb, rating_key, originally_available_at=None, duration=None, show_name=None, include_container=False):
    container = Container.MP4
    video_codec = VideoCodec.H264
    audio_codec = AudioCodec.AAC
    audio_channels = 2

    track_object = EpisodeObject(
        key = Callback(
            createEpisodeObject,
            url=url,
            title=title,
            summary=summary,
            thumb=thumb,
            rating_key=rating_key,
            originally_available_at=originally_available_at,
            duration=duration,
            show_name=show_name,
            include_container=True
        ),
        rating_key = rating_key,
        title = title,
        summary = summary,
        # thumb = thumb,
        thumb=thumb,
        originally_available_at = originally_available_at,
        duration = duration,
        producers = [],
        show = show_name,
        items = [
            MediaObject(
                parts = [
                    PartObject(key=Callback(PlayVideo, url=url))
                ],
                container = container,
                video_codec = video_codec,
                audio_codec = audio_codec,
                audio_channels = audio_channels,
            )
        ]
    )

    if include_container:
        return ObjectContainer(objects=[track_object])
    else:
        return track_object

@indirect
def PlayVideo(url):
    return IndirectResponse(VideoClipObject, key=url)
    # return IndirectResponse(VideoClipObject, key=getFinalUrl(url))
