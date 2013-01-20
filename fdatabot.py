#! /usr/bin/env python
# Justin Woo <moomoowoo@gmail.com>
# ver: dev

# usage: fdatabot.py [config filepath]

# optional:
#   -h, --help			help
# required:
#   [config filepath]	location of the configuration file

# purpose:
# looks up frame data in local character.csv files and prints it out based on a command in the "]character move" format.

import argparse, sys, os
import socket
import fdataget
from multiprocessing import Process, Lock

class chatbot:
	def __init__(self, server, port, nick, fdatapath, aliasespath, lock):
		self.engine = fdataget.fdataengine(fdatapath, aliasespath, lock)
		self.s = socket.socket()
		self.s.connect((server, int(port)))
		self.sendOut('NICK %s\n' % (nick))
		self.sendOut('USER %s %s + bla :%s\n' % (nick, server, nick))
	
	def sendOut(self, outbound):
		print outbound
		self.s.send(outbound)
	
	def getSocketResponse(self):
		return self.s.recv(500).rstrip()
	
	def joinChannel(self, channel):
		self.sendOut('JOIN %s\n' % (channel))
	
	def sendPRIVMSG(self, channel, messagebody):
		self.sendOut('PRIVMSG %s :%s\n' % (channel, messagebody))
	
	def sendPONG(self, line):
		# :PING (whatever crap)
		self.sendOut('PONG %s\n' % (line.split(' ')[1]))
	
	def parsePRIVMSG(self, line):
		outmsg = self.engine.parsePRIVMSG(line)
		print outmsg
		if outmsg == None:
			return
		outchan = line.lower().split(' ')[2]
		self.sendPRIVMSG(outchan, outmsg)

		# line = line.lower().split(' ')
		# outchan = line[2]
		# msgin = line[3:]
		# self.sendPRIVMSG(outchan, 'I heard you say "%s"' % ' '.join(msgin)[1:])


def main(lock, config, fdatapath, aliasespath):
	line = config.rstrip().split(',') 
	server = line[0]
	port = line[1]
	nick = line[2]
	channels = line[3:]
	bot = chatbot(server, port, nick, fdatapath, aliasespath, lock)

	while 1:
		line = bot.getSocketResponse().rstrip()
		if line != '':
			print line
		if line.find('PING') != -1:
			bot.sendPONG(line.rstrip())
		elif line.find('PRIVMSG') != -1:
			bot.parsePRIVMSG(line.rstrip())
		elif line.find('elcome') != -1:
			for channel in channels:
				bot.joinChannel(channel)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('configfile', help = 'location of the configuration file')
	args = parser.parse_args()
	lock = Lock()

	# configfile is .csv format: server, port, nick, channel(s)
	if os.path.exists(args.configfile):
		flines = open(args.configfile, 'r').readlines()
		for line in flines[2:]:
			if line.rstrip() != '':
				Process(target = main, args = (lock, line, flines[0].split('data: ')[1].rstrip(), flines[1].split('aliases: ')[1].rstrip())).start()
		