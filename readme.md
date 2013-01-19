Framedata Bot
=============

Author: Justin Woo
Date: 1-Jan 2013

This script allows the user to run a simple IRC bot that listens for messages preceded by ']' to retrieve framedata information.

![example](http://i.imgur.com/8miXF.png)

```
Usage:
fdata_bot.py [-h] SERVER NICK CHANNEL

-h, --help: 	shows help message
SERVER 			address of server to connect to
NICK 			nickname to give to the bot
CHANNEL 		channel to join on server
```

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
Consider multi-pass filtering of selected moves by delimiting elements of the "move" -- i.e. pass the whole move list, build up a list of {key,value} pairs and then filter out non-matching segments from that. That way, for wanted element A, the total moveset could be {A,B,C,D,E,F}, the first pass gets [{A,A.data},{B,B.data},{C,C.data}] and the second pass with the second element would potentially exclusively get [{A,A.data}]. To be done by someone with motivation.

Actually, a better idea would be to take for each word separate scanning an dictionary generations for those. Using the n number of sets, collisions are checked by the keys (move names should be uniquely identifying...) and only KV-pairs common to all sets will be kept and displayed (hopefully bringing us down to just one). This will make it so that order precedence does not alter the results in any way. Maybe. I don't know.

What if we stuffed each server connection into separate processes using multiprocessing? To do: make chatbot into a class so that instances of it can be used in asynchronous functions. -- PROOF OF CONCEPT FINISHED! Now just for the pesky thing that is called "implementation"...

For multiple results, we should prompt the user with a list of options. On answer of simply a number, we should give them the specific one. This will be done with a temporary list holding the latest multiple results.
