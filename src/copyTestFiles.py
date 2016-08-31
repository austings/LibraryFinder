from shutil import *
from pathlib import Path
import codecs
import os
from util import *

def main():
	groupNumber = 4
	testFiles = obtainTestFiles("E:/Projects/TestCaseRecommend/TestCaseFinder/Output/testFiles-group" + str(groupNumber) + "-1-4.csv")
	outputDir = "S:/Danielle/TestFiles/" + str(groupNumber) + "/"

	if not os.path.exists(outputDir): 
		copyFiles(groupNumber, testFiles, outputDir)		
	copyFiles(groupNumber, testFiles, outputDir)


def copyFiles(groupNumber, testFiles, outputDir):
	print("Copying " + str(len(testFiles)) + " files for group " + str(groupNumber) + " to" + str(outputDir) + '\n')
	for aProj in testFiles:
		#projName = aProj.rsplit('\\', 1)[-1] #group 3 needs this format for proj name instead of aProj
		print("Copying test files for project " + str(aProj))
		projFiles = testFiles[aProj] 
		for proj in projFiles:
			try:
				projNum = proj.rsplit('/repo', 1)[1].split('/content/',1)[0].split('/', 1)[1] #for network drive (group 4) projects - gets the num1/num2 proj name format
				projName = projNum.replace('/', '-')
				fileName = proj.rsplit('/', 1)[-1] 
			except IndexError as e:
				print("Generated Index Error: " + str(e))
			#print("file name: " + str(fileName) + '\n')
			newFileName = str(projName) + "-" + str(fileName)
			#print("new file name: " + str(newFileName) + '\n')
			destPath = str(outputDir) + str(newFileName)
			print("Copy Name & Destination: " + str(destPath) + '\n')
			try:
				copy(proj, destPath)
			except IOError as exc:
				print('Generated an IOError exception trying to copy file ' + proj + ': ' + str(exc) + '\n')
	print("Copy Complete!" + '\n')

main()