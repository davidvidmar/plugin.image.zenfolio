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

import zenfolio_common
import PyZenfolio as z

import pprint

class Main(zenfolio_common.Main):

    def __init__(self, mode):

        zenfolio_common.Main.__init__(self)
        self.process(mode)

    def process(self, mode):

        page = self.id

        if (page > 0):
            self.AddDir(self.url, "< Previous Page <", mode, int(page)-1)

        if mode == "pph":
            ps = z.GetPopularPhotos(page, 20, self.auth)
            pprint.pprint(ps)
            self.ProcessPhotoArray(ps)


        if mode == "pps":
            ps = z.GetPopularSets("Gallery", page, 20, self.auth)
            pprint.pprint(ps)
            self.ProcessPhotosetArray(ps)


        if mode == "rph":
            ps = z.GetRecentPhotos(page, 20, self.auth)
            pprint.pprint(ps)
            self.ProcessPhotoArray(ps)


        if mode == "rps":
            ps = z.GetRecentSets("Gallery", page, 20, self.auth)
            pprint.pprint(ps)
            self.ProcessPhotosetArray(ps)


        self.AddDir(self.url, "> Next Page >", mode, int(page)+1)

        self.EndAddDir(addEmptySort = True)