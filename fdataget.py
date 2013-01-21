# Justin Woo <moomoowoo@gmail.com>
# ver: dev

import os
from multiprocessing import Lock

class fdataengine:
	def __init__(self, filepath, aliasespath, lock):
		# let's lock when we access files...
		self.lock = lock
		self.filepath = filepath
		self.queuedquery = []
		self.aliasfile = aliasespath
		self.aliastable = {}
		self.aliasgen()
		self.validinput = False
		self.outmsg = ''

	def aliasgen(self):
		if os.path.exists(self.aliasfile):
			flines = open(self.aliasfile, 'r').readlines()
			for line in flines:
				line = line.rstrip().split(',')
				self.aliastable[line[0]] = []
				for element in line:
					self.aliastable[line[0]].append(element)

	def alias(self, word):
		for key in self.aliastable:
			if word in self.aliastable[key][1:]:
				return self.aliastable[key][0]
		return word

	def isvalidinput(self):
		return self.validinput

	def getOUTMSG(self):
		return self.outmsg

	def parsePRIVMSG(self, line):
		# :nick!username@host PRIVMSG (channel)/(nick) :(message)
		line = line.lower().split(' ')
		msgin = line[3:]
		self.validinput = True
		if msgin[0][1] is ']' and len(msgin) >= 2: #legitimate query
		 	# :]char queryphrase
		 	char = msgin[0][2:] 
		 	query = ' '.join(msgin[1:]).replace('.',' ')
			fname = os.path.join(self.filepath, char + '.csv')
			if os.path.exists(fname):
				# let's make sure there's no messups with concurrent reading attempts
				self.lock.acquire()
				flines = open(fname,'r').readlines()
				self.lock.release()
				results = {}
				resultsdic = {}
				for word in query.split(' '):
					word = self.alias(word)
					resultsdic[word] = {}
					for line in flines:
						if line.split(',')[0].find(word) != -1:
							line = line.rstrip().split(',')
							move = line[0]
							data = []
							data.append('st.up: ' + line[6])
							data.append('activ: ' + line[7])
							data.append('recov: ' + line[8])
							data.append('ad.bl: ' + line[9])
							data.append('ad.hi: ' + line[10])
							data.append('notes: ' + (line[11] if (line[11] != '') else 'none'))
							result = ' '.join(data)
							results[move] = result
							resultsdic[word][move] = result
				mysets = []
				for key in resultsdic.keys():
					subkeys = resultsdic[key].keys()
					mysets.append(subkeys)
				matches = set(mysets[0]).intersection(*mysets)
				self.queuedquery = []
				for match in matches:
					self.queuedquery.append((match, results[match]))
				print len(self.queuedquery)	
				if len(self.queuedquery) == 0:
					retval = 'no matches found for move "%s"' % query
					self.outmsg = retval
				elif len(self.queuedquery) == 1:
					retval = '%s: %s' % (self.queuedquery[0][0], self.queuedquery[0][1])
					self.queuedquery = []
					self.outmsg = retval
				elif len(self.queuedquery) > 1:
					retval = 'multiple results: '
					appendlist = []
					for index,mytuple in enumerate(self.queuedquery):
						appendlist.append(' %s %s ' % (str(index + 1), mytuple[0]))
					retval += '|'.join(appendlist)
					self.outmsg = retval
			else:
				return 'invalid/unrecognized character name'
		elif msgin[0][1:].isdigit():
			num = int(msgin[0][1:])
			if num != 0 and num <= len(self.queuedquery):
				retval = '%s: %s' % (self.queuedquery[num - 1][0], self.queuedquery[num - 1][1])
				self.outmsg = retval
			else:
				self.validinput = False
		else:
			self.validinput = False
