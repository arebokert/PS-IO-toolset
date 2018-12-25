#!/usr/bin/env python

import os
import subprocess
import argparse
import re
from shutil import copyfile

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-c","--cu2s", type=str, help="Input folder containing CU2 files. If not supplied, CU2s will not be copied)")
	parser.add_argument("-i","--imgs", type=str, help="Input folder containing image files. If not supplied, images will not be copied)")
	parser.add_argument("-g","--games", type=str, help="Input folder containing bin files (need to be separated in to folders)",
		required=True)
	
	args = parser.parse_args()

	cu2sDir = args.cu2s
	imgsDir = args.imgs
	gamesDir = args.games
	scriptDir = os.path.realpath(__file__).replace("merger.py", "")
	binmergeDir = os.path.join(scriptDir,"binmerge")
	readGameIdDir = "read-game-id.sh"

	if cu2sDir and not os.path.isdir(cu2sDir):
		raise Exception("CU2 folder does not exist")
	if imgsDir and not os.path.isdir(imgsDir):
		raise Exception("Image folder does not exist")
	if not os.path.isdir(gamesDir):
		raise Exception("Games folder does not exist")

	cu2s = ""
	imgs = ""

	for root, dirs, files in os.walk(cu2sDir):
		cu2s = files
	for root, dirs, files in os.walk(imgsDir):
		imgs = files
	print bcolors.BOLD + "Amount of CU2 files found: " + str(len(cu2s)) + bcolors.ENDC
	print bcolors.BOLD + "Amount of image files found: " + str(len(imgs)) + bcolors.ENDC

	for root1, dirs, files in os.walk(gamesDir):
		for dir in dirs:
			path = os.path.join(root1, dir)
			print "Checking files in " + path
			for root2, dirs, files in os.walk(path):
				cu2File = ""
				binAmt = 0
				for file in files:
					if ".cue" in file:
						cu2File = file
					elif ".bin" in file:
						binAmt += 1
				if binAmt > 1:
					print "Several bins found, merging..."
					gameCu2 = os.path.join(path, cu2File)
					subprocess.check_output(binmergeDir + ' "' + cu2File + '" "' + cu2File.replace(".cue", "") + '"', shell=True, cwd=path)
					print "Deleting track files..."
					for file in files:
						if file != cu2File.replace(".cue", ".bin") and file != cu2File:
							delFile = os.path.join(path, file)
							try:
								os.remove(delFile)
							except Exception as Ex:
								print bcolors.FAIL + str(Ex) + ": Could not remove file" + bcolors.ENDC
			for root3, dirs, files in os.walk(path):
				for file in files:
					if ".cue" in file and cu2sDir and imgsDir:
						cu2File = file
						cu2List = []
						result = subprocess.check_output(readGameIdDir + ' "' + cu2File + '"', shell=True, cwd=path)
						try:
							gameId = result.split(": ",1)[1].replace("_", "-").replace(".", "").replace("\n", "").lower()
						except Exception as Ex:
							print bcolors.FAIL + str(Ex) + ": Failed to retreieve gameID, skipping copy of CU2 and image" + bcolors.ENDC
							continue
						if gameId:
							print "GameID found: " + gameId
							regexGameId = re.compile(r"([A-Z]{4}[ |-][0-9]{5})")
							for cu2 in cu2s:
								matchedFile = regexGameId.search(cu2)
								if matchedFile and matchedFile.group(1).replace(" ", "-").lower() == gameId:
									cu2List.append(cu2)
							cu2List.sort()
							matchedCu2 = ""
							if len(cu2List) > 1:
								print "Found more than one matching CU2 file"
								regexVersion = re.compile(r"([(].?)([0-9][.][0-9])([)])")
								matchedFile = regexVersion.search(file)
								if matchedFile:
									matchedFile = matchedFile.group(2)
									for cu2 in cu2List:
										matchedCu2 = regexVersion.search(cu2)
										if matchedCu2:
											matchedCu2 = matchedCu2.group(2)
											if matchedFile == matchedCu2:
												matchedCu2 = cu2
												break
											else:
												matchedCu2 = ""

							if len(cu2List) > 0:
								cu2Copy = ""
								if matchedCu2:
									print "Found matching CU2 file for this version of the bin file"
									cu2Copy = os.path.join(cu2sDir, matchedCu2)
								else:
									print "More than one matching CU2 file resulting in indecisiveness, picking last one in order"
									cu2Copy = os.path.join(cu2sDir, cu2List[len(cu2List)-1])
								try:
									copyfile(cu2Copy, os.path.join(path, file.replace(".cue", ".cu2")))
								except Exception as Ex:
									print bcolors.FAIL + str(Ex) + ": Could not copy CU2 file" + bcolors.ENDC
							else:
								print "No CU2 file found, skipping copy of CU2"
							imgCopied = False
							for img in imgs:
								matchedFile = regexGameId.search(img)
								if matchedFile and matchedFile.group(1).replace(" ", "-").lower() == gameId:
									print "Found matching image file for this bin file"
									imgCopy = os.path.join(imgsDir, img)
									try:
										copyfile(imgCopy, os.path.join(path, file.replace(".cue", ".bmp")))
									except Exception as Ex:
										print bcolors.FAIL + str(Ex) + ": Could not copy image file" + bcolors.ENDC
									imgCopied = True
									break
								else:
									imgCopied = False
							if not imgCopied:
								print "No image file found, skipping copy of image"
						else:
							print "No gameID found, skipping copy of CU2 and image"

if __name__ == "__main__":
	main()