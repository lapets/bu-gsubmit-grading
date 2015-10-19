#####################################################################
## 
## submissions-pull.py
##
##   Script to retrieve student gsubmit submissions from their
##   gsubmit directories; the resulting file names correspond to
##   the user names of those who submitted.
##
##

import sys                               # Command line arguments.
import os                                # File/folder manipulation.
import time                              # Displaying timestamps.
from shutil import rmtree                # Deleting a folder.
from datetime import datetime, timedelta # Making timestamps.

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
    dueTime = datetime.strptime(sys.argv[3] + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
    submittedPaths = sys.argv[4].split(' ')
    extension = submittedPaths[0].split('.')[1]
    grace = 0 # Grace period in hours, if applicable.
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
if os.path.exists('./data'):
    rmtree('data')
os.makedirs("data")

# Retrieve submitted files.
for student in enrolled:

    # Emit empty placeholder in case there is no submission.
    open('data/'+student+'.'+extension, 'a').write("")

    # Attempt to retrieve student's submission.
    if not student in gsubmits:
        printred(('*' * 19) + ': no gsubmit subfolder for '+student+' found!')
    elif not os.path.isfile(os.path.join(path, student)):
        filesFound = []
        late = False
        lateTimes = []
        latestTime = None
        latestTimeStr = None
        
        # Attempt to retrieve every file expected in the submission.
        for submittedPath in submittedPaths:
            filePath = path+student+'/'+submittedPath
            extension = extension
            if os.path.exists(filePath):
                (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(filePath)

                # Attempt to retrieve the submission file.
                try:
                    txt = open(filePath, 'r').read()
                    open('data/'+student+'.'+extension, 'a').write("\n# " + submittedPath + "\n\n"+txt+"\n\n\n")
                except:
                    pass

                # Calculate the times.
                submissionTime = datetime.strptime(time.ctime(mtime), "%a %b %d %H:%M:%S %Y")
                if (dueTime + timedelta(hours=grace)) < submissionTime:
                    late = True
                    lateTimes.append(str(time.ctime(mtime)))
                if latestTime is None or submissionTime > latestTime:
                    latestTime = submissionTime
                    latestTimeStr = str(time.ctime(mtime))[0:-5]
                    
                filesFound = filesFound + [submittedPath]

        # Report the results for this student.
        if len(filesFound) == 0:
            printred(('*' * 19) + ': missing files ' + str(set(submittedPaths) - set(filesFound)) + ' from ' + student + '!')
        elif len(filesFound) > 0 and len(filesFound) != len(submittedPaths):
	        if late:
	            printblue(latestTimeStr + ': missing files ' + str(set(submittedPaths) - set(filesFound)) + ' from ' + student + ".")
	        else:
	            printpurple(latestTimeStr + ': missing files ' + str(set(submittedPaths) - set(filesFound)) + ' from ' + student + '.')
        elif len(filesFound) == len(submittedPaths):
            if late:
                printblue(latestTimeStr + ': wrote files ' + str(filesFound) + ' for ' + student + ".")
            else:
                print(latestTimeStr + ': wrote files ' + str(filesFound) + ' for ' + student + ".")
        else:
            printyellow(('*' * 19) + ': could not determine submission status for ' + student + '!')

#eof