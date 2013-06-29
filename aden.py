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
import sys
import argparse
import re
from BeautifulSoup import BeautifulSoup
from lib.adenMod import adenMod
import lib.adenUtils as utils

class aden():

    def __init__(self):

        self.VERSION = "0.2"
        self.moduleList = list()

    """
    This method load all the dynamic modules defined
    in the modules list """
    def loadModules(self):

        #Current path
        cwd = os.path.dirname(os.path.realpath(__file__))

        #Loading modules
        for filename in os.listdir(cwd + "/modules"):
            if filename[-3:] != ".py" or filename in ["__init__.py"]:
                continue
            module = filename[:-3]
            self.out("#Loading module '%s'... " % module)
            __import__("modules.%s" % module, globals={}, locals={}, fromlist=[], level=-1)

        #Adding modules to the list
        for cls in adenMod.__subclasses__():
            self.moduleList.append(cls)

        self.out("")

    """
    Starting from the provided url, this method looks from known embedded
    players, in the current page and in the sub frames/iframes.
    If a known players is found, the RTMP data will be grabbed and printed. """
    def scan(self, url, referer = ""):
        self.out("> Scanning url: %s..." % url)

        try:

            #Getting page content
            pagedata = utils.getUrlData(url, referer)

        except Exception as e:
            self.out("*** Error requesting %s: %s" % (url, e))
            return False

        #Looking for embedded player in the page
        player_found = self.grab(url, pagedata)

        #If the player was not found in the current page, let's start to
        #scan internal iframes
        if not player_found:
            soup = BeautifulSoup(pagedata)
            for iframe in soup.findAll(["iframe", "frame"]):
                if iframe.has_key("src") and iframe["src"] and re.search("^http[s]*://.*", iframe["src"], re.IGNORECASE):
                    return self.scan(iframe["src"], url)
        else:
            return True

    """
    Running all modules against the url
    This methon takes two arguments to reuse the data fetched with the
    last request """
    def grab (self, url, pagedata):
        player_found = False

        for tvmod in self.moduleList:
            try:
                mod = tvmod()
                mod.initialize(quiet=self.quiet)
                if mod.probe(pagedata):
                    self.out("> %s player found!" % mod.name)
                    if mod.scan(url) == True:
                        player_found = True
                        self.print_results(mod)
                    else:
                        self.out("*** Error grabbing player properties!\n")
                        sys.exit(1)

            except NameError as e:
                self.out("*** Error running module %s: %s\n" % (mod.name, e))
                sys.exit(1)

        return player_found

    """
    Prints out the results """
    def print_results(self, mod):
        if (self.out_mode == "list"):
            mod.printRTMPdata()
        elif (self.out_mode == "m3u"):
            mod.printM3Uentry()
        elif (self.out_mode == "rtmpdump"):
            mod.printRTMPDump()

    """
    Set some object properties """
    def setProperties (self, quiet=False, out_mode=None):
        if not out_mode:
            out_mode="list"
        self.quiet = quiet
        self.out_mode = out_mode

    """
    Output function wrapper """
    def out(self, str):
        if self.quiet == False:
            print str

"""
Setting up the argparse and usage """
def setupArgParser():

    parser = argparse.ArgumentParser(description="aden lets you to grab the RTMP properties from the most popular live TV streaming services.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--out-list", action='store_const', const="list", dest="out_mode", help="Prints the RTMP data as list (Default)")
    group.add_argument("--out-m3u", action='store_const', const="m3u", dest="out_mode", help="Prints the RTMP data as m3u entry")
    group.add_argument("--out-rtmpdump", action='store_const', const="rtmpdump", dest="out_mode", help="Prints the RTMP data as rtmpdump format")
    parser.add_argument("--quiet", action="store_true", help="Doesn't print anything except the RTMP data")
    parser.add_argument("URL", action="store")

    args = parser.parse_args()

    return args

##### MAIN
if __name__ == '__main__':

    args = setupArgParser()

    adn = aden()

    if not args.quiet:
        print "aden v%s - The RTMP grabber!" % adn.VERSION
        print "Andrea Fabrizi - andrea.fabrizi@gmail.com\n"

    adn.setProperties(quiet=args.quiet, out_mode=args.out_mode)
    adn.loadModules()

    try:
        ret = adn.scan(args.URL)
    except KeyboardInterrupt:
        print "Bye :)"
        sys.exit(1)
    
    if not ret:
        if not args.quiet:
            print "\nNothing found :("
        sys.exit(1)

    sys.exit(0)
