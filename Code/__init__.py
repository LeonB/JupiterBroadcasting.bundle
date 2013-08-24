# import htmlentitydefs
# import re
# from datetime import datetime
# from email.utils import parsedate

import json
from StringIO import StringIO
from time import mktime
from datetime import datetime

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

    # HTTP.CacheTime = CACHE_1HOUR

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
        show_name = show['name']
        title = entry.title
        summary = entry.subtitle if entry.has_key('subtitle') else 'Test'
        date = datetime.fromtimestamp(mktime(entry.updated_parsed))
        # oc.add(VideoClipObject(
        #     url = 'http://201308.jb-dl.cdn.scaleengine.net/coderradio/2013/cr-0063-432p.mp4',
        #     title = title,
        #     summary = summary,
        #     thumb = 'http://www.jupiterbroadcasting.com/wp-content/uploads/2013/08/cr-0063-v.jpg',
        #     originally_available_at = date,
        #     # key = 1.0,
        #     # rating_key = 2.0,
        # ))
        # break

        oc.add(DirectoryObject(
            key=Callback(ShowMenu, show_name=show_name),
            title=title,
            thumb=Resource.ContentsOfURLWithFallback(url='http://vimcasts.org/images/posters/show_invisibles.png', fallback=R('icon-default.png')),
            # thumb=R(show['image']),
            # art='http://vimcasts.org/images/posters/show_invisibles.png',
            summary=summary,
            tagline='Je moeder'))

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
