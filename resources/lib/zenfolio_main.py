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

class Main(zenfolio_common.Main):

    def __init__(self):

        #zenfolio_common.Main.__init__(self)
        self.ParseParams();
        self.process()


    def process(self):

        print "**** MAIN Menu *****"

        self.AddDir(self.url, "All Photos", "root")

        self.AddDir(self.url, "Recent Photos", "rph")
        self.AddDir(self.url, "Recent Photosets", "rps")

        self.AddDir(self.url, "Popular Photos", "pph")
        self.AddDir(self.url, "Popular Photosets", "pps")

        self.AddDir(self.url, "Browse by Category (soon)", "")
        self.AddDir(self.url, "Search (soon)", "")

        self.EndAddDir(addEmptySort=True)