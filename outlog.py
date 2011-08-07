#!/usr/bin/env python

# -----------------------------------------------------------------------------
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#  
# Copyright (C) 2004 Sam Hocevar
#  14 rue de Plaisance, 75014 Paris, France
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
# 
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
# 
#  0. You just DO WHAT THE FUCK YOU WANT TO.
#
# -----------------------------------------------------------------------------

import sys, subprocess, threading, logging, logging.handlers

# -----------------------------------------------------------------------------

class Flusher(threading.Thread):
	def __init__(self, lg, fd):
		threading.Thread.__init__(self)
		self.lg = lg
		self.fd = fd
	
	def run(self):
		self.lg.info('--logging-started--')
		while True:
			line = self.fd.readline()
			if len(line) == 0:
				self.lg.info('--end-of-file--')
				return
			self.lg.info(line[:-1])

if len(sys.argv) < 3:
	print ('usage: %s <name> <cmd> [<arg> ... ]' % sys.argv[0])
	exit(1)

name = sys.argv[1]

formatter = logging.Formatter('%(asctime)s %(message)s')

outhandler = logging.handlers.TimedRotatingFileHandler(name+'-out.log',
		when = 'midnight', interval = 1, backupCount = 14)
outhandler.setFormatter(formatter)
outlogger = logging.getLogger(name+'-out')
outlogger.addHandler(outhandler)
outlogger.setLevel(logging.INFO)

errhandler = logging.handlers.TimedRotatingFileHandler(name+'-err.log',
		when = 'midnight', interval = 1, backupCount = 14)
errhandler.setFormatter(formatter)
errlogger = logging.getLogger(name+'-err')
errlogger.addHandler(errhandler)
errlogger.setLevel(logging.INFO)

print ('application starting... %s' % ' '.join(sys.argv[2:]))

try:
	watched_process = subprocess.Popen(' '.join(sys.argv[2:]),
			stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
	
	outfd, errfd = watched_process.stdout, watched_process.stderr
	
	Flusher(outlogger, outfd).start()
	Flusher(errlogger, errfd).start()
	watched_process.wait()

except:
	print 'application crashed!'
	sys.exit(1)

print 'application ended!'
sys.exit(0)

