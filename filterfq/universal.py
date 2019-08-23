#####################################################################
#																	#
#universal.py - universal functions									#
#																	#
#####################################################################


import os
import sys
import logging


def checkPathExists(path):
	"""Check if path is exists"""
	if not os.path.exists(path):
		logger = logging.getLogger("timestamp")
		logger.error("Directory does not exists: " + path + "\n")
		sys.exit(1)

def makeSurePathExists(path):
	"""Check if path is exists, if not create path"""
#	if not path:
#		return
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			logger = logging.getLogger("timestamp")
			logger.error("Path does not exists: " + path + "\n")


def checkFilesExist(inputFiles):
	"""Check if file is exists"""
	if type(inputFiles) == str:
		checkFileExists(inputFiles)
	else:
		if type(inputFiles) == list:
			for f in inputFiles:
				if type(f) == str:
					checkFileExists(f)
				else:
					if type(f) == list:
						checkFilesExist(f)
					else:
						logger = logging.getLogger("timestamp")
						logger.error("File does not exists: " + f + "\n")
		else:
			logger = logging.getLogger("timestamp")
			logger.error("File does not exists: " + inputFiles + "\n")

	
def checkFileExists(inputFile):
	if not os.path.isfile(inputFile):
		logger = logging.getLogger("timestamp")
		logger.error("File does not exists: " + inputFile + "\n")
		sys.exit(1)



