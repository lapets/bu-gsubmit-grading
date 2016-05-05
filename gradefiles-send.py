#####################################################################
## 
## gradefiles-send.py
##
##   Script to send grade files by email to enrolled students; the
##   input grade file names should correspond to the user names of
##   the students.
##
##

from email.mime.text import MIMEText # For creating a message string.
from subprocess import Popen, PIPE   # For sending email on linux.
import os  # For commands and file manipulation (walk, path, system).

#####################################################################
## Sending a simple email message.
##

def send(txt, courseNumber, task, sender, target):
    msg = MIMEText(txt)
    msg["From"] = sender + "@bu.edu"
    msg["To"] = target + "@bu.edu"
    msg["Cc"] = sender + "@bu.edu"
    msg["Subject"] = "CS " + str(courseNumber) + " " + task + " grade"
    p = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
    p.communicate(bytes(msg.as_string(), 'UTF-8'))

#####################################################################
## Process the command line parameters.
##

if     len(sys.argv) == 6\
   and int(sys.argv[1]) in range(100,1000)\
   and sys.argv[2] in ['Fall', 'Spring']\
   and int(sys.argv[3]) in range(2000,2100):
    courseNumber = sys.argv[1]
    season = sys.argv[2]
    year = sys.argv[3]
    task = sys.argv[4]
    sender = sys.argv[5]
else:
    print('\n  Usage:\n\n    % python gradefiles-send.py <###> <Fall|Spring> <YYYY> <task> <sender-username>\n')
    exit()

#####################################################################
## Check for list of files.
##

if not os.path.exists('./data'):
    print('No folder "data" containing grade files found. Exiting.')
    exit()

#####################################################################
## Send the grade files.
##

for curdir, dirs, files in os.walk('./data/'):
    for file in files:
        txt = open('./data/'+file, 'r').read()
        target = file.split('.')[0]
        send(txt, courseNumber, task, sender, target) 
        print('Sent grade file to ' + target + '.')

#eof