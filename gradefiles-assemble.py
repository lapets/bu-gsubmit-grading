#####################################################################
## 
## gradefiles-assemble.py
##
##   Script template for assembling a collection of gradefiles from
##   a collection of graded submissions (processed using the grading
##   script).
##
##

import os                 # File/folder work (walk, path, system).
from shutil import rmtree # Deleting a folder.

#####################################################################
## Script to extract grade information from a compelted grade sheet.
##

def summary(txt):
    summary = []
    summary += [txt.split('Total:')[1].strip().split('/')[0]]

    if (txt.find('Extra credit:') != -1):
        summary += [txt.split('Extra credit:')[1].split('\n')[0].replace('+','').strip()]
    else:
        summary += [' ']

    if (txt.find('Late penalty:') != -1):
        summary += ['-'+txt.split('Late penalty:')[1].split('\n')[0].replace('-','').strip()]
    else:
        summary += [' ']

    return "\t".join(summary)

#####################################################################
## Convert every file into a gradefile ready for the gradefiles-push
## script; simultaneously display the columns for the grade sheet.
##

# Check if source directory exists.
if os.path.exists('./processed'):

    # Create and clear destination folder.
    if os.path.exists('./grades'):
        rmtree('grades')
    os.makedirs('grades')

    count = 0
    for curdir, dirs, files in os.walk('./processed/'):
        for file in files:
            txt = open('./processed/'+file, 'r').read().replace('"""', "'''").split("'''")
            if len(txt) >= 2:
                txt = txt[1]
                name = file.split('.')[0]
                target = './grades/'+name+'.py'
                open(target, 'w').write(txt[1:])
                print('Wrote file: ' + target + '\t' + summary(txt))
                count += 1

# Display count for double-checking purposes.
print('Wrote ' + str(count) + ' files.')

#eof
