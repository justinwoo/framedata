#! /usr/bin/env python
# Justin Woo <moomoowoo@gmail.com>

# Usage:
# usage: rawextract.py [directory]

# optional:
#   -h, --help			help
# required:
#   [directory]			directory where html files are stored
#   [output]			where to store output .csv files

# purpose:
# takes .htm files of shoryuken's wiki of sf4 characters and rips relevant data into .csv files

import argparse, sys, os

def main(args):
	global chardict
	chardict = {}
	for filename in os.listdir(args.directory):
		if filename[-4:] == '.htm':
			finlines = open(os.path.join(args.directory,filename), 'r').readlines()
			ctr = 0
			pos = []
			for line in finlines:
				if line.find('<th> Move Name') != -1:
					pos.append(ctr)
				ctr += 1
			if len(pos) >= 2:
				contents = process(filename, finlines[pos[0]:pos[1]])
				cname = ' '.join(filename.split(' ')[5:-10])
				chardict[cname] = contents

			else:
				print 'FILE ' + filename + ' FAILED TO PROCESS'
				print 'LEN(POS): ' + str(len(pos))
	for key in chardict:
		fout = open(os.path.join(args.output,key.lower().replace(' ','') + '.csv'), 'w')
		fout.write('\n'.join(chardict[key]))
		fout.close()

def process(filename, finlines):
	cname = filename.split(' ')[5:]
	contents = []
	biglist = ''.join(finlines).rstrip().split('</tr>')
	for entry in biglist[1:-2]:
		if entry.find('<th>') == -1:
			line = ''
			smlist = entry.rstrip().split('</td>')
			temp = smlist[0].split('File:')
			line += (temp[0].split('<a')[0][10:] + (temp[1].split('.gif')[0] if len(temp) > 1 else ''))
			line += ',' + (smlist[1].split('"center">')[1])
			line += ',' + (smlist[2].split('"center">')[1])
			line += ',' + (smlist[3].split('"center">')[1])
			line += ',' + (smlist[4].split('"center">')[1])
			line += ',' + (smlist[5].split('"center">')[1])
			line += ',' + (smlist[6].split('"center">')[1])
			line += ',' + (smlist[7].split('"center">')[1])
			line += ',' + (smlist[8].split('"center">')[1])
			line += ',' + (smlist[9].split('"center">')[1])
			line += ',' + (smlist[10].split('"center">')[1])
			line += ',' + (smlist[11].split('"center">')[1] if smlist[11].find('center') != -1 else smlist[11].split('"left">')[1])
			line = line.replace('\n','').lower()
			contents.append(line)
	return contents




if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('directory', help = 'directory where html files are stored')
	parser.add_argument('output', help = 'where to store output .csv files')
	args = parser.parse_args()
	main(args)