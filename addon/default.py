#!/usr/bin/python														   #
# -*- coding: utf-8 -*-													   #
#                          VortexPlay Addon                                 #
#                     Desenvolvido por Braz Ferreira                       #
#############################=IMPORTS=######################################
	#Kodi Specific
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs
	#Python Specific
import base64,os,re,time,sys,urllib.request
import urllib.parse,urllib.error,json,datetime,shutil
import xml.dom.minidom
from xml.dom.minidom import Node
from datetime import datetime,timedelta
	#Addon Specific
from resources.modules import control,tools,popup,speedtest
try:
	from resources.modules.online_updater import OnlineUpdater
	ONLINE_UPDATE_AVAILABLE = True
except:
	ONLINE_UPDATE_AVAILABLE = False
##########################=VARIABLES=#######################################
ADDON = xbmcaddon.Addon()
ADDONPATH = ADDON.getAddonInfo("path")
ADDON_NAME = ADDON.getAddonInfo("name")
ADDON_ID = ADDON.getAddonInfo('id')

DIALOG			  = xbmcgui.Dialog()
DP				  = xbmcgui.DialogProgress()
HOME			  = xbmcvfs.translatePath('special://home/')
ADDONS			  = os.path.join(HOME,	   'addons')
USERDATA		  = os.path.join(HOME,	   'userdata')
PLUGIN			  = os.path.join(ADDONS,   ADDON_ID)
PACKAGES		  = os.path.join(ADDONS,   'packages')
ADDONDATA		  = os.path.join(USERDATA, 'addon_data', ADDON_ID)
ADVANCED		  = os.path.join(USERDATA,	'advancedsettings.xml')
advanced_settings = os.path.join(PLUGIN,'resources', 'advanced_settings')
MEDIA			  = os.path.join(ADDONS,  PLUGIN , 'resources', 'media')
KODIV			  = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
M3U_PATH		  = os.path.join(ADDONDATA,  'm3u.m3u')
##########################=ART PATHS=#######################################
icon			  = os.path.join(PLUGIN,  'icon.png')
fanart			  = os.path.join(PLUGIN,  'fanart.jpg')
background		  = os.path.join(MEDIA,   'background.jpg')
live			  = os.path.join(MEDIA,   'live.jpg')
catch			  = os.path.join(MEDIA,   'cu.jpg')
Moviesod		  = os.path.join(MEDIA,   'movie.jpg')
Tvseries		  = os.path.join(MEDIA,   'tv.jpg')
iconextras		  = os.path.join(MEDIA,   'iconextras.png')
iconsettings	  = os.path.join(MEDIA,   'iconsettings.png')
iconlive		  = os.path.join(MEDIA,   'iconlive.png')
iconcatchup		  = os.path.join(MEDIA,   'iconcatchup.png')
iconMoviesod	  = os.path.join(MEDIA,   'iconmovies.png')
iconTvseries	  = os.path.join(MEDIA,   'icontvseries.png')
iconsearch		  = os.path.join(MEDIA,   'iconsearch.png')
iconaccount		  = os.path.join(MEDIA,   'iconaccount.png')
icontvguide		  = os.path.join(MEDIA,   'iconguide.png')

#########################=XC VARIABLES=#####################################
server_option	  = control.setting('server_option')
if server_option == 'Servidor 2':
	dns			  = control.setting('DNS2')
	username	  = control.setting('Username2')
	password	  = control.setting('Password2')
elif server_option == 'Servidor 3':
	dns			  = control.setting('DNS3')
	username	  = control.setting('Username3')
	password	  = control.setting('Password3')
elif server_option == 'Servidor 4':
	dns			  = control.setting('DNS4')
	username	  = control.setting('Username4')
	password	  = control.setting('Password4')
else:
	dns			  = control.setting('DNS')
	username	  = control.setting('Username')
	password	  = control.setting('Password')
live_url		  = '{0}/enigma2.php?username={1}&password={2}&type=get_live_categories'.format(dns,username,password)
vod_url			  = '{0}/enigma2.php?username={1}&password={2}&type=get_vod_categories'.format(dns,username,password)
series_url		  = '{0}/enigma2.php?username={1}&password={2}&type=get_series_categories'.format(dns,username,password)
panel_api		  = '{0}/panel_api.php?username={1}&password={2}'.format(dns,username,password)
player_api		  = '{0}/player_api.php?username={1}&password={2}'.format(dns,username,password)
play_url		  = '{0}/live/{1}/{2}/'.format(dns,username,password)
play_live		  = '{0}/{1}/{2}/'.format(dns,username,password)
play_movies		  = '{0}/movie/{1}/{2}/'.format(dns,username,password)
play_series		  = '{0}/series/{1}/{2}/'.format(dns,username,password)
#############################################################################
adult_tags = ['xxx','xXx','XXX','adult','Adult','ADULT','adults','Adults','ADULTS','porn','Porn','PORN']

def buildcleanurl(url):
	url = str(url).replace('USERNAME',username).replace('PASSWORD',password)
	return url

def start(signin):
	# Verificação automática de atualizações (silenciosa)
	if ONLINE_UPDATE_AVAILABLE:
		try:
			updater = OnlineUpdater()
			updater.auto_update_on_startup()
		except:
			pass
	
	if username == "":
		# Primeiro, perguntar qual servidor usar
		server_choice = xbmcgui.Dialog().select('Escolha o Servidor', ['Servidor 1 (Ragnatech)', 'Servidor 2 (Chanelvs)', 'Servidor 3 (NewOneBlack)', 'Servidor 4 (OneNewEasy)'])
		if server_choice == 0:
			control.setSetting('server_option','Servidor 1')
			dns = tools.keypopup('Enter DNS')
			usern = tools.keypopup('Enter Username')
			passw = tools.keypopup('Enter Password')
			control.setSetting('DNS',dns)
			control.setSetting('Username',usern)
			control.setSetting('Password',passw)
		elif server_choice == 1:
			control.setSetting('server_option','Servidor 2')
			dns = tools.keypopup('Enter DNS')
			usern = tools.keypopup('Enter Username')
			passw = tools.keypopup('Enter Password')
			control.setSetting('DNS2',dns)
			control.setSetting('Username2',usern)
			control.setSetting('Password2',passw)
		elif server_choice == 2:
			control.setSetting('server_option','Servidor 3')
			dns = tools.keypopup('Enter DNS')
			usern = tools.keypopup('Enter Username')
			passw = tools.keypopup('Enter Password')
			control.setSetting('DNS3',dns)
			control.setSetting('Username3',usern)
			control.setSetting('Password3',passw)
		elif server_choice == 3:
			control.setSetting('server_option','Servidor 4')
			dns = tools.keypopup('Enter DNS')
			usern = tools.keypopup('Enter Username')
			passw = tools.keypopup('Enter Password')
			control.setSetting('DNS4',dns)
			control.setSetting('Username4',usern)
			control.setSetting('Password4',passw)
		else:
			return
		
		xbmc.executebuiltin('Container.Refresh')
		auth_url = '{0}/player_api.php?username={1}&password={2}'.format(dns,usern,passw)
		response = tools.OPEN_URL(auth_url)
		parse = json.loads(response)
		login_data = parse['user_info']['auth']
		if login_data == 0:
			line1 = "Incorrect Login Details"
			line2 = "Please Re-enter" 
			line3 = "" 
			xbmcgui.Dialog().ok('Attention', line1+'\n'+line2+'\n'+line3)
			start()
		else:
			line1 = "Login Sucsessfull"
			line2 = "Welcome to "+ADDON_NAME
			line3 = ('[B][COLOR white]%s[/COLOR][/B]'%usern)
			xbmcgui.Dialog().ok(ADDON_NAME, line1+'\n' + line2 +'\n' + line3)
			adult_set()
			#tvguidesetup()
			addonsettings('ADS2','')
			xbmc.executebuiltin('Container.Refresh')
			home()
	else:
		home()

def home():
	# Ordem solicitada: CANAIS, FILMES, SÉRIES
	tools.addDir('[B][COLOR white][UPPERCASE]📺 CANAIS AO VIVO[/UPPERCASE][/COLOR][/B]','live',1,iconlive,background,'')
	tools.addDir('[B][COLOR white][UPPERCASE]🎬 FILMES[/UPPERCASE][/COLOR][/B]','vod',3,iconMoviesod,background,'')
	tools.addDir('[B][COLOR white][UPPERCASE]📺 SÉRIES DE TV[/UPPERCASE][/COLOR][/B]','live',18,iconTvseries,background,'')
	tools.addDir('[B][COLOR white][UPPERCASE]🔍 BUSCAR[/UPPERCASE][/COLOR][/B]','url',5,iconsearch,background,'')
	tools.addDir('[B][COLOR white][UPPERCASE]👤 INFORMAÇÕES DA CONTA[/UPPERCASE][/COLOR][/B]','url',6,iconaccount,background,'')
	tools.addDir('[B][COLOR white][UPPERCASE]⚙️ CONFIGURAÇÕES[/UPPERCASE][/COLOR][/B]','url',8,iconsettings,background,'')
	tools.addDir('[B][COLOR white][UPPERCASE]➕ EXTRAS[/UPPERCASE][/COLOR][/B]','url',16,iconextras,background,'')

def livecategory():
	open = tools.OPEN_URL(live_url)
	i = 0
	doc = xml.dom.minidom.parseString(open)
	for topic in doc.getElementsByTagName('channel'):
		name= tools.b64(doc.getElementsByTagName('title')[i].firstChild.nodeValue)
		url2 = tools.check_protocol(doc.getElementsByTagName('playlist_url')[i].firstChild.nodeValue).replace('<![CDATA[','').replace(']]>','')
		if xbmcaddon.Addon().getSetting('hidexxx')=='false':
			tools.addDir('%s'%name,url2,2,icon,live,'')
		else:
			if not any(s in name for s in adult_tags):
				tools.addDir('%s'%name,url2,2,icon,background,'')
		i +=1

def Livelist(url):
	url	 = buildcleanurl(url)
	open = tools.OPEN_URL(url)
	i = 0
	doc = xml.dom.minidom.parseString(open)
	for topic in doc.getElementsByTagName('channel'):
		name = re.sub('\[.*?min ','-',tools.b64(doc.getElementsByTagName('title')[i].firstChild.nodeValue))
		url1 = tools.check_protocol(doc.getElementsByTagName('stream_url')[i].firstChild.nodeValue).replace('<![CDATA[','').replace(']]>','')
		try:
			thumb = (doc.getElementsByTagName('desc_image')[i].firstChild.nodeValue).replace('<![CDATA[ ','').replace(' ]]>','')
			desc = tools.b64(doc.getElementsByTagName('description')[i].firstChild.nodeValue)
		except:
			thumb = live
			desc = 'No Info Available'
		if xbmcaddon.Addon().getSetting('hidexxx')=='false':
			tools.addDir('%s'%name,url1,4,thumb,background,desc)
		else:
			if not any(s in name for s in adult_tags):
				tools.addDir('%s'%name,url1,4,thumb,background,desc)
		i +=1

def series_cats(url):
	open = tools.OPEN_URL(player_api+'&action=get_series_categories')
	parse = json.loads(open)
	vod_cat = parse
	for cat in vod_cat:
		if xbmcaddon.Addon().getSetting('hidexxx')=='false':
			tools.addDir(cat['category_name'],player_api+'&action=get_series&category_id='+cat['category_id'],25,icon,background,'')
		else:
			if not any(s in name for s in adult_tags):
				tools.addDir(cat['category_name'],player_api+'&action=get_series&category_id='+cat['category_id'],25,icon,background,'')

def serieslist(url):
	open  = tools.OPEN_URL(url)
	ser_cat = json.loads(open)
	for ser in ser_cat:	
		name = ser['name']
		url = player_api+'&action=get_series_info&series_id='+str(ser['series_id'])
		try:
			thumb = ser['cover']
			background = ser['backdrop_path'][0]
			plot = ser['plot']
			releaseDate = ser['releaseDate']
			cast = str(ser['cast']).split()
			rating_5based = ser['rating_5based']
			episode_run_time = str(ser['episode_run_time'])
			genre = ser['genre']
		except:
			thumb = icon
			plot = ''
			releasedate = ''
			cast = ('', '')
			rating_5based = ''
			episode_run_time = ''
			genre = ''
		if xbmcaddon.Addon().getSetting('meta') == 'true':
			tools.addDirMeta(name,url,19,thumb,background,plot,releaseDate,cast,rating_5based,episode_run_time,genre)
		else:
			#tools.log('[FTG]--')
			tools.addDir(name,url,19,thumb,background,'')
		

def series_seasons(url):
	open  = tools.OPEN_URL(url)
	ser_cat = json.loads(open)
	for ser in ser_cat['episodes']:
		info = ser_cat['info']
		try:
			thumb = info['cover']
		except:
			thumb = ''
		try:
			background = info['backdrop_path'][0]
		except:
			background = ''
		tools.addDir('Season - '+ser,url+'&season_number='+str(ser),20,thumb,background,'')

def season_list(url):
	tools.log(url)
	open  = tools.OPEN_URL(url)
	ser_cat = json.loads(open)
	info = ser_cat['info']
	ser_cat = ser_cat['episodes']
	from urllib.parse import urlparse, parse_qs
	parsed_url = urlparse(url)
	season_number = str(parse_qs(parsed_url.query)['season_number'][0])
	for ser in ser_cat[season_number]:
		url = play_series+str(ser['id'])+'.'+ser['container_extension']
		try:
			thumb = ser['info']['movie_image']
		except:
			thumb = ''
		try:
			background = ser['info']['movie_image']
		except:
			background = ''
		try:
			plot = ser['info']['plot']
		except:
			plot = ''
		try:
			releasedate = ser['info']['releasedate']
		except:
			releasedate = ''
		try:
			cast = str(info['cast']).split()
		except:
			cast = ('', '')
		try:
			rating_5based = info['rating_5based']
		except:
			rating_5based = ''
		try:
			duration = str(ser['info']['duration'])
		except:
			duration = ''
		try:
			genre = info['genre']
		except:
			genre = ''
			
		if xbmcaddon.Addon().getSetting('meta') == 'true':
			tools.log(cast)
			tools.addDirMeta(ser['title'],url,4,thumb,background,plot,releasedate,cast,rating_5based,duration,genre)
		else:
			tools.addDir(ser['title'],url,4,thumb,background,'')
		

def vod(url):
	if url =="vod":
		open = tools.OPEN_URL(vod_url)
	else:
		url	 = buildcleanurl(url)
		open = tools.OPEN_URL(url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		if '<playlist_url>' in open:
			name = str(tools.b64(tools.regex_from_to(a,'<title>','</title>'))).replace('?','')
			url1 = tools.check_protocol(tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>',''))
			if xbmcaddon.Addon().getSetting('hidexxx')=='false':
				tools.addDir(name,url1,3,icon,background,'')
			else:
				if not any(s in name for s in adult_tags):
					tools.addDir(name,url1,3,icon,background,'')
		else:
			if xbmcaddon.Addon().getSetting('meta') == 'true':
				try:
					name = tools.b64(tools.regex_from_to(a,'<title>','</title>'))
					thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
					url = tools.check_protocol(tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>',''))
					desc = tools.b64(tools.regex_from_to(a,'<description>','</description>'))
					plot = tools.regex_from_to(desc,'PLOT:','\n')
					try:
						cast = tools.regex_from_to(desc,'CAST:','\n')
					except:
						cast = ('', '')
					ratin= tools.regex_from_to(desc,'RATING:','\n')
					year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
					year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
					runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
					genre= tools.regex_from_to(desc,'GENRE:','\n')
					tools.addDirMeta(str(name).replace('[/COLOR][/B].','.[/COLOR][/B]'),url,4,thumb,background,plot,str(year).replace("['","").replace("']",""),str(cast).split(),ratin,runt,genre)
				except:pass
				xbmcplugin.setContent(int(sys.argv[1]), 'vod')
			else:
				name = tools.b64(tools.regex_from_to(a,'<title>','</title>'))
				thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
				url = tools.check_protocol(tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>',''))
				desc = tools.b64(tools.regex_from_to(a,'<description>','</description>'))
				tools.addDir(name,url,4,thumb,background,desc)

def search():
	text = searchdialog()
	if not text:
		return
	
	text = text.lower()
	tools.log('Buscando por: ' + str(text))
	
	try:
		open = tools.OPEN_URL(panel_api)
		parse = json.loads(open)
		all_chans = tools.regex_get_all(open,'{"num":','}')
		
		found_results = False
		for a in all_chans:
			name = tools.regex_from_to(a,'name":"','"')
			url	 = tools.regex_from_to(a,'"stream_id":"','"')
			thumb= tools.regex_from_to(a,'stream_icon":"','"').replace('\/','/')
			stream_type = tools.regex_from_to(a,'"stream_type":"','"').replace('\/','/')
			container_extension = tools.regex_from_to(a,'container_extension":"','"')
			
			if text in name.lower():
				found_results = True
				if xbmcaddon.Addon().getSetting('hidexxx')=='false':
					if 'movie' in stream_type:
						tools.addDir(name,play_movies+url+'.'+container_extension,4,thumb,background,'')
					elif 'live' in stream_type:
						tools.addDir(name,play_live+url,4,thumb,background,'')
				else:
					if not any(s in name.lower() for s in [tag.lower() for tag in adult_tags]):
						if 'movie' in stream_type:
							tools.addDir(name,play_movies+url+'.'+container_extension,4,thumb,background,'')
						elif 'live' in stream_type:
							tools.addDir(name,play_live+url,4,thumb,background,'')
		
		if not found_results:
			xbmcgui.Dialog().notification('VortexPlay', 'Nenhum resultado encontrado', xbmcgui.NOTIFICATION_INFO, 3000)
			
	except Exception as e:
		tools.log('Erro na busca: ' + str(e))
		xbmcgui.Dialog().notification('VortexPlay', 'Erro na busca', xbmcgui.NOTIFICATION_ERROR, 3000)

def catchup():
	open = tools.OPEN_URL(panel_api+'&action=get_live_streams')
	data = json.loads(open)
	for streams in data:
		if not streams['tv_archive']:
			continue
		try:
			thumb = streams['stream_icon']
		except:
			thumb = iconcatchup
		name = streams['name']
		stream_id = str(streams['stream_id'])
		if not name=="":
				tools.addDir(name,'url',13,thumb,background,stream_id)

def tvarchive(name,description):
	APIv2 = "{0}/player_api.php?username={1}&password={2}&action=get_simple_data_table&stream_id={3}".format(dns,username,password,description)
	link = tools.OPEN_URL(APIv2)
	data = json.loads(link)
	for streams in data['epg_listings']:
		if not streams['has_archive']:
			continue
		if not streams['start']:
			continue
		name = base64.b64decode(streams['title']).decode('UTF-8')
		stream_id = streams['id']
		plot = base64.b64decode(streams['description']).decode('UTF-8')
		start = streams['start']
		end = streams['end']
		format = '%Y-%m-%d %H:%M:%S'
		start_obj = datetime(*(time.strptime(start, format)[0:6]))
		end_obj = datetime(*(time.strptime(end, format)[0:6]))
		start_api_obj = start_obj.strftime('%Y-%m-%d:%H-%M')
		end_api_obj = end_obj.strftime('%Y-%m-%d:%H-%M')
		difference = end_obj - start_obj
		duration = difference.total_seconds()
		duration = round(duration / 60)
		start2 = start[:-3]
		editstart = start2
		start2 = str(start2).replace(' ',' - ')
		catchupURL = "{0}/streaming/timeshift.php?username={1}&password={2}&stream={3}&start=".format(dns,username,password,description)
		ResultURL = catchupURL + str(start_api_obj) + "&duration={0}".format(duration)
		Fname = "[B][COLOR white]{0}[/COLOR][/B] - {1}".format(start2,name)
		tools.addDir(Fname,ResultURL,4,iconcatchup,background,plot)

#############################

def tvguide():
		xbmc.executebuiltin('ActivateWindow(TVGuide)')

def stream_video(url):
	url = buildcleanurl(url)
	
	# Log para debug
	tools.log('Tentando reproduzir: ' + str(url))
	
	# Headers básicos mas eficazes
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
		'Referer': dns
	}
	
	# Criar ListItem básico
	liz = xbmcgui.ListItem('')
	liz.setArt({'icon': icon, 'thumb': icon})
	liz.setInfo(type='Video', infoLabels={'Title': '', 'Plot': ''})
	liz.setProperty('IsPlayable', 'true')
	
	# Configurações básicas de rede que funcionam
	liz.setProperty('network.buffer_mode', '1')
	liz.setProperty('network.readbufferfactor', '4.0')
	liz.setProperty('network.cachemembuffersize', '20971520')  # 20MB
	
	# Limpar URL de caracteres problemáticos
	url = url.replace(' ', '%20')
	
	# Método 1: Tentar com headers básicos
	try:
		if '|' not in url:
			url_with_headers = url + '|User-Agent=' + headers['User-Agent']
		else:
			url_with_headers = url
		
		liz.setPath(str(url_with_headers))
		tools.log('Método 1: URL com headers')
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
		return
	except Exception as e:
		tools.log('Método 1 falhou: ' + str(e))
	
	# Método 2: Tentar sem headers
	try:
		liz2 = xbmcgui.ListItem('')
		liz2.setArt({'icon': icon, 'thumb': icon})
		liz2.setInfo(type='Video', infoLabels={'Title': '', 'Plot': ''})
		liz2.setProperty('IsPlayable', 'true')
		liz2.setPath(str(url))
		tools.log('Método 2: URL simples')
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz2)
		return
	except Exception as e:
		tools.log('Método 2 falhou: ' + str(e))
	
	# Método 3: Último recurso - ListItem mínimo
	try:
		liz3 = xbmcgui.ListItem('')
		liz3.setProperty('IsPlayable', 'true')
		liz3.setPath(str(url))
		tools.log('Método 3: ListItem mínimo')
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz3)
		return
	except Exception as e:
		tools.log('Método 3 falhou: ' + str(e))
		# Notificar erro ao usuário
		xbmcgui.Dialog().notification('VortexPlay', 'Erro na reprodução', xbmcgui.NOTIFICATION_ERROR, 3000)

def searchdialog():
	search = control.inputDialog(heading='Search '+ADDON_NAME+':')
	if search=="":
		return
	else:
		return search

def settingsmenu():
	if xbmcaddon.Addon().getSetting('meta')=='true':
		META = '[B][COLOR lime]ON[/COLOR][/B]'
	else:
		META = '[B][COLOR red]OFF[/COLOR][/B]'
	if xbmcaddon.Addon().getSetting('hidexxx')=='true':
		xxx = '[B][COLOR lime]ON[/COLOR][/B]'
	else:
		xxx = '[B][COLOR red]OFF[/COLOR][/B]'
	
	current_server = control.setting('server_option')
	if current_server == 'Servidor 2':
		server_status = '[B][COLOR yellow]Servidor 2 (Chanelvs)[/COLOR][/B]'
	elif current_server == 'Servidor 3':
		server_status = '[B][COLOR yellow]Servidor 3 (NewOneBlack)[/COLOR][/B]'
	elif current_server == 'Servidor 4':
		server_status = '[B][COLOR yellow]Servidor 4 (OneNewEasy)[/COLOR][/B]'
	else:
		server_status = '[B][COLOR yellow]Servidor 1 (Ragnatech)[/COLOR][/B]'
	
	tools.addDir('Servidor Atual: %s'%server_status,'CHANGE_SERVER',10,icon,background,'')
	if ONLINE_UPDATE_AVAILABLE:
		tools.addDir('VERIFICAR ATUALIZAÇÕES','CHECK_UPDATES',10,icon,background,'')
	tools.addDir('META IS %s'%META,'META',10,icon,background,META)
	tools.addDir('BLOQUEAR CONTEÚDO ADULTO IS %s'%xxx,'XXX',10,icon,background,xxx)
	tools.addDir('SAIR','LO',10,icon,background,'')

def addonsettings(url,description):
	url	 = buildcleanurl(url)
	if	 url =="clearcache":
		dialog = xbmcgui.Dialog().yesno('LIMPAR CACHE', 'Deseja realmente limpar o cache?', 'SIM', 'NÃO')
		if dialog:
			tools.clear_cache()
			xbmcgui.Dialog().notification('VortexPlay', 'Cache limpo com sucesso!', xbmcgui.NOTIFICATION_INFO, 3000)
	elif url =="CHANGE_SERVER":
		current_server = control.setting('server_option')
		server_options = ['Servidor 1 (Ragnatech)', 'Servidor 2 (Chanelvs)', 'Servidor 3 (NewOneBlack)', 'Servidor 4 (OneNewEasy)']
		
		dialog = xbmcgui.Dialog().select('Escolha o Servidor', server_options)
		if dialog == 0:
			control.setSetting('server_option', 'Servidor 1')
			xbmc.executebuiltin('Container.Refresh')
		elif dialog == 1:
			control.setSetting('server_option', 'Servidor 2')
			xbmc.executebuiltin('Container.Refresh')
		elif dialog == 2:
			control.setSetting('server_option', 'Servidor 3')
			xbmc.executebuiltin('Container.Refresh')
		elif dialog == 3:
			control.setSetting('server_option', 'Servidor 4')
			xbmc.executebuiltin('Container.Refresh')
	elif url =="CHECK_UPDATES":
		if ONLINE_UPDATE_AVAILABLE:
			try:
				updater = OnlineUpdater()
				updater.force_update_check()
			except Exception as e:
				xbmcgui.Dialog().ok('VortexPlay', f'Erro ao verificar atualizações:\n{str(e)}')
	elif url =="AS":
		xbmc.executebuiltin('Addon.OpenSettings(%s)'% ADDON_ID)
	elif url =="ADS":
		dialog = xbmcgui.Dialog().select('Edit Advanced Settings', ['Open AutoConfig','Enable Fire TV Stick AS','Enable Fire TV AS','Enable 1GB Ram or Lower AS','Enable 2GB Ram or Higher AS','Enable Nvidia Shield AS','Disable AS'])
		if dialog==0:
			advancedsettings('auto')
		elif dialog==1:
			advancedsettings('stick')
			tools.ASln()
		elif dialog==2:
			advancedsettings('firetv')
			tools.ASln()
		elif dialog==3:
			advancedsettings('lessthan')
			tools.ASln()
		elif dialog==4:
			advancedsettings('morethan')
			tools.ASln()
		elif dialog==5:
			advancedsettings('shield')
			tools.ASln()
		elif dialog==6:
			advancedsettings('remove')
			xbmcgui.Dialog().ok(ADDON_NAME, 'Advanced Settings Removed')
	elif url =="ADS2":
		dialog = xbmcgui.Dialog().select('Select Your Device Or Closest To', ['Open AutoConfig','Fire TV Stick ','Fire TV','1GB Ram or Lower','2GB Ram or Higher','Nvidia Shield'])
		if dialog==0:
			advancedsettings('auto')
			tools.ASln()
		elif dialog==1:
			advancedsettings('stick')
			tools.ASln()
		elif dialog==2:
			advancedsettings('firetv')
			tools.ASln()
		elif dialog==3:
			advancedsettings('lessthan')
			tools.ASln()
		elif dialog==4:
			advancedsettings('morethan')
			tools.ASln()
		elif dialog==5:
			advancedsettings('shield')
			tools.ASln()
	elif url =="tv":
		dialog = xbmcgui.Dialog().yesno(ADDON_NAME,'Would You like us to Setup the TV Guide for You?')
		if dialog:
			pvrsetup()
			xbmcgui.Dialog().ok(ADDON_NAME, 'PVR Integration Complete, Restart Kodi For Changes To Take Effect')
	elif url =="Itv":
			xbmc.executebuiltin('InstallAddon(pvr.iptvsimple)')
	elif url =="ST":
		speedtest.speedtest()
	elif url =="META":
		if 'ON' in description:
			xbmcaddon.Addon().setSetting('meta','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('meta','true')
			xbmc.executebuiltin('Container.Refresh')
	elif url =="XXX":
		if 'ON' in description:
			pas = tools.keypopup('Enter Adult Password:')
			if pas ==control.setting('xxx_pw'):
				xbmcaddon.Addon().setSetting('hidexxx','false')
				xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('hidexxx','true')
			xbmc.executebuiltin('Container.Refresh')		
	elif url =="LO":
		xbmcaddon.Addon().setSetting('DNS','')
		xbmcaddon.Addon().setSetting('Username','')
		xbmcaddon.Addon().setSetting('Password','')
		xbmc.executebuiltin('XBMC.ActivateWindow(Videos,addons://sources/video/)')
		xbmc.executebuiltin('Container.Refresh')
	elif url =="UPDATE":
		if 'ON' in description:
			xbmcaddon.Addon().setSetting('update','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('update','true')
			xbmc.executebuiltin('Container.Refresh')
	elif url == "RefM3U":
		DP.create(ADDON_NAME, "Please Wait")
		tools.gen_m3u(panel_api, M3U_PATH)
	elif url == "TEST":
		tester()

def adult_set():
	dialog = DIALOG.yesno(ADDON_NAME,'Would you like to hide the Adult Menu? \nYou can always change this in settings later on.')
	if dialog:
		control.setSetting('xxx_pwset','true')
		pass
	else:
		control.setSetting('xxx_pwset','false')
		pass
	dialog = DIALOG.yesno(ADDON_NAME,'Would you like to Password Protect Adult Content? \nYou can always change this in settings later on.')
	if dialog:
		control.setSetting('xxx_pwset','true')
		adultpw = tools.keypopup('Enter Password')
		control.setSetting('xxx_pw',adultpw)
	else:
		control.setSetting('xxx_pwset','false')
		pass

def advancedsettings(device):
	if device == 'stick':
		file = open(os.path.join(advanced_settings, 'stick.xml'))
	elif device =='auto':
		popup.autoConfigQ()
	elif device == 'firetv':
		file = open(os.path.join(advanced_settings, 'firetv.xml'))
	elif device == 'lessthan':
		file = open(os.path.join(advanced_settings, 'lessthan1GB.xml'))
	elif device == 'morethan':
		file = open(os.path.join(advanced_settings, 'morethan1GB.xml'))
	elif device == 'shield':
		file = open(os.path.join(advanced_settings, 'shield.xml'))
	elif device == 'remove':
		os.remove(ADVANCED)
	try:
		read = file.read()
		f = open(ADVANCED, mode='w+')
		f.write(read)
		f.close()
	except:
		pass

def accountinfo():
	try:
		response = tools.OPEN_URL(panel_api)
		parse = json.loads(response)
		
		# Verificar se a resposta contém as informações necessárias
		if 'user_info' not in parse:
			xbmcgui.Dialog().notification('VortexPlay', 'Erro ao obter informações da conta', xbmcgui.NOTIFICATION_ERROR, 3000)
			return
		
		user_info = parse['user_info']
		
		# Processar data de expiração
		expiry = user_info.get('exp_date', '')
		if expiry and expiry != "":
			try:
				expiry = datetime.fromtimestamp(int(expiry)).strftime('%d/%m/%Y - %H:%M')
				expreg = re.compile('^(.*?)/(.*?)/(.*?)$',re.DOTALL).findall(expiry)
				for day,month,year in expreg:
					month = tools.MonthNumToName(month)
					year = re.sub(' -.*?$','',year)
					expiry = month+' '+day+' - '+year
			except:
				expiry = 'Data inválida'
		else:
			expiry = 'Ilimitado'
		
		# Exibir informações da conta
		tools.addDir('[B][COLOR white]USUÁRIO:[/COLOR][/B] '+str(user_info.get('username', 'N/A')),'','',icon,background,'')
		tools.addDir('[B][COLOR white]SENHA:[/COLOR][/B] '+str(user_info.get('password', 'N/A')),'','',icon,background,'')
		tools.addDir('[B][COLOR white]DATA DE EXPIRAÇÃO:[/COLOR][/B] '+str(expiry),'','',icon,background,'')
		tools.addDir('[B][COLOR white]STATUS DA CONTA:[/COLOR][/B] '+str(user_info.get('status', 'N/A')),'','',icon,background,'')
		tools.addDir('[B][COLOR white]CONEXÕES ATUAIS:[/COLOR][/B] '+str(user_info.get('active_cons', 'N/A')),'','',icon,background,'')
		tools.addDir('[B][COLOR white]CONEXÕES PERMITIDAS:[/COLOR][/B] '+str(user_info.get('max_connections', 'N/A')),'','',icon,background,'')
		tools.addDir('[B][COLOR white]IP LOCAL:[/COLOR][/B] '+str(tools.getlocalip()),'','',icon,background,'')
		tools.addDir('[B][COLOR white]IP EXTERNO:[/COLOR][/B] '+str(tools.getexternalip()),'','',icon,background,'')
		tools.addDir('[B][COLOR white]VERSÃO DO KODI:[/COLOR][/B] '+str(KODIV),'','',icon,background,'')
		
	except Exception as e:
		tools.log('Erro ao obter informações da conta: ' + str(e))
		xbmcgui.Dialog().notification('VortexPlay', 'Erro ao carregar informações da conta', xbmcgui.NOTIFICATION_ERROR, 3000)

def waitasec(time_to_wait,title,text):
	FTGcd = xbmcgui.DialogProgress()
	ret = FTGcd.create(' '+title)
	secs=0
	percent=0
	increment = int(100 / time_to_wait)
	cancelled = False
	while secs < time_to_wait:
		secs += 1
		percent = increment*secs
		secs_left = str((time_to_wait - secs))
		remaining_display = "Still " + str(secs_left) + "seconds left"
		FTGcd.update(percent,text+'\n'+remaining_display)
		xbmc.sleep(1000)
		if (FTGcd.iscanceled()):
			cancelled = True
			break
	if cancelled == True:
		return False
	else:
		FTGcd.close()
		return False

def tester():
	FTG = ''

def pvrsetup():
	correctPVR()
	tools.killxbmc()
	return

def correctPVR():
	choice = DIALOG.yesno(ADDON_NAME, 'Does your provider allow M3U?')
	if choice:
		m3u_do = 'no'
	else:
		DP.create(ADDON_NAME, "Please Wait")
		tools.gen_m3u(panel_api, M3U_PATH)
		m3u_do = 'yes'
	try:
		addon		  = xbmcaddon.Addon(ADDON_ID)
		dns_text	  = addon.getSetting(id='DNS')
		username_text = addon.getSetting(id='Username')
		password_text = addon.getSetting(id='Password')
		PvrEnable	  = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.demo","enabled":false},"id":1}'
		jsonSetPVR	  = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":true},"id":1}'
		IPTVon		  = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}'
		nulldemo	  = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.demo","enabled":false},"id":1}'
		loginurl	  = dns_text+"/get.php?username=" + username_text + "&password=" + password_text + "&type=m3u_plus&output=ts"
		EPGurl		  = dns_text+"/xmltv.php?username=" + username_text + "&password=" + password_text

		xbmc.executeJSONRPC(PvrEnable)
		xbmc.executeJSONRPC(jsonSetPVR)
		xbmc.executeJSONRPC(IPTVon)
		xbmc.executeJSONRPC(nulldemo)

		FTG = xbmcaddon.Addon('pvr.iptvsimple')
		if m3u_do == 'yes':
			FTG.setSetting(id='m3uPath', value=M3U_PATH)
			FTG.setSetting(id='m3uPathType', value="0")
		else:
			FTG.setSetting(id='m3uUrl', value=loginurl)
		FTG.setSetting(id='epgUrl', value=EPGurl)
		FTG.setSetting(id='m3uCache', value="false")
		FTG.setSetting(id='epgCache', value="false")

		xbmc.executebuiltin("Container.Refresh")
		DIALOG.ok(ADDON_NAME,"PVR Client Updated, Kodi needs to re-launch for changes to take effect, click ok to quit kodi and then please re launch")
		os._exit(1)
	except:
		DIALOG.ok(ADDON_NAME,"PVR Client: Unknown Error or PVR already Set-Up")

def tvguidesetup():
		dialog = DIALOG.yesno(ADDON_NAME,'Would You like '+ADDON_NAME+' to Setup the TV Guide for You?')
		if dialog:
			pvrsetup()
			DIALOG.ok(ADDON_NAME, 'You are all done! \n Restart Kodi For Changes To Take Effect')

def num2day(num):
	if num =="0":
		day = 'monday'
	elif num=="1":
		day = 'tuesday'
	elif num=="2":
		day = 'wednesday'
	elif num=="3":
		day = 'thursday'
	elif num=="4":
		day = 'friday'
	elif num=="5":
		day = 'saturday'
	elif num=="6":
		day = 'sunday'
	return day
	
def extras():
	tools.addDir('TESTE DE VELOCIDADE','ST',10,icon,background,'')
	tools.addDir('LIMPAR CACHE','clearcache',10,icon,background,'')

params=tools.get_params()
url=None
name=None
mode=None
iconimage=None
description=None
query=None
type=None

try:
	url=urllib.parse.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.parse.unquote_plus(params["name"])
except:
	pass
try:
	iconimage=urllib.parse.unquote_plus(params["iconimage"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass
try:
	description=urllib.parse.unquote_plus(params["description"])
except:
	pass
try:
	query=urllib.parse.unquote_plus(params["query"])
except:
	pass
try:
	type=urllib.parse.unquote_plus(params["type"])
except:
	pass

if mode==None or url==None or len(url)<1:
	start('false')

elif mode==1:
	livecategory()
	
elif mode==2:
	Livelist(url)
	
elif mode==3:
	vod(url)
	
elif mode==4:
	stream_video(url)
	
elif mode==5:
	search()
	
elif mode==6:
	accountinfo()
	
elif mode==7:
	tvguide()
	
elif mode==8:
	settingsmenu()
	
elif mode==10:
	addonsettings(url,description)
	
elif mode==11:
	pvrsetup()
	
elif mode==12:
	catchup()

elif mode==13:
	tvarchive(name,description)
	
elif mode==14:
	listcatchup2()
	
elif mode==15:
	ivueint()
	
elif mode==16:
	extras()
	
elif mode==18:
	series_cats(url)

elif mode==25:
	serieslist(url)
	
elif mode==19:
	series_seasons(url)

elif mode==20:
	season_list(url)

elif mode=='start':
	start(signin)

elif mode=='test':
	tester()

xbmcplugin.endOfDirectory(int(sys.argv[1]))