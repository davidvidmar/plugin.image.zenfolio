#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      David
#
# Created:     09.01.2011
# Copyright:   (c) David 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import cgi
import sys

import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

import PyZenfolio as z

import pprint

DEBUG = True

class Main:

    __settings__ = xbmcaddon.Addon(id='plugin.image.zenfolio')
    __language__ = __settings__.getLocalizedString

    username = __settings__.getSetting("username")
    thumb_size = int(__settings__.getSetting("thumb_size")) + 1
    image_size = int(__settings__.getSetting("image_size")) + 1

    def __init__(self):

        if DEBUG:
            print "***** ZENFOLIO *****"
            #print "*** Settings"
            #print "Username = " + self.username
            #print "Thumb Size = " + str(self.thumb_size)
            #print "Image Size = " + str(self.image_size)

        self.ParseParams()
        self.Authenticate()

    def Authenticate(self):

        print "Authenticating..."

        password = self.__settings__.getSetting("password")

        auth_challenge = z.GetChallenge(self.username)
        self.auth = z.Authenticate(auth_challenge, password)

        #print "auth = " + auth

    def ParseParams(self):

        self.url = sys.argv[0]
        parms = sys.argv[2]

        if DEBUG:
            print "*** Parameters"
            print "URL = " + self.url
            print "Parms = " + parms
            #print "Argv 1 = " + sys.argv[1]

        if len(parms) > 2:
            parms = parms[1:]

        parm = cgi.parse_qs(parms)

        if "id" in parm:
            self.id = parm["id"][0]

            if DEBUG:
                print "ID = " + self.id
        else:
            self.id = 0


    def ProcessGroup(self, g):

        if DEBUG:
            print "*** Processing Group"

        for e in g["Elements"]:
            print e['$type']
            if e["$type"] == "Group":
                self.AddDirectoryGroup(e)
            elif e["$type"] == "PhotoSet":
                self.AddDirectoryPhotoset(e)

        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_NONE)
        self.EndAddDir()

    def ProcessPhotosetArray(self, a):

        for e in a:
            self.AddDirectoryPhotoset(e)

        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_NONE)


    def ProcessPhotoArray(self, a):

        for e in a:
            self.AddDirectoryPhoto(e)

        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_NONE)


    def AddDirectoryGroup(self, e):

        li = xbmcgui.ListItem(e["Title"].encode('utf-8'))
        u = self.url + "?mode=g&id=" + str(e["Id"])

        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=li, isFolder=True)


    def AddDirectoryPhotoset(self, e):

        if e["TitlePhoto"] is not None:
            thumbUrl = "http://%s%s-%s.jpg?token=%s" % (e["TitlePhoto"]["UrlHost"], e["TitlePhoto"]["UrlCore"], self.thumb_size, self.auth)
        else:
            thumbUrl = None

        li = xbmcgui.ListItem(e["Title"].encode('utf-8') + " (" + str(e["PhotoCount"]) + " photos)", thumbnailImage = thumbUrl)
        u = self.url + "?mode=ps&id=" + str(e["Id"])

        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=li, isFolder=True)

    def ProcessPhotoSet(self, ps):

        if DEBUG:
            print "*** Photoset"

        for p in ps["Photos"]:
            self.AddDirectoryPhoto(p)

        #TODO: sorting
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_NONE)

        self.EndAddDir()


    def AddDirectoryPhoto(self, p):

        thumbUrl = "http://%s%s-%s.jpg?token=%s" % (p["UrlHost"], p["UrlCore"], self.thumb_size, self.auth)
        picUrl = "http://%s%s-%s.jpg?token=%s" % (p["UrlHost"], p["UrlCore"], self.image_size, self.auth)

        if p["Caption"] is not None:
            title = p["Caption"].encode('utf-8')
        elif p["Title"] is not None:
            title = p["Title"].encode('utf-8')
        elif p["FileName"] is not None:
            title = p["FileName"].encode('utf-8')
        else:
            title = p["UrlCore"]

        if DEBUG:
            print "Pic URL = " + picUrl
            print "Thumb URL = " + thumbUrl
            print "Title = " + title

        li = xbmcgui.ListItem(title, thumbnailImage = thumbUrl)

        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=picUrl, listitem=li)


    def AddDir(self, url, caption, mode, id=None):


        li = xbmcgui.ListItem(caption)
        u = url + "?mode=" + mode

        if id is not None:
            u = u + "&id=" + str(id)

        print "adddir: " + u

        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=li, isFolder=True)


    def EndAddDir(self, addEmptySort = False):

        if addEmptySort:
            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_NONE)

        xbmcplugin.endOfDirectory(int(sys.argv[1]))