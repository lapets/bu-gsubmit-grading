#####################################################################
## 
## submissions-pull.py
##
##   Script to retrieve student gsubmit submissions from their
##   gsubmit directories; the resulting file names correspond to
##   the user names of those who submitted.
##
##

import sys
import os
import time
from shutil import rmtree
from datetime import datetime

#####################################################################
## ASCII escape sequence macros for color output on the terminal.
##

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
def printred(s): print(bcolors.FAIL + s + bcolors.ENDC)
def printblue(s): print(bcolors.OKBLUE + s + bcolors.ENDC)

#####################################################################
## Process the command line parameters.
##

if     len(sys.argv) == 5\
   and int(sys.argv[1]) in range(100,1000)\
   and sys.argv[2] in ['Fall', 'Spring']\
   and int(sys.argv[3].split('-')[0]) in range(2000,2100):
    courseNumber = sys.argv[1]
    season = sys.argv[2]
    year = sys.argv[3].split('-')[0]
    due = datetime.strptime(sys.argv[3] + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
    submittedPaths = sys.argv[4].split(' ')
else:
    print('\n  Usage:\n\n    % python submissions-pull.py <###> <Fall|Spring> <YYYY-MM-DD> "path1 path2 ..."\n')
    exit()

#####################################################################
## Retrieve files.
##

# Path to submitted assignment files.
path = '/cs/course/cs' + courseNumber + '/' + season + '-' + str(year) + '/homework/spool/'
gsubmits = os.listdir(path)

# Get list of enrolled students.
if not os.path.isfile(courseNumber + '.txt'):
    print("Missing student list file: " + courseNumber + ".txt")
    exit()
enrolled = sorted(open(courseNumber + '.txt').read().split("\n"))

# Create and clear destination folder.
rmtree('data')
os.makedirs("data")

# Retrieve submitted files.
for student in enrolled:
    if not student in gsubmits:
        printred('No gsubmit subfolder for '+student+' found!')
    elif not os.path.isfile(os.path.join(path, student)):
        
        #submittedPaths = ['hw1/a1.py', 'a1.py', 'Assignment1/a1.py', 'PS1/a1.py', 'a1/a1.py', 'HW1/a1.py','hw01/a1.py', 'HW01/a1.py','CS320_Assignment_1/a1.py']
        #submittedPaths = ['final/Parse.hs', 'final/TypeCheck.hs','final/Interpret.hs','final/Optimize.hs','final/Compile.hs']
        #submittedPaths = ['midterm/parse.py', 'midterm/interpret.py', 'midterm/compile.py', 'midterm/analyze.py', 'midterm/validate.py']
        #submittedPaths = ['project/AbstractSyntax.hs', 'project/Parse.hs', 'project/TypeCheck.hs', 'project/KeyValueStore.hs', 'project/Interpret.hs',  'project/Validate.hs', 'project/Compile.hs']
        #submittedPaths = ['hw1/hw1.py']
        #submittedPaths = ['hw3/hw3.py']
        #submittedPaths = ['hw5/Allocation.hs']
        #submittedPaths = ['hw3/parse.py', 'hw3/interpret.py', 'hw3/machine.py', 'hw3/compile.py']

        filesFound = []
        late = False
        lateTimes = []
        found = False
        for submittedPath in submittedPaths:
            filePath = path+student+'/'+submittedPath
            if os.path.exists(filePath):# and not found:
                (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(filePath)

                try:
                    txt = open(filePath, 'r').read()
                    ext = filePath.split(".")[-1] # Use file extensions.
                    open('data/'+student+'.'+ext, 'a').write("\n# " + submittedPath + "\n\n"+txt+"\n\n\n")
                except:
                    pass

                submission = datetime.strptime(time.ctime(mtime), "%a %b %d %H:%M:%S %Y")
                if due < submission:
                    late = True
                    lateTimes.append(str(time.ctime(mtime)))
                    #printblue(str(time.ctime(mtime)) + ': wrote file for ' + student + ".")
                else:
                    pass
                    #print(str(time.ctime(mtime)) + ': wrote file for ' + student + ".")
                found = True
                filesFound = filesFound + [submittedPath]
        if len(filesFound) != len(submittedPaths):
            printred('*** Missing files ' + str(set(submittedPaths) - set(filesFound)) + ' from ' + student + '! ***')
        elif len(filesFound) == len(submittedPaths) and late:
            printblue(str(time.ctime(mtime)) + ': wrote files ' + str(filesFound) + ' for ' + student + " (" + ", ".join(lateTimes) + ").")
        elif len(filesFound) == len(submittedPaths):
            print(str(time.ctime(mtime)) + ': wrote files ' + str(filesFound) + ' for ' + student + ".")

        #if not found:
        #    printred('No submission from '+student+' found!')

#eof