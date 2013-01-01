#! /usr/bin/env python
# Justin Woo <moomoowoo@gmail.com>
# ver: dev

# Usage:
# usage: chatbot.py [server] [nick] [channel]

# optional:
#   -h, --help		help
# required:
#   [server]			server to connect to
#   [nickname]		nickname to use
#   [channel]			channel to join

# purpose:
# looks up frame data in local /data/character.csv files and prints it out based on a command in the "]character move" format. 

import argparse, sys, os
import socket

def main(args):
	#generate alias list first
	aliasgen()

	server = args.server
	nickname = args.nickname
	channel = args.channel
	ident = nickname
	port = 6667

	s = socket.socket()
	s.connect((server,port))
	s.send('NICK ' + nickname + '\n')
	s.send('USER ' + ident + ' ' + server + ' bla :' + 'james' + '\n')
	
	while 1:
		line = s.recv(500)

		if line != '':
			print line.rstrip()
		
		if line.find('elcome') != -1:
			outmsg = 'JOIN ' + channel + '\n'
			print outmsg
			s.send(outmsg)
		
		if line.find('PING') != -1:
			line = line.rstrip().split(' ')
			outmsg = 'PONG ' + line[1] + '\n'
			print outmsg
			s.send(outmsg)
		elif line.find('PRIVMSG') != -1:
			line = line.rstrip().lower().split(' ')
			outmsg = parsemsg(line)
			if type(outmsg) is list and outmsg[0] != '':
				for msg in outmsg:
					print msg
					s.send(msg)

def parsemsg(line):
	#:nick!username@host PRIVMSG channel/nick :Message 
	sender = line[0].split('!')[1:]
	msg = line[3:]
	channel = line[2]
	if msg[0][1] is ']' and len(msg) >= 2:
		msgbody = fdata(msg[0][1:], ' '.join(msg[1:]))
		if type(msgbody) is str and msgbody != '':
			outmsg = ['PRIVMSG ' + channel + ' :' + msgbody + '\n']
			return outmsg
		elif type(msgbody) is list:
			outmsgs = []
			for msg in msgbody:
				outmsgs.append('PRIVMSG ' + channel + ' :' + msg + '\n')
			return outmsgs
		else:
			return ''
	else:
		return ''

def fdata(c_name, move):
	#read in our data
	c_name = c_name[1:]
	move = alias(move)
	if c_name.find('help') != -1:
		return 'Usage: ]character move'
	if move == '':
		return ''
	namelist = []
	fname = os.path.join('data',c_name+'.csv')	
	if os.path.exists(fname):
		flines = open(fname,'r').readlines()
		for line in flines:
			if line.find(move) != -1:
				line = line.rstrip().split(',')
				data = []
				data.append('st.up: ' + line[6])
				data.append('activ: ' + line[7])
				data.append('recov: ' + line[8])
				data.append('ad.bl: ' + line[9])
				data.append('ad.hi: ' + line[10])
				data.append('notes: ' + (line[11] if (line[11] != '') else 'none'))
				outmsg = ' '.join(data)
				if len(namelist) == 0:
					namelist.append(outmsg)
				namelist.append(line[0])
	else:
		return 'no such character found'
	if len(namelist) == 0:
		return 'no matches for that move'
	if len(namelist) == 2:
		return outmsg
	else:
		returnmsg = 'more than one result found: '
		for ele in namelist[1:-1]:
			returnmsg += ele + ' | '
		returnmsg += namelist[-1]
		firstresult = 'First result:' + namelist[0]
		return [returnmsg, firstresult]


def alias(move):
	templist = move.split(' ')
	if len(templist) == 1:
		templist = move.split('.')
	newlist = []
	for ele in templist:
		for key in alist:
			if (ele in alist[key][1:]) is True:
				newlist.append(alist[key][0])
				break;
		else:
			newlist.append(ele)
	if len(templist) == len(newlist):
		return ' '.join(newlist)
	else:
		return ''

def aliasgen():
	global alist
	alist = {}
	fname = os.path.join('data','alias'+'.csv')
	if os.path.exists(fname):
		flines = open(fname,'r').readlines()
		for line in flines:
			line = line.rstrip().split(',')
			alist[line[0]] = []
			for element in line:
				alist[line[0]].append(element)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('server', help = 'server to connect to')
	parser.add_argument('nickname', help = 'nickname to set')
	parser.add_argument('channel', help = 'channel to join')
	args = parser.parse_args()
	main(args)