import urllib, urllib2, socket, hashlib, time
import xbmc, xbmcgui, xbmcaddon

ADDON        = xbmcaddon.Addon()
ADDONID      = ADDON.getAddonInfo('id')
ADDONVERSION = ADDON.getAddonInfo('version')
LANGUAGE     = ADDON.getLocalizedString

socket.setdefaulttimeout(10)
