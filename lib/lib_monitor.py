import os
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
from lib.db_defaults import dbFunctions 
import json as simplejson

_monitor    = xbmc.Monitor()
_home		= xbmcgui.Window(10000)
_play	    = xbmc.Player()
_cap	    = xbmc.RenderCapture()
_dialog     = xbmcgui.Dialog()
_dbF        = dbFunctions()
_addon		= xbmcaddon.Addon()
_updb		= 'true'

class libMonitor(xbmc.Monitor):
    def onScanFinished(self, library):
        if _addon.getSetting('updb') == "true":
        	_dbF.scn_db(_updb)
    def  onCleanFinished(self, library):
        if _addon.getSetting('clndb') == "true":
        	_dbF.cln_db()
    # def onSettingsChanged(self):
    # 	_dialog.ok('test1',"")


class Player(xbmc.Player):
	def init(self,title="not yet"):
		self.check()
		# _dialog.ok("",str(_home.getProperty("checked")))
		if self.video:
			if _home.getProperty("checked") != "true":
				_home.setProperty("checked","true")
				self.item = dbFunctions().query_pl(title,_play.getPlayingFile())
				# _dialog.textviewer("",str(self.item))
				self.updateplayer(self.item)
		













		# 	self.jsonp = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}')
		# 	self.jsonp = unicode(self.jsonp, 'utf-8', errors='ignore')
		# 	self.json  = simplejson.loads(self.jsonp)
		# 	for self.item in self.json['result']:
		# 		self.player = self.item.get('playerid', '')
		# 	self.jsonq = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Player.GetItem", "params": { "properties": ["title", "artist", "season", "episode", "duration", "showtitle", "tvshowid", "thumbnail", "file", "fanart", "streamdetails"], "playerid": 0 }, "id": "VideoGetItem"}')
		# 	try:
		# 		self.save_results(self.jsonq)
		# 	except:
		# 		return
				# _home.setProperty("checked","true")
				# self.itempath=_play.getPlayingFile()
				# self.info=_play.getVideoInfoTag().getPath() 
				# self.infoid=_play.getVideoInfoTag().getDbId() 
				# _dialog.ok("",str(self.info))
				# _dialog.ok("",str(self.infoid))
		return
	# def save_results(self,title):
	# 	self.file=open(addon_set, "a")
	# 	self.file.write(title+"\n")
	# 	return
	def check(self):
		self.video=_play.isPlayingVideo()
		if self.video:
			# Video().captures(1920,1080)
			return
		else:
			_home.clearProperty("checked")
			return
	def updateplayer(self,info):
		try:
			self.art=info.get('art',"")
			self.poster=self.art.get('poster','')
			self.fanart=self.art.get('fanart','')
			# _dialog.ok("",str(self.poster))
			self.item=xbmcgui.ListItem(thumbnailImage=self.poster,iconImage =self.poster)
			self.item.setPath(xbmc.Player().getPlayingFile())
			self.item.setArt(self.art)
			self.item.setInfo('video',{'mediatype':'movie', 'title':info.get('title','')+" Multi-Disc",'poster':self.poster, 'plot':info.get('plot',''),})
		# self.item.setInfo('video',{'title':info.get('title',''),'art':info.get('art',''), 'cast':info.get('cast',''), 'year': info.get('year',''), 'plot':info.get('plot',''), 'path':info.get('file',''), 'rating':info.get('rating',''), 'mpaa':info.get('mpaa',''), 'dateadded':info.get('dateadded','')})
        # self._listitem.setInfo('video',{'title':self.title, 'year': self.year, 'plot': self.plot, 'path':self.path, 'rating':self.rating, 'mpaa':self.mpaa, 'dateadded':self.dateadded})
			_play.updateInfoTag(self.item)
		except:
			_home.clearProperty("checked")
		return




class Video(xbmc.RenderCapture):
	def captures(self,width="32",height="32"):
		_cap.capture(width,height)
		self.rgb=()
		self.pixels=_cap.getImage(1000)
		self.width = _cap.getWidth()
		self.height = _cap.getHeight()
		self.addon_set  = xbmc.translatePath('special://userdata/addon_data/script.libraryhelper/results.txt')
		for self.y in range(self.height):
		 	self.row = self.width * self.y * 4 
		 	for self.x in range(self.width):
		 		self.rgb[0] = self.pixels[self.row + self.x * 4 + 2]
		 		self.rgb[1] = self.pixels[self.row + self.x * 4 + 1]
		 		self.rgb[2] = self.pixels[self.row + self.x * 4]




		_dialog.textviewer('te',str(self.rbg))




####### Updated 011818