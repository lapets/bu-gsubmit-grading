#####################################################################
## 
## gradefiles-push.py
##
##   Script to post grade files to the gsubmit directories of
##   enrolled students; the input grade file names should correspond
##   to the user names of the students.
##
##

import sys # For command line arguments.
import os  # For commands and file manipulation (walk, path, system).

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
   and int(sys.argv[3]) in range(2000,2100):
    courseNumber = sys.argv[1]
    season = sys.argv[2]
    year = sys.argv[3]
    path = sys.argv[4]
    task = path
    course = 'cs' + courseNumber + '/' + season + '-' + year
else:
    print('\n  Usage:\n\n    % python gradefiles-push.py <###> <Fall|Spring> <YYYY> <task>\n')
    exit()

#####################################################################
## Check for list of files.
##

if not os.path.exists('./data'):
    print('No folder "data" containing grade files found. Exiting.')
    exit()

#####################################################################
## Post the grade files.
##

for curdir, dirs, files in os.walk('./data/'):
    for file in files:
        txt = open('./data/'+file, 'r').read()
        name = file.split('.')[0]
        path = '/cs/course/' + course + '/homework/spool/'+name
        target = path+'/grade.' + task + '.txt'

        if os.path.exists(path):
            open(target, 'w').write(txt)
            print('Wrote file: ' + target)
        else:
            printred('Path '+path+' does not exist!')

#####################################################################
## Adjust grade file permissions so that students can read them.
##

os.system('chmod 0664 /cs/course/' + course + '/homework/spool/*/grade.' + task + '.txt')

#eof