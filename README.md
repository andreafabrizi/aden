# aden

**aden** lets you to grab the RTMP properties from the most popular live TV streaming services.  

It's written in pure python, cross platform and very modular, so anyone can write it's own plugin 
for not natively supported services.

The main difference between this software and **rtmpSnoop** is that **aden** allows you to grab the RTMP properties of a live stream
without playing it. It needs only the page URL where the live channel is published.  
However is important to understand the limits of this program, in fact it works only with the supported
services (see the next paragraph).  

If you are looking for a more powerful and flexible solution, please use **rtmpSnoop**.

## Supported services
At the moment the following services are fully supported:

* LiveFlash (www.liveflash.tv)
* Ucaster (www.ucaster.eu)
* YYCast (www.yycast.com)
* Micast (www.micast.tv)
* Filmon (www.filmon.com)
* LetOn (www.leton.tv)

## Requirements

To run this program you need only **python** (at least 2.7 version) and the **BeautifulSoup** module.  
To install it on a debian/ubuntu system type `apt-get install python-beautifulsoup`.

## Usage

The syntax is quite simple:

```
$python aden.py -h
usage: aden.py [-h] [--out-list | --out-m3u | --out-rtmpdump] [--quiet] URL

aden lets you to grab the RTMP properties from the most popular live TV
streaming services.

positional arguments:
  URL

optional arguments:
  -h, --help      show this help message and exit
  --out-list      Prints the RTMP data as list (Default)
  --out-m3u       Prints the RTMP data as m3u entry
  --out-rtmpdump  Prints the RTMP data as rtmpdump format
  --quiet         Doesn't print anything except the RTMP data
```
For example, to grab the RTMP properties for a live TV channel published on `http://www.test.com/channel1.html`, just run:

```
$python aden.py http://www.test.com/channel1.html
aden v0.2 - The RTMP grabber!
Andrea Fabrizi - andrea.fabrizi@gmail.com

#Loading plugin 'liveFlashTv'... 
#Loading plugin 'ucaster'... 

> Scanning url: http://www.test.com/channel1.html...
> Scanning url: http://www.hiddenstream.com/hiddenframe.html...
> Found matching page for Ucaster.eu: http://www.hiddensream.com/hiddenframe.html

*************************************
Found Ucaster.eu channel: channel1
*************************************
url: rtmp://174.37.222.57/live/channel1?id=12345
app: live
extra: OK
flashVer: WIN 11,7,700,169
pageUrl: http://www.ucaster.eu/embedded/channel1/1/500/380
swfUrl: http://www.ucaster.eu/static/scripts/eplayer.swf
tcUrl: rtmp://174.37.222.57/live
playPath: channel1?id=12345
************************************
```
