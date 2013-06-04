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

class filmon(adenMod):

    def __init__(self):
        self.name = "filmon.com"
        self.description = "filmon.com aden module"
        self.channelInfo_url = "http://www.filmon.com/ajax/getChannelInfo"

        """
        The probing strings don't have to be too accurate. In fact they are used only to filter out
        the useless pages and reduce the load for the more accurate function 'scan' """
        self.probeMatches = ["filmon.com", "http://www.filmon.com/tv/modules/FilmOnTV/flash/expressInstall.swf", "def_server_url"]

    def scan(self, url):

        self.domain = utils.getDomainFromUrl(url)

        #The selected channel must be specified in the page URL
        #e.g. http://www.filmon.com/#CANALE-5
        m = re.search("^http.*://.*/#(.*)$", url)
        if m:
            channel_name = m.group(1).lower()
        else:
            return None

        #Poor checking if the channel name is valid or not... 
        if self.pageData.find(channel_name) < 0:
            return None

        #Getting pageData again, because I need the cookies
        req = urllib2.Request(url)
        req.add_header('User-agent', utils.user_agent)
        usock = urllib2.urlopen(req)
        self.pageData = utils.trimData(usock.read())
        usock.close()

        #Getting cookies
        cookie = usock.info().getheader("Set-Cookie").split(";")[0]

        #Getting channel ID
        #e.g.  alias="canale-5" channel_id = "433"
        m = re.search(".*alias=\"%s\"channel_id=\"([^\"]*)\".*" % channel_name, self.pageData)
        if m:
            channel_id = m.group(1)
        else:
            return None

        #Getting swfUrl
        #e.g {"streamer":"\/tv\/modules\/FilmOnTV\/files\/flashapp\/filmon\/FilmonPlayer.swf?v=13"
        m = re.search(".*\"streamer\":\"([^\"]*)\".*", self.pageData)
        if m:
            swfUrl = "http://" + self.domain + m.group(1).replace("\\","")
        else:
            return None

        #Getting channel info
        postdata = "channel_id=" + channel_id + "&quality=low"
        req = urllib2.Request(self.channelInfo_url, postdata)
        req.add_header("User-agent", utils.user_agent)
        req.add_header("Cookie", cookie)
        req.add_header("X-Requested-With", "XMLHttpRequest")
        usock = urllib2.urlopen(req)
        self.channelInfoData = usock.read()
        usock.close()

        #Getting rtmp url
        #e.g. [{"serverURL":"rtmp:\/\204.107.27.247\/live\/?id=0ad5aac39bb13fbed283f107d459de50e
        m = re.search(".*\[\{\"serverURL\":\"([^\"]*).*", self.channelInfoData)
        if m:
            rtmpUrl = m.group(1).replace("\\","")
        else:
            return None

        #Getting app
        m = re.search("rtmp.*://[^/]*/(.*)", rtmpUrl)
        if m:
            app = m.group(1)
        else:
            return None

        #Getting playPath
        #e.g. "streamName":"433.low.stream"
        m = re.search(".*\"streamName\":\"([^\"]*).*", self.channelInfoData)
        if m:
            playPath = m.group(1).replace("\\","")
        else:
            return None

        #Saving the RTMP properties
        self.channel_name = channel_name
        self.RTMP["url"] = "%s/%s" % (rtmpUrl, playPath)
        self.RTMP["app"] = app
        self.RTMP["pageUrl"] = url
        self.RTMP["swfUrl"] = swfUrl
        self.RTMP["tcUrl"] = rtmpUrl
        self.RTMP["playPath"] = playPath

        return True
