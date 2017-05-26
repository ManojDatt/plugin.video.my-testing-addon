import urllib, urllib2, socket, hashlib, time
import xbmc, xbmcgui, xbmcaddon

ADDON        = xbmcaddon.Addon()
ADDONID      = ADDON.getAddonInfo('id')
ADDONVERSION = ADDON.getAddonInfo('version')
LANGUAGE     = ADDON.getLocalizedString

socket.setdefaulttimeout(10)
def log(txt):
    if isinstance (txt,str):
        txt = txt.decode("utf-8")
    message = u'%s: %s' % (ADDONID, txt)
    xbmc.log(msg=message.encode("utf-8"), level=xbmc.LOGDEBUG)

class Main:
    def __init__( self ):
        self._service_setup()
        while (not self.Monitor.abortRequested()) and (not self.Exit):
            xbmc.sleep(1000)

    def _service_setup( self ):
        self.LibrefmURL           = 'http://turtle.libre.fm/'
        self.ClientId             = 'xbm'
        self.ClientVersion        = '0.2'
        self.ClientProtocol       = '1.2.1'
        self.Exit                 = False
        self.Monitor              = MyMonitor(action = self._get_settings)
        self._get_settings()

    def _get_settings( self ):
        log('#DEBUG# reading settings')
        service    = []
        LibrefmSubmitSongs = ADDON.getSetting('librefmsubmitsongs') == 'true'
        LibrefmSubmitRadio = ADDON.getSetting('librefmsubmitradio') == 'true'
        LibrefmUser        = ADDON.getSetting('librefmuser').lower()
        LibrefmPass        = ADDON.getSetting('librefmpass')
        if (LibrefmSubmitSongs or LibrefmSubmitRadio) and LibrefmUser and LibrefmPass:
            # [service, auth-url, user, pass, submitsongs, submitradio, sessionkey, np-url, submit-url, auth-fail, failurecount, timercounter, timerexpiretime, queue]
            service = ['librefm', self.LibrefmURL, LibrefmUser, LibrefmPass, LibrefmSubmitSongs, LibrefmSubmitRadio, '', '', '', False, 0, 0, 0, []]
            self.Player = MyPlayer(action = self._service_scrobble, service = service)

class MyPlayer(xbmc.Player):
    def __init__( self, *args, **kwargs ):
        xbmc.Player.__init__( self )
        self.action = kwargs['action']
        self.service = kwargs['service']
        self.Audio = False
        self.Count = 0
        log('#DEBUG# Player Class Init')

    def onPlayBackStarted( self ):
        # only do something if we're playing audio
        if self.isPlayingAudio():
            # we need to keep track of this bool for stopped/ended notifications
            self.Audio = True
            # keep track of onPlayBackStarted events http://trac.xbmc.org/ticket/13064
            self.Count += 1
            log('#DEBUG# onPlayBackStarted: %i' % self.Count)
            # tags are not available instantly and we don't what to announce right away as the user might be skipping through the songs
            xbmc.sleep(2000)
            # don't announce if user already skipped to the next track
            if self.Count == 1:
                # reset counter
                self.Count = 0
                # get tags
                tags = self._get_tags()
                # announce song
                self.action(tags, self.service)
            else:
                # multiple onPlayBackStarted events occurred, only act on the last one
                log('#DEBUG# skipping onPlayBackStarted event')
                self.Count -= 1

    def onPlayBackEnded( self ):
        if self.Audio:
            self.Audio = False
            log('#DEBUG# onPlayBackEnded')
            self.action(None, self.service)

    def onPlayBackStopped( self ):
        if self.Audio:
            self.Audio = False
            log('#DEBUG# onPlayBackStopped')
            self.action(None, self.service)

    def _get_tags( self ):
        # get track tags
        artist      = self.getMusicInfoTag().getArtist()
        album       = self.getMusicInfoTag().getAlbum()
        title       = self.getMusicInfoTag().getTitle()
        duration    = str(self.getMusicInfoTag().getDuration())
        # get duration from xbmc.Player if the MusicInfoTag duration is invalid
        if int(duration) <= 0:
            duration = str(int(self.getTotalTime()))
        track       = str(self.getMusicInfoTag().getTrack())
        mbid        = '' # musicbrainz id is not available
        comment     = self.getMusicInfoTag().getComment()
        path        = self.getPlayingFile()
        timestamp   = int(time.time())
        source      = 'P'
        # streaming radio of provides both artistname and songtitle as one label
        if title and not artist:
            try:
                artist = title.split(' - ')[0]
                title = title.split(' - ')[1]
            except:
                pass
        tracktags   = [artist, album, title, duration, track, mbid, comment, path, timestamp, source]
        log('#DEBUG# tracktags: %s' % tracktags)
        return tracktags

class MyMonitor(xbmc.Monitor):
    def __init__( self, *args, **kwargs ):
        xbmc.Monitor.__init__( self )
        self.action = kwargs['action']

    def onSettingsChanged( self ):
        log('#DEBUG# onSettingsChanged')
        self.action()

if ( __name__ == "__main__" ):
    log('script version %s started' % ADDONVERSION)
    Main()
log('script stopped')

def RunScript(self):
    log(self)
