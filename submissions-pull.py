#####################################################################
## 
## submissions-pull.py
##
##   Script to retrieve student gsubmit submissions from their
##   gsubmit directories; the resulting file names correspond to
##   the user names of those who submitted.
##
##

import sys                    # For command line arguments.
import os                     # For file and folder manipulation.
import time                   # For displaying timestamps.
from shutil import rmtree     # For deleting a folder.
from datetime import datetime # For making timestamps.

#####################################################################
## ASCII escape sequence macros for color output on the terminal.
##

class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
def printred(s): print(bcolors.RED + s + bcolors.ENDC)
def printblue(s): print(bcolors.BLUE + s + bcolors.ENDC)
def printyellow(s): print(bcolors.YELLOW + s + bcolors.ENDC)
def printpurple(s): print(bcolors.PURPLE + s + bcolors.ENDC)

#####################################################################
## Process the command line parameters.
##

if     len(sys.argv) == 5\
   and int(sys.argv[1]) in range(100,1000)\
   and sys.argv[2] in ['Fall', 'Spring']\
   and int(sys.argv[3].split('-')[0]) in range(2000,2100)\
   and len(sys.argv[4]) > 0:
    courseNumber = sys.argv[1]
    season = sys.argv[2]
    year = sys.argv[3].split('-')[0]
    due = datetime.strptime(sys.argv[3] + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
    submittedPaths = sys.argv[4].split(' ')
    extension = submittedPaths[0].split('.')[1]
else:
    print('\n  Usage:\n\n    % python submissions-pull.py <###> <Fall|Spring> <YYYY-MM-DD> "path1 path2 ..."\n')
    exit()

#####################################################################
## Other useful functions.
##

def laterDate(date1, date2):
    # Given two dates, return the later date.
    pass

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
if os.path.exists('./data'):
    rmtree('data')
os.makedirs("data")

# Retrieve submitted files.
for student in enrolled:

    # Emit empty placeholder in case there is no submission.
    open('data/'+student+'.'+extension, 'a').write("")

    # Attempt to Retrieve student's submission.
    if not student in gsubmits:
        printred('No gsubmit subfolder for '+student+' found!')
    elif not os.path.isfile(os.path.join(path, student)):
        filesFound = []
        late = False
        lateTimes = []
        for submittedPath in submittedPaths:
            filePath = path+student+'/'+submittedPath
            extension = extension
            if os.path.exists(filePath):
                (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(filePath)

                try:
                    txt = open(filePath, 'r').read()
                    open('data/'+student+'.'+extension, 'a').write("\n# " + submittedPath + "\n\n"+txt+"\n\n\n")
                except:
                    pass

                submission = datetime.strptime(time.ctime(mtime), "%a %b %d %H:%M:%S %Y")
                if due < submission:
                    late = True
                    lateTimes.append(str(time.ctime(mtime)))
                else:
                    pass
                filesFound = filesFound + [submittedPath]
        if len(filesFound) > 0 and len(filesFound) != len(submittedPaths):
	        if late:
	            printblue('Missing files ' + str(set(submittedPaths) - set(filesFound)) + ' from ' + student + " (" + ", ".join(lateTimes) + ").")
	        else:
	            printpurple('Missing files ' + str(set(submittedPaths) - set(filesFound)) + ' from ' + student + '!')
        elif len(filesFound) == 0:
            printred('Missing files ' + str(set(submittedPaths) - set(filesFound)) + ' from ' + student + '!')
        elif len(filesFound) == len(submittedPaths) and late:
            printblue(str(time.ctime(mtime)) + ': wrote files ' + str(filesFound) + ' for ' + student + " (" + ", ".join(lateTimes) + ").")
        elif len(filesFound) == len(submittedPaths):
            print(str(time.ctime(mtime)) + ': wrote files ' + str(filesFound) + ' for ' + student + ".")
        else:
            printyellow('Could not determine submission status for ' + student + '!')

#eof