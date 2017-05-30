import os, sys
from urlparse import parse_qsl
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib

# Get the plugin url in plugin:// notation.
__url__ = sys.argv[0]
# Get the plugin handle as an integer number.
__handle__ = int(sys.argv[1])
_addon_ = xbmcaddon.Addon('plugin.video.my-testing-addon')
home = _addon_.getAddonInfo('path')
fanart = xbmc.translatePath( os.path.join( home, 'resources/data/fanart.jpg' ) )
## Get all setting value by ADDON.getSetting("SETTING_ID")
ADDON  = xbmcaddon.Addon()

VIDEOS = {'Animals': [{'name': 'Crab',
                       'thumb': 'http://www.vidsplay.com/vids/crab.jpg',
                       'video': 'http://www.vidsplay.com/vids/crab.mp4',
                       'genre': 'Animals'},
                      {'name': 'Alligator',
                       'thumb': 'http://www.vidsplay.com/vids/alligator.jpg',
                       'video': 'http://www.vidsplay.com/vids/alligator.mp4',
                       'genre': 'Animals'},
                      {'name': 'Turtle',
                       'thumb': 'http://www.vidsplay.com/vids/turtle.jpg',
                       'video': 'http://www.vidsplay.com/vids/turtle.mp4',
                       'genre': 'Animals'}
                      ],
            'Cars': [{'name': 'Postal Truck',
                      'thumb': 'http://www.vidsplay.com/vids/us_postal.jpg',
                      'video': 'http://www.vidsplay.com/vids/us_postal.mp4',
                      'genre': 'Cars'},
                     {'name': 'Traffic',
                      'thumb': 'http://www.vidsplay.com/vids/traffic1.jpg',
                      'video': 'http://www.vidsplay.com/vids/traffic1.avi',
                      'genre': 'Cars'},
                     {'name': 'Traffic Arrows',
                      'thumb': 'http://www.vidsplay.com/vids/traffic_arrows.jpg',
                      'video': 'http://www.vidsplay.com/vids/traffic_arrows.mp4',
                      'genre': 'Cars'}
                     ],
            'Food': [{'name': 'Chicken',
                      'thumb': 'http://www.vidsplay.com/vids/chicken.jpg',
                      'video': 'http://www.vidsplay.com/vids/bbqchicken.mp4',
                      'genre': 'Food'},
                     {'name': 'Hamburger',
                      'thumb': 'http://www.vidsplay.com/vids/hamburger.jpg',
                      'video': 'http://www.vidsplay.com/vids/hamburger.mp4',
                      'genre': 'Food'},
                     {'name': 'Pizza',
                      'thumb': 'http://www.vidsplay.com/vids/pizza.jpg',
                      'video': 'http://www.vidsplay.com/vids/pizza.mp4',
                      'genre': 'Food'}
                     ]}

def log(txt):
    xbmc.log("#DEbuger----------"+str(txt))

def get_categories():
    """
    Get the list of video categories.
    Here you can insert some parsing code that retrieves
    the list of video categories (e.g. 'Movies', 'TV-shows', 'Documentaries' etc.)
    from some site or server.
    :return: list
    """
    return VIDEOS.keys()
def get_videos(category):
    """
    Get the list of videofiles/streams.
    Here you can insert some parsing code that retrieves
    the list of videostreams in a given category from some site or server.
    :param category: str
    :return: list
    """
    return VIDEOS[category]
def list_categories():
    """
    Create the list of video categories in the Kodi interface.
    :return: None
    """
    # Get video categories

    categories = get_categories()
    # Create a list for our items.
    listing = []
    # Iterate through categories
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category, thumbnailImage=VIDEOS[category][0]['thumb'])
        # Set a fanart image for the list item.
        # Here we use the same image as the thumbnail for simplicity's sake.
        # list_item.setProperty('fanart_image', VIDEOS[category][0]['thumb'])
        list_item.setProperty('fanart_image', fanart)
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
        list_item.setInfo('video', {'title': category, 'genre': category})
        # Create a URL for the plugin recursive callback.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = '{0}?action=listing&category={1}'.format(__url__, category)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the listing as a 3-element tuple.
        listing.append((url, list_item, is_folder))
    # Add our listing to Kodi.
    # Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
    # instead of adding one by ove via addDirectoryItem.
    xbmcplugin.addDirectoryItems(__handle__, listing, len(listing))
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(__handle__)

def list_videos(category):
    """
    Create the list of playable videos in the Kodi interface.
    :param category: str
    :return: None
    """
    # Get the list of videos in the category.
    videos = get_videos(category)
    # Create a list for our items.
    listing = []
    # Iterate through videos.
    for video in videos:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=video['name'], thumbnailImage=video['thumb'])
        # Set a fanart image for the list item.
        # Here we use the same image as the thumbnail for simplicity's sake.
        list_item.setProperty('fanart_image', video['thumb'])
        # Set additional info for the list item.
        list_item.setInfo('video', {'title': video['name'], 'genre': video['genre']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for the plugin recursive callback.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/vids/crab.mp4
        url = '{0}?action=play&video={1}'.format(__url__, video['video'])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the listing as a 3-element tuple.
        listing.append((url, list_item, is_folder))
    # Add our listing to Kodi.
    # Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
    # instead of adding one by ove via addDirectoryItem.
    xbmcplugin.addDirectoryItems(__handle__, listing, len(listing))
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(__handle__)

def play_video(path):
    """
    Play a video by the provided path.
    :param path: str
    :return: None
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(__handle__, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring
    :param paramstring:
    :return:
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring[1:]))
    # Check the parameters passed to the plugin
    name = ADDON.getSetting("playername")
    password = ADDON.getSetting("playerpass")
    if name =="MYUSER" and password=="PASSWORD":
        if params:
            if params['action'] == 'listing':
                # Display the list of videos in a provided category.
                list_videos(params['category'])
            elif params['action'] == 'play':
                # Play a video from a provided URL.
                play_video(params['video'])
        else:
            # If the plugin is called from Kodi UI without any parameters,
            # display the list of video categories
            list_categories()

    else:
        dialog = xbmcgui.Dialog()
        dialog.ok("Setting", "Please enter your trial account username: MYUSER, and password: PASSWORD in general setting tab.")
        ADDON.OpenSettings("login.required")

if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    router(sys.argv[2])

# try: Emulating = xbmcgui.Emulating
# except: Emulating = False
# #get actioncodes from keymap.xml
# ACTION_PREVIOUS_MENU = 10
# class MyClass(xbmcgui.Window):
#     def __init__(self):
#         if Emulating: xbmcgui.Window.__init__(self)
#         self.addControl(xbmcgui.ControlImage(0,0,720,480, "Q:\\scripts\\Tutorial\\background.gif"))
#         self.strActionInfo = xbmcgui.ControlLabel(100, 200, 200, 200, "", "font13", "0xFFFF00FF")
#         self.addControl(self.strActionInfo)
#         self.strActionInfo.setLabel("Push BACK to quit.")
#         # Make all the buttons
#         self.button0 = xbmcgui.ControlButton(250, 100, 200, 60, "Download", "0x5c5c5c")
#         self.addControl(self.button0)
#         self.button1 = xbmcgui.ControlButton(250, 250, 220, 60, "2. Push Me!")
#         self.addControl(self.button1)
#         self.button2 = xbmcgui.ControlButton(450, 250, 220, 60, "3. Push Me!")
#         self.addControl(self.button2)
#         self.button3 = xbmcgui.ControlButton(55,23,145,60, "Quit")
#         self.addControl(self.button3)
#
#         self.setFocus(self.button0)
#         self.button0.controlLeft(self.button1)
#         self.button1.controlUp(self.button0)
#         self.button1.controlRight(self.button2)
#         self.button2.controlLeft(self.button1)
#         self.button3.controlLeft(self.button3)
#     def onAction(self, action):
#         if action == ACTION_PREVIOUS_MENU:
#             self.close()
#
#
#     def onControl(self, control):
#         if control == self.button0:
#             dialog = xbmcgui.Dialog()
#             if dialog.yesno("Message", "Do you want to download?"):
#                 webfile = "http://www.google.com/images/logo.gif"
#                 localfile = "Q:\\scripts\\logo.gif"
#                 self.downloadURL(webfile,localfile)
#             else:
#                 self.message("Download denied")
#         if control == self.button1:
#             self.message("You pushed the second button.")
#         if control == self.button2:
#             self.message("You pushed the third button.")
#         if control == self.button3:
#             self.close()
#     def downloadURL(self,source, destination):
#         try:
#             loc = urllib.URLopener()
#             loc.retrieve(source, destination)
#             self.message("Download successful!")
#         except:
#             self.message("Download failed. Check your internet connection and try again later.")
#
#     def message(self, messageText):
#         dialog = xbmcgui.Dialog()
#         dialog.ok(" My message title", messageText)
# mydisplay = MyClass()
# mydisplay.doModal()
# del mydisplay
