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
import re

user_agent = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36"

"""
Simple method to get the html content from a page url """
def getUrlData(url, referer=""):

    req = urllib2.Request(url)
    if referer:
        req.add_header("Referer", referer)
    req.add_header("User-agent", user_agent)
    req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
    usock = urllib2.urlopen(req)
    data = usock.read()
    usock.close()
    return data

"""
This function removes each space and CR/LF from the string.
It's usefull to make error-tolerant the regex parsing """
def trimData(data):
    data = data.replace(" ", "")
    data = data.replace("\n", "");
    data = data.replace("\r", "");
    return data

"""
Returns the domain from the full URL """
def getDomainFromUrl(url):
    m = re.search("http.*//([^/?]*).*", url)
    if m:
        return m.group(1)
    else:
        return None

