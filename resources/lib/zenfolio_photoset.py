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

        zenfolio_common.Main.__init__(self)
        self.process()

    def process(self):

        ps = z.LoadPhotoSet(self.id, self.auth)
        self.ProcessPhotoSet(ps)
