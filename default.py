#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmcaddon,base64

pluginhandle = int(sys.argv[1])

settings = xbmcaddon.Addon(id='plugin.video.mtv_de')
translation = settings.getLocalizedString

def index():
        addDir("ZDF","zdf",'listChannel',"")
        addDir("ZDFneo","zdfneo",'listChannel',"")
        addDir("ZDFkultur","zdfkultur",'listChannel',"")
        addDir("ZDFinfo","zdfinfo",'listChannel',"")
        addDir("3sat","dreisat",'listChannel',"")
        xbmcplugin.endOfDirectory(pluginhandle)
        if (xbmc.getSkinDir() == "skin.confluence" or xbmc.getSkinDir() == "skin.touched"): xbmc.executebuiltin('Container.SetViewMode(50)')

def listChannel(url):
        if url=="zdf":
          addDir("Das Aktuellste","http://www.zdf.de/ZDFmediathek/senderstartseite/sst1/1209114",'listVideos',"")
          addDir("Meist gesehen","http://www.zdf.de/ZDFmediathek/senderstartseite/sst2/1209114",'listVideos',"")
        elif url=="zdfneo":
          addDir("Das Aktuellste","http://www.zdf.de/ZDFmediathek/kanaluebersicht/aktuellste/857392",'listVideos',"")
          addDir("Tipps","http://www.zdf.de/ZDFmediathek/senderstartseite/sst0/1209122",'listVideos',"")
          addDir("Themen","http://www.zdf.de/ZDFmediathek/senderstartseite/sst1/1209122",'listShows',"")
          addDir("Sendungen","http://www.zdf.de/ZDFmediathek/senderstartseite/sst2/1209122",'listShows',"")
        elif url=="zdfkultur":
          addDir("Das Aktuellste","http://www.zdf.de/ZDFmediathek/kanaluebersicht/aktuellste/1321386",'listVideos',"")
          addDir("Tipps","http://www.zdf.de/ZDFmediathek/senderstartseite/sst0/1317640",'listVideos',"")
          addDir("Sendungen","http://www.zdf.de/ZDFmediathek/senderstartseite/sst1/1317640",'listShows',"")
          addDir("Meist gesehen","http://www.zdf.de/ZDFmediathek/senderstartseite/sst2/1317640",'listVideos',"")
        elif url=="zdfinfo":
          addDir("Das Aktuellste","http://www.zdf.de/ZDFmediathek/kanaluebersicht/aktuellste/398",'listVideos',"")
          addDir("Tipps","http://www.zdf.de/ZDFmediathek/senderstartseite/sst0/1209120",'listVideos',"")
          addDir("Sendungen","http://www.zdf.de/ZDFmediathek/senderstartseite/sst1/1209120",'listShows',"")
          addDir("Meist gesehen","http://www.zdf.de/ZDFmediathek/senderstartseite/sst2/1209120",'listVideos',"")
        elif url=="dreisat":
          addDir("Das Aktuellste","http://www.zdf.de/ZDFmediathek/senderstartseite/sst1/1209116",'listVideos',"")
          addDir("Sendungen","http://www.zdf.de/ZDFmediathek/senderstartseite/sst2/1209116",'listShows',"")
        xbmcplugin.endOfDirectory(pluginhandle)
        if (xbmc.getSkinDir() == "skin.confluence" or xbmc.getSkinDir() == "skin.touched"): xbmc.executebuiltin('Container.SetViewMode(50)')

def listShows(url):
        content = getUrl(url)
        spl=content.split('<div class="image">')
        for i in range(1,len(spl),1):
            entry=spl[i]
            match=re.compile('<a href="(.+?)">', re.DOTALL).findall(entry)
            url=match[0]
            match=re.compile('<img src="(.+?)"', re.DOTALL).findall(entry)
            thumb=match[0]
            thumb=thumb.replace("/timg94x65blob","/timg485x273blob")
            match=re.compile('<p><b><a href="(.+?)">(.+?)<br />', re.DOTALL).findall(entry)
            title=match[0][1]
            title=cleanTitle(title)
            addDir(title,"http://www.zdf.de"+url,'listVideos',"http://www.zdf.de"+thumb)
        xbmcplugin.endOfDirectory(pluginhandle)
        if (xbmc.getSkinDir() == "skin.confluence" or xbmc.getSkinDir() == "skin.touched"): xbmc.executebuiltin('Container.SetViewMode(500)')

def listVideos(url):
        if url.find("?bc=")>=0:
          url=url[:url.find("?bc=")]
        url=url+"?teaserListIndex=500"
        content = getUrl(url)
        spl=content.split('<div class="image">')
        for i in range(1,len(spl),1):
            entry=spl[i]
            if entry.find("BILDER</a></p>")==-1 and entry.find(">INTERAKTIV</a></p>")==-1 and entry.find(">LIVE</a></p>")==-1:
              match=re.compile('/video/(.+?)/', re.DOTALL).findall(entry)
              if len(match)>=1:
                url=match[0]
                match=re.compile('<p class="grey"><a href="(.+?), (.+?)</a></p>', re.DOTALL).findall(entry)
                date=match[0][1]
                match=re.compile('>VIDEO, (.+?)<', re.DOTALL).findall(entry)
                length=match[0]
                match=re.compile('<img src="(.+?)"', re.DOTALL).findall(entry)
                thumb=match[0]
                thumb=thumb.replace("/timg94x65blob","/timg485x273blob")
                match=re.compile('<p><b><a href="(.+?)">(.+?)<br />', re.DOTALL).findall(entry)
                title=match[0][1]
                title=cleanTitle(title)
                if length.find(":")>=0:
                  length=length+" min"
                if date.find(", ")>=0:
                  date=date[date.find(", ")+2:]
                if date.find(".20")>=0:
                  date=date[:date.find(".20")]
                title=date+" - "+title+" ("+length+")"
                addLink(title,url,'playVideo',"http://www.zdf.de"+thumb)
        xbmcplugin.endOfDirectory(pluginhandle)
        if (xbmc.getSkinDir() == "skin.confluence" or xbmc.getSkinDir() == "skin.touched"): xbmc.executebuiltin('Container.SetViewMode(500)')

def playVideo(url):
        content = getUrl("http://www.zdf.de/ZDFmediathek/xmlservice/web/beitragsDetails?id="+url+"&ak=web")
        match1=re.compile('<formitaet basetype="h264_aac_mp4_rtmp_zdfmeta_http" isDownload="false">\n                <quality>veryhigh</quality>\n                <url>(.+?)</url>', re.DOTALL).findall(content)
        match2=re.compile('<formitaet basetype="h264_aac_mp4_rtmp_zdfmeta_http" isDownload="false">\n                <quality>high</quality>\n                <url>(.+?)</url>', re.DOTALL).findall(content)
        url=""
        if len(match1)>=1:
          url=match1[0]
        elif len(match2)>=1:
          url=match2[1]
        content = getUrl(url)
        match=re.compile('<default-stream-url>(.+?)</default-stream-url>', re.DOTALL).findall(content)
        listitem = xbmcgui.ListItem(path=match[0])
        return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

def cleanTitle(title):
        title=title.replace("&lt;","<").replace("&gt;",">").replace("&amp;","&").replace("&#039;","\\").replace("&quot;","\"").replace("&szlig;","ß").replace("&ndash;","-")
        title=title.replace("&Auml;","Ä").replace("&Uuml;","Ü").replace("&Ouml;","Ö").replace("&auml;","ä").replace("&uuml;","ü").replace("&ouml;","ö")
        title=title.strip()
        return title

def getUrl(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0')
        response = urllib2.urlopen(req,timeout=5)
        link=response.read()
        response.close()
        return link

def parameters_string_to_dict(parameters):
        ''' Convert parameters encoded in a URL to a dict. '''
        paramDict = {}
        if parameters:
            paramPairs = parameters[1:].split("&")
            for paramsPair in paramPairs:
                paramSplits = paramsPair.split('=')
                if (len(paramSplits)) == 2:
                    paramDict[paramSplits[0]] = paramSplits[1]
        return paramDict

def addLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('IsPlayable', 'true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
         
params=parameters_string_to_dict(sys.argv[2])
mode=params.get('mode')
url=params.get('url')
if type(url)==type(str()):
  url=urllib.unquote_plus(url)

if mode == 'listChannel':
    listChannel(url)
elif mode == 'listVideos':
    listVideos(url)
elif mode == 'listShows':
    listShows(url)
elif mode == 'playVideo':
    playVideo(url)
else:
    index()
