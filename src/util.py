
import csv
'''
Utility functions
    with code written by Andrew Popovich as noted
'''

def obtainTestFiles(testFilesCsv):
    """
        @author Andrew Popovich
        obtainTestFiles will parse the test file CSV to extract
        a list of test files for each project. This information is
        then returned in a dictionary where:

        key -> project name (e.g. 10264)
        value -> list of test file paths in that project

        Parameters: testFilesCsv - the file path of the test files csv
        Retruns: A dictionary representing the test files in each project
        
    """
    print ("Generating Test Files Dictionary")
    # Key -> Project names, Value -> List of test file names
    projectTestFiles = {}

    testFiles = csv.reader(open(testFilesCsv, "r", encoding="utf-8"))

    # Loop through each line in file to populate projectTestFiles
    count = 0
    for line in testFiles:
        project = line[1]
        if count > 0:
            if  (project not in projectTestFiles):
                projectTestFiles[project] = [line[0].replace("\\","/")]
            else:
                projectTestFiles[project] += [line[0].replace("\\","/")]                                           
        count += 1

    print ("Generating Test Files Dictionary - Complete!")    
    return projectTestFiles

def obtainDependencies(dependencyFile):
    """
        @author Andrew Popovich
        obtainDependencies parses the dependency file for a project
        and returns the file depenencies in the form of a dictionary.
        This dictionary is represented as:

        key -> String for the filepath of the file
        value -> List of strings indicating the files that the key
                 depends on

        Parameters: depedencyFile - String file path to the dependency file
        Returns: A dictionary representing the dependencies in the project
    """
    deps = {}

    # Ugly, but quick and dirty way to account for dep file not
    # having full paths...
    depTokens = dependencyFile.split("\\")
    depRoot = depTokens[0] + "/" + depTokens[1] + "/" + depTokens[2] + "/" + depTokens[3] +"/"
    
    depFile =  csv.reader(open(dependencyFile))
    count = 0
    for line in depFile:
        dependency = depRoot + line[1].replace("\\","/")
        file = depRoot + line[0].replace("\\","/")
        if count > 0:
            if  (file not in deps):
                deps[file] = [dependency]
            else:
                deps[file] += [dependency]                                           
        count += 1

    return deps

def lookupGenerator(filename):
    """
        @author Andrew Popovich
        lookupGenerator parses a file to create a lookup table 
        based on the contents of the file.
    
        Parameters: filename - String representing the path to the file
        Returns: A dictionary representing the file's contents
                 Key = pattern
                 value = list of keywords
        
        Note: The contents of the file pointed to by filename must 
              be in the form of: 
          
              pattern,keyword, keyword, .... keyword
    """
    lookup = {}
    for line in open(filename):
        heuristics = []
        if line != "":
            line = line.strip("\n")
            tokens = line.split(",")
            pattern = tokens[0]
            for toke in tokens[1:]:
                heuristics.append(toke)
            if pattern not in lookup:
                lookup[pattern] = heuristics
            else:
                print("Pattern already included, add keyword to that list")
    return lookup
