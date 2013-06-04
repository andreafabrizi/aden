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
import re
import urllib2
from lib.adenMod import adenMod
import lib.adenUtils as utils

class yycast(adenMod):

    def __init__(self):
        self.name = "Micast.tv"
        self.description = "Micast.tv aden module"

        """
        The probing strings don't have to be too accurate. In fact they are used only to filter out
        the useless pages and reduce the load for the more accurate function 'scan' """
        self.probeMatches = ["micast.tv", "streamer=", "flashvars=", "<embed"]

    def scan(self, url):

        self.domain = utils.getDomainFromUrl(url)

        #Getting the channel name from the embed tag
        m = re.search(".*flashvars=\".*file=([^&]*).*streamer=([^&]*).*src=\"([^\"]*)\".*", self.pageData)
        if m:
            channel_name = m.group(1)
            streamer = m.group(2)
            swfUrl = m.group(3)
        else:
            return None

        #Getting app
        m = re.search("^rtmp://[^/]*/(.*)", streamer)
        if not m:
            return None

        app = m.group(1)

        #Saving the RTMP properties
        self.channel_name = channel_name
        self.RTMP["url"] = streamer
        self.RTMP["app"] = app
        self.RTMP["pageUrl"] = url
        self.RTMP["swfUrl"] = swfUrl
        self.RTMP["tcUrl"] = streamer
        self.RTMP["playPath"] = channel_name

        return True
