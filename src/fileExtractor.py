'''
    FileExtractor class for extracting code files from a project

    @author: Andrew Popovich
'''
import os
class FileExtractor(object):
    """
        FileExtractor is a class for extracting all of the valid code
        files found using this utility. It also can be used for outputting
        all files that are invalid in this utility.
    """

    def __init__(self, projectRoot, fileOutput, validFileExts):
        """
            Constructor
        """
        self.fileExcOutput = fileOutput
        self.projectRoot = projectRoot
        self.validFiles = validFileExts
        self.filesExcluded = []
        self.projectFiles = []
        
    def determineProjectFiles(self):
        """
            Returns a list of valid code file extensions found in the
            project directory/subdirectories
            
            Parameters: projectRoot - Path object representing the root directory
                                      of a project
                        validFiles - A list of valid code file extensions
            Returns: A list of strings representing valid code file extensions in
                     the project
        
        """
        fileList = self.projectRoot.glob("**/*.*")
        for file in fileList:
            if file.suffix.lstrip(".") in self.validFiles: 
                self.projectFiles += [file]
            else:
                self.filesExcluded += [file]
        
        #Uncomment the next line to output files that were 
        #excluded from processing separately
        #self.outputExcludedFiles()
        
        return self.projectFiles
    
    def outputExcludedFiles(self):
        """
            Opens the output file instance variable and writes
            the excluded file list to it.
        """
        outputFile = open(self.fileExcOutput,"w",-1,"utf-8")
        for file in self.filesExcluded:
            outputFile.write(str(file) + "\n")
        outputFile.close()
            