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
        self.name = "YYCast.com"
        self.description = "YYCast.com aden module"

        """
        The probing strings don't have to be too accurate. In fact they are used only to filter out
        the useless pages and reduce the load for the more accurate function 'scan' """
        self.probeMatches = ["http://www.yycast.com/javascript/embedPlayer.js", "v_width", "v_height", "fid"]

    def scan(self, url):

        self.domain = utils.getDomainFromUrl(url)

        #Getting the channel id from the script
        m = re.search(".*fid=\"([^\"]*)\";v_width=([0-9]*);v_height=([0-9]*).*", utils.trimData(self.pageData))
        if m:
            channel_name = m.group(1)
            width = m.group(2)
            height = m.group(3)
        else:
            return None

        #Building yycast url
        yycast_url = "http://%s/embed.php?fileid=%s&vw=%s&vh=%s" % (self.domain, channel_name, width, height)

        #Requesting yycast url, with a fake Referer
        data = utils.getUrlData(yycast_url, url)

        #Reading FlashVars from the script
        m = re.search(".*'streamer':'([^']*)',.*", utils.trimData(data))
        if m:
            streamer = m.group(1)
        else:
            return None

        """
        Sometimes the streamer value is the RTMP server and sometimes is a load balancer (rtmp://live.yycast.com:1935/lb/).
        I don't know exactly why...
        The problem is that, at this time, there is no way to get the real server IP in the case that the RTMP load balancer
        address is given.
        So, if I get the loadbalancer address I'm returning an hard-coded yycast server address. """
        if streamer.find("/lb/") >= 0:
            streamer = "rtmp://79.142.66.14/live/"

        #Saving the RTMP properties
        self.channel_name = channel_name
        self.RTMP["url"] = "%s_definst_/%s" % (streamer, channel_name)
        self.RTMP["app"] = "live/_definst_"
        self.RTMP["pageUrl"] = yycast_url
        self.RTMP["swfUrl"] = "http://%s/playerskin/player.swf" % self.domain
        self.RTMP["tcUrl"] = "%s_definst_" % (streamer)
        self.RTMP["playPath"] = channel_name

        return True
