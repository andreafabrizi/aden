#!/usr/bin/env python
#
# Copyright (C) 2013 Andrea Fabrizi <andrea.fabrizi@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; either version 3 of
# the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA
#
import os
import urllib2
import lib.adenUtils as utils

class adenMod(object):

    def __init__(self):
        raise NotImplementedError

    def initialize(self, quiet=False):
        self.pageData = None
        self.quiet = quiet
        self.RTMP = dict()
        self.RTMP["flashVer"] = "WIN 11,7,700,169"

    """
    This is the only one method that needs to be implemented
    from each service module """
    def scan(self, url):
        raise NotImplementedError

    """
    This method looks for known strings in each page parsed.
    If all the strings are matched, the page is 'eligible' for the scanning """
    def probe(self, pagedata):
        self.pageData = pagedata
        for p in self.probeMatches:
            if (self.pageData.find(p) < 0):
                return False
        return True

    """
    Prints out the RTMP properties using a simple list mode """
    def printRTMPdata(self):

        self.printOutHeader()

        for key in ["url", "app", "pageUrl", "swfUrl", "tcUrl", "playPath", "flashVer", "extra"]:
            if self.RTMP.has_key(key):
                print "%s: %s" % (key, self.RTMP[key])

        self.printOutFooter()

    """
    Prints out the RTMP properties using the m3u format """
    def printM3Uentry(self):

        self.printOutHeader()
        print "#EXTINF:0,1, %s Channel" % self.name

        line = "%s " % self.RTMP["url"]

        for key in ["app", "pageUrl", "swfUrl", "tcUrl", "playPath"]:
            if (self.RTMP.has_key(key)):
                line += "%s=%s " % (key, self.RTMP[key])

        if (self.RTMP.has_key("extra")):
            line += "conn=S:%s" % self.RTMP["extra"]

        line += " live=1"

        print line
        self.printOutFooter()

    """
    Prints out the RTMP properties using the rtmpdump format """
    def printRTMPDump(self):

        self.printOutHeader()
        line = "rtmpdump -r '%s' " % self.RTMP["url"]

        if (self.RTMP.has_key("app")):
            line += "-a '%s' " % self.RTMP["app"]

        if (self.RTMP.has_key("tcUrl")):
            line += "-t '%s' " % self.RTMP["tcUrl"]

        if (self.RTMP.has_key("playPath")):
            line += "-y '%s' " % self.RTMP["playPath"]

        if (self.RTMP.has_key("swfUrl")):
            line += "-W '%s' " % self.RTMP["swfUrl"]

        if (self.RTMP.has_key("pageUrl")):
            line += "-p '%s' " % self.RTMP["pageUrl"]

        if (self.RTMP.has_key("flashVer")):
            line += "-f '%s' " % self.RTMP["flashVer"]

        if (self.RTMP.has_key("extra")):
            line += "-C S:%s " % self.RTMP["extra"]

        line += "--live -o stream_%s.flv" % utils.trimData(self.channel_name)

        print line
        self.printOutFooter()

    """
    Prints the Header for the result output """
    def printOutHeader(self):

        if not self.quiet:
            print "\n*************************************"
            print "%s channel found: %s" % (self.name, self.channel_name)
            print "*************************************"

    """
    Prints the Footer for the result output """
    def printOutFooter(self):

        if not self.quiet:
            print "*************************************\n"
