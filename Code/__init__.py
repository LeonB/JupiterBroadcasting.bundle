# import htmlentitydefs
# import re
# from datetime import datetime
# from email.utils import parsedate

import json
from StringIO import StringIO
from time import mktime
from datetime import datetime
import urllib2

TITLE            = 'Jupiter Broadcasting'
JB_FEED_URL      = 'http://vimcasts.org/episodes.json'
JB_ICON          = 'icon-default.png'
JB_ART           = 'art-default.jpg'

SHOWS = {}

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

####################################################################################################
# Menus
####################################################################################################
@handler('/video/jupiterbroadcasting', TITLE)
def MainMenu():
    oc = ObjectContainer()

    # Add live stream
    oc.add(DirectoryObject(
        key=Callback(ArchiveMenu),
        title='Live Stream',
        thumb=R('jupiterbroadcasting.jpg'),
        summary='The JBLive stream'))

    # Add shows
    for show in activeShows():
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

    for show in archivedactiveShows():
        show_name = show['name']
        oc.add(DirectoryObject(
            key=Callback(ShowMenu, show_name=show_name),
            title=show_name,
            thumb=R(show['image']),
            summary=show['plot']))

    return oc

@route('/video/jupiterbroadcasting/show/{show_name}')
def ShowMenu(show_name):
    show = getShow(show_name)
    rss = getShowEpisodes(show)
    oc = ObjectContainer(title2=show_name, view_group='InfoList')

    for entry in rss.entries:
        Log.Debug(entry)

        show_name = show['name']
        title = entry.title
        summary = entry.subtitle if entry.has_key('subtitle') else None
        thumb = entry.media_thumbnail[0]['url'] if entry.has_key('media_thumbnail') else None
        date = datetime.fromtimestamp(mktime(entry.updated_parsed))
        if entry.has_key('itunes_duration'):
            duration = Datetime.MillisecondsFromString(entry.itunes_duration)
        else:
            duration = None
        try:
            url = getFinalUrl(entry.enclosures[0]['href'])
        except HTTPError:
            continue

        Log.Debug("url: %s" % url)

        oc.add(createEpisodeObject(
            url=url,
            title=title,
            summary=summary,
            thumb=thumb,
            originally_available_at=date,
            duration=duration,
            rating_key=title,
            show_name=show_name))

    return oc

####################################################################################################

def activeShows():
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

def getFinalUrl(url):
    redirects = Dict['redirects']
    if not redirects:
        redirects = {}

    if url not in redirects:
        Log.Debug("Checking redirects for %s" % url)
        req = urllib2.Request(url)
        req.get_method = lambda: 'HEAD'
        res = urllib2.urlopen(req)
        final_url = res.geturl()
        redirects = {url: final_url}
        Dict['redirects'] = redirects

    return redirects[url]

def archivedactiveShows():
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
    shows = activeShows()
    shows = filter(lambda show: show['name'] == show_name, shows)

    if len(shows) == 1:
        return shows[0]

    archivedShows = archivedactiveShows()
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

def createEpisodeObject(url, title, summary, thumb, originally_available_at, duration, rating_key, show_name, include_container=False):
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
            originally_available_at=originally_available_at,
            duration=duration,
            rating_key=rating_key,
            show_name=show_name,
            include_container=True
        ),
        rating_key = url,
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
