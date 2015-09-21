#####################################################################
## 
## gradefiles-push.py
##
##   Script to post grade files to the  gsubmit directories of
##   enrolled students; the input grade file names should correspond
##   to the user names of the students.
##
##

import os # walk, path, system

#####################################################################
## Process the command line parameters.
##

task = 'hw6'
course = 'cs235/Spring-2015'

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
            print('Path '+path+' does not exist!')

#####################################################################
## Adjust grade file permissions so that students can read them.
##

os.system('chmod 0664 /cs/course/' + course + '/homework/spool/*/grade.' + task + '.txt')

#end