import json
from StringIO import StringIO
from time import mktime
from datetime import datetime
import urllib2
import socket

TITLE            = 'Jupiter Broadcasting'
JB_FEED_URL      = 'http://vimcasts.org/episodes.json'
JB_ICON          = 'icon-default.png'
JB_ART           = 'art-default.jpg'
LIVE_STREAM_URL  = 'http://videocdn-us.geocdn.scaleengine.net/jblive-iphone/live/jblive.stream/playlist.m3u8'

RE_PODTRAC_URL   = '^http://www.podtrac.com/pts/redirect.mp4/(.*)$'

###############################################################################
def Start():
    resetShowsCache()
    resetArchivedShowsCache()
    # Plugin.AddPrefixHandler("/video/jupiterbroadcasting", MainMenu, L('jupiterbroadcasting'), JB_ICON, JB_ART)
    Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
    Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')

    # Set up containers for all possible objects
    ObjectContainer.title1 = TITLE
    ObjectContainer.view_group = 'InfoList'
    ObjectContainer.art = R(JB_ART)
    DirectoryObject.thumb = R(JB_ICON)
    DirectoryObject.art = R(JB_ART)
    # VideoClipObject.thumb = R(JB_ICON)
    # VideoClipObject.art = R(JB_ART)

    HTTP.CacheTime = CACHE_1HOUR
    HTTP.Headers['User-Agent'] = 'Plex Jupiter Broadcasting Channel'

####################################################################################################
# Menus
####################################################################################################
@handler('/video/jupiterbroadcasting', TITLE)
def MainMenu():
    oc = ObjectContainer()

    # Add live stream
    title = 'The Jupiter Broadcasting Live Stream'
    oc.add(createEpisodeObject(
        url=LIVE_STREAM_URL,
        title=title,
        summary=title,
        thumb=R('jupiterbroadcasting.jpg'),
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
        title='Archived Shows',
        thumb=R('jupiterbroadcasting.jpg'),
        summary='Archived / discontinued shows'))

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
        date = datetime.fromtimestamp(mktime(entry.updated_parsed))
        if entry.has_key('itunes_duration'):
            duration = Datetime.MillisecondsFromString(entry.itunes_duration)
        else:
            duration = None
        try:
            url = getFinalUrl(entry.enclosures[0]['href'])
        except urllib2.HTTPError as e:
            Log.Warn("Problem with %s: %s" % (url, e.reason))
            continue
        except socket.timeout as e:
            Log.Warn("%s took to long to complete" % url)
            continue

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
        io = StringIO(data)
        shows = json.load(io)
        Data.SaveObject('shows', shows)
    else:
        Log.Debug('Loading shows from cache')
        shows = Data.LoadObject('shows')

    return shows

def resetShowsCache():
    if Data.Exists('shows'):
        Data.Remove('shows')

# def getFinalUrl(url):
#     if Data.Exists('redirects'):
#         redirects = Data.LoadObject('redirects')
#     else:
#         redirects = {}

#     if url not in redirects:
#         Log.Debug("Checking redirects for %s" % url)
#         req = urllib2.Request(url)
#         req.get_method = lambda: 'HEAD'
#         res = urllib2.urlopen(req, timeout=3.0)
#         final_url = res.geturl()
#         redirects = {url: final_url}
#         Data.SaveObject('redirects', redirects)

#     return redirects[url]

def getFinalUrl(url):
    redirects = Dict['redirects']
    if not redirects:
        redirects = {}

    if url not in redirects:
        Log.Debug("Checking redirects for %s" % url)

        m = RE_PODTRAC_URL.match(url)
        if m:
            final_url = "http://%s" % m.group(1)
        else:
            req = urllib2.Request(url, None, HTTP.Headers)
            req.get_method = lambda: 'HEAD'
            res = urllib2.urlopen(req, timeout=3.0)
            final_url = res.geturl()

        redirects = {url: final_url}
        Dict['redirects'] = redirects
        Dict.Save()

    return redirects[url]

def getArchivedShows():
    if not Data.Exists('archived_shows'):
        Log.Debug('Loading archived shows from disk')
        data = Resource.Load('ArchivedShows.json', binary=False)
        io = StringIO(data)
        archived_shows = json.load(io)
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
    # if not Data.Exists('rss'):
    #     rss = RSS.FeedFromURL(show['feed'])
    #     Data.SaveObject('rss', rss)
    # else:
    #     rss = Data.LoadObject('rss')

    # return rss

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
        producers = ['Jupiter Broadcasting'],
        show = show_name,
        items = [
            MediaObject(
                parts = [
                    PartObject(key=url)
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
