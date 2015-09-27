bu-gsubmit-grading
==================

Scripts for retrieving student submissions and posting grades via gsubmit (a tool used by the Boston University Computer Science Department).

Usage
-----

The scripts always store all student files (whether they are student submission files or student grade files) in the directory `./data`. Each file name in `./data` corresponds to the user name of the student to whom it belongs.

To retrieve submitted files from every student in the fall course CS 235 under a path such as `hw1/hw1.py` and with a due date of September 14th, 2015, run the following:

    python submissions-pull.py 235 Fall 2015-09-14 "hw1/hw1.py"

Note that any number of file paths can be specified in the last argument (each path separated by a space). The contents of all the files found for each student will be concatenated into a single file corresponding to the user name of that student. Also note that this script assumes the file `235.txt` exists in the current directory and contains the user names of all currently enrolled students.

To post the grade files for `hw1` for all students taking CS 235 in the fall, run the following:

    python gradefiles-push.py 235 Fall 2015 hw1

The above will create the file `grade.hw1.txt` in the `gsubmit` directory of each student for the specified course.
