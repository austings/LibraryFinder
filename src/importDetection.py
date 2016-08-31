import concurrent.futures
import threading
import re
import os
from fileExtractor import FileExtractor
import pdb
from util import obtainDependencies

# learned regex checks from http://regexone.com/lesson/introduction_abcs
def isLibrary(line,extension): #<--add regex checks
    
    #get file extension
    extension = extension[(extension.rfind(".")):]
    if(extension==".py"): #python
        match = re.match("((from)\s\w+\s)?(import)\s\w+",line)
    elif(extension==".js"): #javascript
        match = re.match("(<script).*(>)$",line)
    elif(extension==".java"): # java
        match = re.match("(import)\s.*(\.)?(;)$",line)
    elif(extension==".m" or extension==".h" or extension==".mlx" or extension ==".c" or extension ==".cc" or extension = ".cpp"): #objective c and matLab
        match = re.match("(#)?(import|include)\s(<|\")\w+",line)
    elif(extension==".rb"): #ruby
        match = re.match("(load|require)\s",line)
    elif(extension==".php"): #php
        match = re.search("(include|require)\s'\w+'",line)
    elif(extension==".sh"): #bash
        match = re.match("(source)\s\w+\.(sh)",line)
    elif(extension==".scala"): #scala
        match = re.match("(import)\s\w+",line)
    else:
        print("File extension "+extension+" not found. Skipping.")
        return False

    
    if match:
        return True
    else:
        return False

def detectImports(fileContent,extension): 
    numMatches = 0
    matchCollection = []
    for line in fileContent.split("\n"):
        if(isLibrary(line,extension)==True):
            matchCollection.append(line)
    return matchCollection

"""
Import Library Detection
@author Austin Sierra
A class used to locate external imported libraries and api
"""
class detect():
    def __init__(self):
        pass

    '''
    findLines is a method which finds import statement lines in a file and then returns
    the threadData with the appropriate lines.

    param(proj): is the project we are currently checking for import statements
    param(testFiles): a dictionary of test files where the key is the project id and value is a list of files
    '''
    def findLines(self, proj, testFiles):
        # Data unique to each thread (prevents overwriting by other threads)
        threadData = threading.local()
        # valid file extensions to look in
        #save project specfic data
        threadData.project = str(proj.name)
        threadData.projectDir = str(proj)
        print(threadData.projectDir)
        matches = {}
        #copy the the relevant files over for this project.
        threadData.testFiles = []
        if testFiles[threadData.project] != None:
            threadData.testFiles = testFiles[threadData.project]

        print("Begin analysis for project " + threadData.project + " # of test files: " + str(len(threadData.testFiles)))
        #read file contents
        for afile in threadData.testFiles: 
            contents = ""
            try:
                openedFile = open(afile ,"r",encoding="latin-1")
                for line in openedFile:
                    contents += line
                    contents += "\n"
                openedFile.close()
            except IOError as exc:
                print(str(afile))
                print('Generated an IOError exception in thread processProject: ' + str(exc))

            '''
            Detect Import Statements from file contents
            '''
            #CHECK IF there are import statements in this file. We return the threadData array containing the
            #project and its directory.
            threadData.libraries = (detectImports(contents,str(afile)))
            threadData.libraries.append(str(afile))
            matches[threadData.project] = threadData.libraries
            print("A file in project "+threadData.project+" is complete!")
        return matches
