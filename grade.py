#####################################################################
## 
## grade.py
##
##   Script template for grading a collection of Python submissions.
##
##

import sys                # Command line arguments.
import os                 # File/folder manipulation.
import time               # To sleep.
from shutil import rmtree # Deleting a folder.

#####################################################################
## Determine whether we are testing an entire folder or an individual
## file. If we are testing a folder, this block is the last block to
## run. Otherwise, it is skipped.
##

if len(sys.argv) == 1 or\
   len(sys.argv[1].split('.')) == 1: # No extension delimiter.

  # Default directory containing submissions is "./submitted".
  submitted = sys.argv[1] if len(sys.argv) == 2 else 'submitted'   

  # Default target directory is "./processed".
  processed = sys.argv[1] if len(sys.argv) == 2 else 'processed'

  # Create and clear target directory.
  if os.path.exists('./' + processed):
      rmtree(processed)
      time.sleep(1) # Wait for OS to process the above instruction.
  os.makedirs(processed)

  # Walk the specified directory containing the submitted files.
  for curdir, dirs, files in os.walk(submitted):
      for file in sorted(files): # Process in alphabetical order.
          status = 'Processing ' + file + '...'
          name = file.split('.')[0]
          os.system('python grade.py ' + submitted + '/' + file + ' > ' + processed + '/' + name + '.py')
          time.sleep(1) # In case above is asynchronous.
          gradesheet = '"""\n' + "\n".join([line[1:] for line in open(processed + '/'+name+'.py').read().split('\n') if len(line) > 0 and line[0] == '@']) + '\n"""\n\n'
          contents = open(submitted + '/'+name+'.py').read()
          open(processed + '/' + name + '.py', 'w').write(gradesheet + contents)

          print(status + 'done.')

  # Done processing file.
  exit()

# If there is only one file in the directory other than
# the script and there is no command line argument,
# process only that file.
name = None
for curdir, dirs, files in os.walk('./data/'):
    if len(files) == 2:
        name = [for f in files if f != 'grade.py'][0]

#####################################################################
## We are testing an individual file. Load the file.
##

name = sys.argv[1].split('.')[0] if name == None else name
exec(open(name+'.py').read())

total = 0

def str_(s):
    return '"'+str(s)+'"' if type(s) == str else str(s)

def notFound(part, maxPoints):
    lineStr = '@        ' + part + '. (' + str(maxPoints).rjust(2) + ' pts)     '
    print(lineStr + '0'.rjust(2) + '/' + str(maxPoints).rjust(2))

def check(part, maxPoints, functionName, inputs_result_pairs, isVar = False):
    prefix = functionName + '('
    suffix = ')'
    lineStr = '@        ' + part + '. (' + str(maxPoints).rjust(2) + ' pts)     '
    try:
        function = eval(functionName)
    except:
        print(lineStr + '0'.rjust(2) + '/' + str(maxPoints).rjust(2))
    else:
        global total
        passed = 0
        for (inputs, result) in inputs_result_pairs:

            output = None
            try:
                output = function(*inputs)
            except:
                output = '<Error>'

            if output == result:
                passed = passed + 1
            elif output == '<Error>':
                print("\n  Failed on:\n    "+prefix+', '.join([str_(i) for i in inputs])+suffix+"\n\n"+"  Should be:\n    "+str(result)+"\n\n"+"  A run-time error occurred!\n")
            else:
                pass
                print("\n  Failed on:\n    "+prefix+', '.join([str_(i) for i in inputs])+suffix+"\n\n"+"  Should be:\n    "+str(result)+"\n\n"+"  Returned:\n    "+str(output)+"\n")
        #print("Passed " + str(passed) + " of " + str(len(inputs_result_pairs)) + " tests.")
        pts = passed * maxPoints // len(inputs_result_pairs)
        total += pts
        print(lineStr + str(pts).rjust(2) + '/' + str(maxPoints).rjust(2))
        #print("")


#####################################################################
## Run the tests (example).
##

pass

#eof