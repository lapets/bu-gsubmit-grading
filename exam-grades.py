#####################################################################
## 
## exam-grades.py
##
##   Creates grade files for an exam from a list of grades.
##
##

#####################################################################
## Data.
##

data = [\
  ("example",100)\
  ]

#####################################################################
## Write the grade files.
##
  
exam = 'exam' # Exam name (e.g. "midterm").
  
maxTotal = 100
for (name, raw) in data:
    if raw > maxTotal:
        extra = raw - maxTotal
        total = maxTotal
    else:
        total = raw
        extra = 0
    
    txt = '''Subject Area ### (Season YYYY)\nTitle\nExam\nDDDD, MM DD, YYYY'''
    txt += '''\n\nTotal:                         ''' +    ('  ' if len(str(total)) == 1 else    (' ' if len(str(total)) == 2 else '')) + str(total) + '''/100\n'''
    if extra != 0:
        txt += '''Extra credit:                + ''' +    ('  ' if len(str(extra)) == 1 else    (' ' if len(str(extra)) == 2 else '')) + str(extra) + '''\n'''
    open(exam+"/"+name+".py", 'w').write(txt)

#eof