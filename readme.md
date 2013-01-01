Framedata Bot
=============

Author: Justin Woo
Date: 1-Jan 2013

This script allows the user to run a simple IRC bot that listens for messages preceded by ']' to retrieve framedata information.

```
Usage:
fdata_bot.py [-h] SERVER NICK CHANNEL

-h, --help:     shows help message
SERVER          address of server to connect to
NICK            nickname to give to the bot
CHANNEL         channel to join on server
```

Setup will require the generation of data from web pages downloaded from Shoryuken. Some hard coded tricks are used to do this based on the title given from the webpages.

![setup](http://i.imgur.com/0Pmjs.png)


rawextract.py usage:
```
Usage:
rawextract.py [-h] DIRECTORY OUTPUT

-h, --help:   shows help message
DIRECTORY  		directory where html files are stored
OUTPUT  			where to store output .csv files
```

Future work:
If anyone wishes to continue work and talk to me about it, just e-mail me.
