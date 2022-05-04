#### 14 Feb 2022
#### 5143 Shell Project 

#### Group Members

- Allyson Warren

#### Overview:
This is a project written in python that implements a basic shell. It follows
the standard commands expected within a standard shell such as listing and handling
files and directories within the computer system. It can change permissions, directories,
copy, move, and read from any item within a current directory.


#### Instructions

- To run type python3 shell.py into a linux shell and it will run the program

***Commands***:

| Command | Flag / Param | Meaning                                   | Notes    |
| ------- | ------------ | ----------------------------------------- |----------|
| `ls`    |              | list files and directories                | finished |
|         | `-a`         | list all show hidden files                | finished |
|         | `-l`         | long listing                              | finished | 
|         | `-h`         | human readable sizes                      | finished |
| `mkdir` |              | make a directory                          | finished |
| `cd`    | `directory`  | change to named directory                 | finished |
| `cd`    |              | change to home-directory                  | finished |
|         | `~	`        | change to home-directory                  | finished |
|         | `..`         | change to parent directory                | finished |
| `pwd`   |              | display the path of the current directory | finished |
| `cp `   | `file1 file2`                | copy file1 and call it file2                                               | finished |
| `mv`    | `file1 file2`                | move or rename file1 to file2                                              | finished |
| `rm`    | `file`                       | remove a file                                                              | finished |
|         | `-r`                         | recurse into non-empty folder to delete all                                | finished |
|         | `fil*e` or `*file` or `file* | removes files that match a wildcard                                        | finished |
| `rmdir` | `directory`                  | remove a directory                                                         | finished |
| `cat`   | `file`                       | display a file                                                             | finished |
|         | `file1`,`file2`,`fileN`      | display each of the files as if they were concatenated                     | finished |
| `less`  | `file`                       | display a file a page at a time                                            | finished |
| `head`  | `file`                       | display the first few lines of a file                                      | finished |
|         | `-n`                         | how many lines to display                                                  | finished |
| `tail`  | `file`                       | display the last few lines of a file                                       | finished |
|         | `-n`                         | how many lines to display                                                  | finished |
| `grep`  | `'keyword' file`             | search a file(s) files for keywords and print lines where pattern is found | finished |
|         | `-l`                         | only return file names where the word or pattern is found                  | finished |
| `wc`    | `file`                       | count number of lines/words/characters in file                             | finished |
|         | `-l`                         | count number of lines in file                                              | finished |
|         | `-m`                         | count number of characters in file                                         | finished |
|         | `-w`                         | count number of words in file                                              | finished |
| `command > file`          | redirect standard output to a file                   |  | finished |
| `command >> file`         | append standard output to a file                     |  | finished |
| `command < file`          | redirect standard input from a file                  |  | finished |
| `command1`                | `command2`                                           |  | finished |
| `command1 \| command2`    | pipe the output of command1 to the input of command2 |  | finished |
| `cat file1 file2 > file0` | concatenate file1 and file2 to file0                 |  | finished |
| `sort`                    | sort data                                            |  | finished |
| `who`                     | list users currently logged in                       |  | finished |
| `history`   | show a history of all your commands                              |  | finished |
| `!x`        | this loads command `x` from your history so you can run it again |  | finished |
| `chmod xxx` | change modify permission                                         |  | finished |



***Non Working Components***

Every command should be working adequately.
You cannot use the arrow keys to grab previous history though.

***References***
- https://linuxconfig.org/understanding-of-ls-command-with-a-long-listing-format-output-with-permission-bits
- https://stackoverflow.com/questions/1830618/how-to-find-the-owner-of-a-file-or-directory-in-python
- https://stackoverflow.com/questions/16994696/python-get-time-stamp-on-file-in-mm-dd-yyyy-format
- https://stackoverflow.com/questions/14319023/find-out-who-is-logged-in-on-linux-using-python
