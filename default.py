# -*- coding: utf-8 -*-

import urllib
import urllib2
import cookielib
import datetime
import time
import re
import os
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import cgi

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

addon         = xbmcaddon.Addon('plugin.video.fengyunzhibo')
__addonname__ = addon.getAddonInfo('name')
home          = addon.getAddonInfo('path').decode('utf-8')
icon          = xbmc.translatePath(os.path.join(home, 'icon.png'))
fanart        = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))




def log(txt):
    message = '%s: %s' % (__addonname__, txt.encode('ascii', 'ignore'))
    xbmc.log(msg=message, level=xbmc.LOGDEBUG)


def _parse_argv():

        global url,name,iconimage, mode, playlist,fchan,fres,fhost,fname,fepg

        params = {}
        try:
            params = dict( arg.split( "=" ) for arg in ((sys.argv[2][1:]).split( "&" )) )
        except:
            params = {}

        url =       demunge(params.get("url",None))
        name =      demunge(params.get("name",""))
        iconimage = demunge(params.get("iconimage",""))
#        fanart =    demunge(params.get("fanart",""))
        playlist =  demunge(params.get("playlist",""))
        fchan =     demunge(params.get("fchan",""))
        fres =      demunge(params.get("fres",""))
        fhost =     demunge(params.get("fhost",""))
        fname =     demunge(params.get("fname",""))
        fepg =      demunge(params.get("fepg",None))

        try:
            playlist=eval(playlist.replace('|',','))
        except:
            pass

        try:
            mode = int(params.get( "mode", None ))
        except:
            mode = None




def demunge(munge):
        try:
            munge = urllib.unquote_plus(munge).decode('utf-8')
        except:
            pass
        return munge







def getSources():

              log("Fengyunzhibo -- Fengyunzhibo main page")
              url = "http://www.fengyunzhibo.com/channel-list"
              req = urllib2.Request(url.encode('utf-8'))
              req.add_header('User-Agent', USER_AGENT)
              try:
                 response = urllib2.urlopen(req)
                 link1=response.read()
                 response.close()
              except:
                 link1 = ""

              link=str(link1).replace('\n','')     
              match=re.compile('<div class="list-wrap">.+?"list-title">(.+?)</h1>').findall(str(link))
              for cattext in match:
                 caturl = cattext
                 try:
                    addDir(cattext,caturl,17,icon,fanart,cattext,"TV","",False)
                 except:
                    log("Fengyunzhibo -- Problem adding directory")






def play_playlist(name, list):
        playlist = xbmc.PlayList(1)
        playlist.clear()
        item = 0
        for i in list:
            item += 1
            info = xbmcgui.ListItem('%s) %s' %(str(item),name))
            playlist.add(i, info)
        xbmc.executebuiltin('playlist.playoffset(video,0)')


def addDir(name,url,mode,iconimage,fanart,description,genre,date,showcontext=True):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description, "Genre": genre, "Year": date } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok



def addLink(url,name,iconimage,fanart,description,genre,date,showcontext=True,playlist=None):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=12"
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description, "Genre": genre, "Year": date } )
        liz.setProperty( "Fanart_Image", fanart )
        liz.setProperty('IsPlayable', 'true')
        if not playlist is None:
            playlist_name = name.split(') ')[1]
            contextMenu_ = [('Play '+playlist_name+' PlayList','XBMC.RunPlugin(%s?mode=13&name=%s&playlist=%s)' %(sys.argv[0], urllib.quote_plus(playlist_name), urllib.quote_plus(str(playlist).replace(',','|'))))]
            liz.addContextMenuItems(contextMenu_)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok


xbmcplugin.setContent(int(sys.argv[1]), 'movies')
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_GENRE)
except:
    pass


url=None
name=None
iconimage=None
mode=None
playlist=None
fchan=None
fres=None
fhost=None
fname=None
fepg=None

_parse_argv()



log("Fengyunzhibo -- Mode: "+str(mode))
if not url is None:
    print "Fengyunzhibo -- URL: "+str(url.encode('utf-8'))
#log("Fengyunzhibo -- Name: "+str(name))

if mode==None:
    log("Fengyunzhibo -- getSources")
    getSources()

elif mode==12:
    log("Fengyunzhibo -- setResolvedUrl")
    item = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

elif mode==13:
    log("Fengyunzhibo -- play_playlist")
    play_playlist(name, playlist)

elif mode==17:
              log("Fengyunzhibo -- Mode 17")
              name = url.encode('utf-8')
              url = "http://www.fengyunzhibo.com/channel-list"
              req = urllib2.Request(url.encode('utf-8'))
              req.add_header('User-Agent', USER_AGENT)
              try:
                 response = urllib2.urlopen(req)
                 link1=response.read()
                 response.close()
              except:
                 link1 = ""

              link=str(link1).replace('\n','')
              match=re.compile('<h1 class="list-title">'+name+'</h1>(.+?)</div>                </div>').findall(str(link))
              for catblock in match:
                match=re.compile('<h2 class="list-title">(.+?)</h2>').findall(str(catblock))
                for cattext in match:
                 caturl = cattext
                 try:
                    addDir(cattext,caturl,18,iconimage,fanart,cattext,"TV","",False)
                 except:
                    log("Fengyunzhibo -- Problem adding directory")

elif mode==18:
              log("Fengyunzhibo -- Mode 18")
              name = url.encode('utf-8')
              url = "http://www.fengyunzhibo.com/channel-list"
              req = urllib2.Request(url.encode('utf-8'))
              req.add_header('User-Agent', USER_AGENT)
              try:
                 response = urllib2.urlopen(req)
                 link1=response.read()
                 response.close()
              except:
                 link1 = ""

              link=str(link1).replace('\n','')
              match=re.compile('<h2 class="list-title">'+name+'</h2>(.+?)<div class="clear">').findall(str(link))
              for catblock in match:
                match=re.compile('<a class="channel-link" href="(.+?)".+?program=.+?>(.+?)<').findall(str(catblock))
                for caturl,cattext in match:
                 url = "http://www.fengyunzhibo.com"+caturl
                 req = urllib2.Request(url.encode('utf-8'))
                 req.add_header('User-Agent', USER_AGENT)
                 try:
                    response = urllib2.urlopen(req)
                    link1=response.read()
                    response.close()
                 except:
                    link1 = ""

                 link=str(link1).replace('\n','')
                 match=re.compile('snapshot: "(.+?)"'+".+?iosPlayURL: '(.+?)'").findall(str(link))
                 for iconimage,vidurl in match:
                   if not ("isVod:" in vidurl):
                    vidurl = vidurl.encode('utf-8')
                    try:
                       addLink(vidurl,cattext,iconimage,fanart,cattext,"TV","")
                    except:
                       log("Fengyunzhibo -- Problem adding directory")

xbmcplugin.endOfDirectory(int(sys.argv[1]))