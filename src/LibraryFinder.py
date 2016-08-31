'''
    Main program for the Library Finder
    author: Austin Sierra
    ref: Danielle Gonzalez's Heuristic Finder and
        Andrew Popovich's TestCaseFinder
       last edit: july 20 2016
'''
from util import *
from pathlib import Path
from importDetection import *
import codecs
import threading
import concurrent.futures
import os


def main():
    print("start")
    #create output file
    directory = "S:/Austin/Projects/LibraryFinder/output/libraries-1.csv"
    outFile = codecs.open(directory, "w", "utf-8")
    outFile.write("Project,FilePath,Library\n")
    outFile.close()

    # create a text file for any exceptions
    exceptionOutput = "S:/Austin/Projects/LibraryFinder/output/exceptions.txt"
    exceptionFile = open(exceptionOutput, "w", encoding="utf-8")
    exceptionFile.close()

    #find the path of all the projects
    allProjects = Path("S:/Austin/Projects/LibraryFinder/resource/projects")

    lock = threading.Lock()

    beginAnalysis(allProjects, exceptionOutput,directory)

def beginAnalysis(allProjects, exceptionOutput,directory):
    #thread pool

    #obtains the test files in dictionary where the key is the project id and the value is a list of files
    #found in util.py
    testFiles = obtainTestFiles("S:/Austin/Projects/LibraryFinder/resource/Test.csv")#list of files to be used
    print("Begin Analysis- # of test files " + str(len(testFiles)))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        futures = []
        
        #Add projects to the thread pool  
        for proj in allProjects.iterdir():
            if proj.is_dir(): 
                futures += [executor.submit(detect().findLines, proj, testFiles)]

        allResults =[]

        for myFuture in concurrent.futures.as_completed(futures):
            try:
                librariesFound = myFuture.result() #<-- what does this return
            except Exception as ex:
                print("Project Error: " +str(type(ex)) + ": " + str(ex.args)+ "-\n" +str(ex))
                writeException(exceptionOutput,str(ex))
            else:
                try:
                    count = 0
                    writeToFile(librariesFound,directory)
                except Exception as exc:
                    print('Generated an exception during processing: ' + str(exc))
                    writeException(exceptionOutput, str(exc))

    print("\nThe results have been successfully written to the output file")


def writeToFile(results,output):
    outFile = codecs.open(output, "a", encoding="utf-8")
    try:
        for item in results:
            count = 0
            for select in results[item]:
                while count < (len(results[item])-1):
                    outFile.write(str(item)+ "," + str(results[item][len(results[item])-1])+"," + str(results[item][count])+ "\n")
                    count= count+1
    except Exception as ex:
        print("Error occurred during output: " + str(ex)+ str(type(ex)))

    outFile.close()

#Danielles method
def writeException(file, exception):
    file = open(file, "a", encoding="utf-8")
    file.write(exception+"\n\n")
    file.close()


main()