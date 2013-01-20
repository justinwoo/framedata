Framedata Bot
=============

Author: Justin Woo
Date: 1-Jan 2013

This script allows the user to run a simple IRC bot that listens for messages preceded by ']' to retrieve framedata information.

![example](http://i.imgur.com/E8SMcs0.png)

```
Usage:
fdatabot.py [-h] SERVER NICK CHANNEL

-h, --help: 	shows help message
CONFIG 			location of the configuration file
```

The configuration file is formatted as such:

```
data: ./out
aliases: ./aliastable.dat
irc.slashnet.org,6667,testerszxc,#kigurumi
```
> Note: you append extra [server],[port],[nick],[[channels]] entries to add more connections
> Please append channels in a [#chan1, #chan2, #chan3, ...] format to add extra channel joins

In this version, the horrible rawextract.py script has been replaced with the much better SRKSF4scraper.py. Setup will now require the use of BeautifulSoup in the grabbing of HTML data from the SRK Wiki directly. Lots of the old voodoo code was left in to minimize development time.

![setup](http://i.imgur.com/BjuJwcv.png)
> yes, oni and gen's tables are all messed up in the wiki. will i be providing a fix for them? no. srk should fix their damn tables.


SRKSF4scraper.py usage:
```
Usage:
SRKSF4scraper.py [-h] OUTPUT

-h, --help:			shows help message
OUTPUT  			where to store output .csv files
```

Future work:
If anyone wishes to continue work and talk to me about it, just e-mail me.

To be done:
Find bugs, fix them.
