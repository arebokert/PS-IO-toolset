#!/usr/bin/env python

import os
import subprocess
import argparse
import re
from shutil import copyfile


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-c","--cu2s", type=str, help="Input folder containing CU2 files. If not supplied, CU2s will not be copied)")
	parser.add_argument("-i","--imgs", type=str, help="Input folder containing image files. If not supplied, images will not be copied)")
	parser.add_argument("-g","--games", type=str, help="Input folder containing bin files (need to be separated in to folders)",
		required=True)
	parser.add_argument('-d', "--delete", help="Delete track-files after merging bins (might be unsafe, use at your own risk)", action='store_true')
	
	args = parser.parse_args()

	cu2sDir = args.cu2s
	imgsDir = args.imgs
	gamesDir = args.games
	delFiles = args.delete
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
	print "Amount of CU2 files found: " + str(len(cu2s))
	print "Amount of image files found: " + str(len(imgs))

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
				""" if binAmt > 1:
					print "Several bins found, merging..."
					gameCu2 = os.path.join(path, cu2File)
					subprocess.check_output(binmergeDir + ' "' + cu2File + '" "' + cu2File.replace(".cue", "") + '"', shell=True, cwd=path)
					if delFiles:
						print "Deleting track files..."
						for file in files:
							if file != cu2File.replace(".cue", ".bin") and file != cu2File:
								delFile = os.path.join(path, file)
								os.remove(delFile) """
				for file in files:
					if ".cue" in file and cu2sDir and imgsDir:
						cu2File = file
						cu2List = []
						print readGameIdDir + ' "' + cu2File + '"'
						result = subprocess.check_output(readGameIdDir + ' "' + cu2File + '"', shell=True, cwd=path)
						#gameId = result.split(": ",1)[1].replace("_", "-").replace(".", "").replace("\n", "").lower()
						""" if gameId:
							for cu2 in cu2s:
								if cu2.lower().find(result) != -1:
									cu2List.append(cu2)
							cu2List.sort()
							regex = re.compile(r"([(][0-9][.][0-9][)])", re.flags)
							matched = regex.findall(file)
							print matched
							newCu2List = list(filter(regex.match, cu2List))
							if len(cu2List) > 0:
								cu2Copy = os.path.join(cu2sdir, cu2List[len(cu2List)-1])
								print cu2copy + " - > " + root2 + "/" + file.replace(".cue", ".cu2")
								try:
									copyfile(cu2sdir + cu2copy, root2 + "/" + file.replace(".cue", ".cu2"))
								except:
									print("Error when copying!") 
							for img in imgs:
								if img.lower().find(binv) != -1:
									try:
										copyfile(imgsdir + img, root2 + "/" + file.replace(".cue", ".bmp"))
									except:
										print("Error when copying!")  """
							
					
	print "\nCommence copy process!"
	""" for root1, dirs, files in os.walk(gamesDir):
		for dir in dirs:
			for root2, dirs, files in os.walk(dir):
				for file in files:
					if ".cue" in file:

						
						p = subprocess.check_output('read-game-id.sh "' + file + '"', shell=True, cwd=root2)
						binv = p.split(": ",1)[1].replace("_", "-").replace(".", "").replace("\n", "").lower()
						print binv
						cu2list = []
						if binv != "":
							for cu2 in cu2s:
								if cu2.lower().find(binv) != -1:
									cu2list.append(cu2)
							cu2list.sort()
							if len(cu2list) > 0:
								cu2copy = cu2list[len(cu2list)-1]
								print cu2sdir + cu2copy + " - > " + root2 + "/" + file.replace(".cue", ".cu2")
								try:
									copyfile(cu2sdir + cu2copy, root2 + "/" + file.replace(".cue", ".cu2"))
								except:
									print("Error when copying!") 
							for img in imgs:
								if img.lower().find(binv) != -1:
									try:
										copyfile(imgsdir + img, root2 + "/" + file.replace(".cue", ".bmp"))
									except:
										print("Error when copying!") 
						#print matching
						#cu2 = [s for s in cu2s if binv in s]
						#print cu2
						#if cu2
						#shutil.move(cu2sdir + cu2, root2 + "/" + file.replace(".cue", "cu2"))
						#os.system("read-game-id.sh " + file)
						#print root + "/" + file
						#os.system('binmerge-master/binmerge "' + root+"/"+file + '" "' + file.replace(".cue", "") + '"') """

if __name__ == "__main__":
	main()