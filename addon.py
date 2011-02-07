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

#TODO - latest photosets (my + community)
#TODO - featured photosets (my + community)
#TODO - caption na sliki
#TODO - podatki o sliki + sort
#TODO - error handling

import os
import sys

__plugin__  = "Zenfolio"
__author__  = "David Vidmar <david@vidmar.net>"
__url__     = "http://vidmar.net/"
__date__    = "20 January 2011"
__version__ = "1.0"

if len(sys.argv) >= 2 and "mode=g" in sys.argv[2]:
    print "**** GROUP Mode ****"
    import resources.lib.zenfolio_group as zenfolio;
    zenfolio.Main()

elif len(sys.argv) >= 2 and "mode=ps" in sys.argv[2]:
    print "**** PHOTOSET Mode ****"
    import resources.lib.zenfolio_photoset as zenfolio;
    zenfolio.Main()

elif len(sys.argv) >= 2 and "mode=root" in sys.argv[2]:
    print "**** ROOT Mode ****"
    import resources.lib.zenfolio_root as zenfolio;
    zenfolio.Main()

elif len(sys.argv) >= 2 and "mode=pph" in sys.argv[2]:
    print "**** POPULAR PHOTO Mode ****"
    import resources.lib.zenfolio_poprec as zenfolio;
    zenfolio.Main("pph")

elif len(sys.argv) >= 2 and "mode=pps" in sys.argv[2]:
    print "**** POPULAR PHOTOSET Mode ****"
    import resources.lib.zenfolio_poprec as zenfolio;
    zenfolio.Main("pps")

elif len(sys.argv) >= 2 and "mode=rph" in sys.argv[2]:
    print "**** RECENT PHOTOS Mode ****"
    import resources.lib.zenfolio_poprec as zenfolio;
    zenfolio.Main("rph")

elif len(sys.argv) >= 2 and "mode=rps" in sys.argv[2]:
    print "**** ROOT Mode ****"
    import resources.lib.zenfolio_poprec as zenfolio;
    zenfolio.Main("rsp")

else:
    import resources.lib.zenfolio_main as zenfolio;
    zenfolio.Main()
