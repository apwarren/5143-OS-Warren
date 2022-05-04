#### 4 May 2022
### 5143 Reader Writer Part 1 Simulator

#### Group Members

- Allyson Warren

#### Overview:
This is a project written in python that implements a reader writer 
program in which multiple readers are capable of reading from memory at
once or only writer can access memory at a time. Memory is capable of being
treated as one entity or sectioned off to three sections. If sectioned, a writer
will only block off the needed memory sections and won't prevent readers or other
writers from accessing unused memory. All readers and writers are threaded processes
and there is to be 5 times the amount of readers that there are writers. After fully
running the simulation which can take a while, the program will display how long it
took for the simulation to finish running. While running, the program will display
what is happening by using the rich library to display memory in a table as well
as a table showing which processes are reading and writing to given memory sections.
Writers are given a generated set of instructions to read, operate, and write from. Readers
are given a set of instructions that are strictly limited to just reading.


#### Instructions

To run the simulation you will need to state the amount of writers you wish to simulate.
Each will have its own set of instructions. You can also optionally type yes or true to
have the simulation section off memory, otherwise it will treat memory as one item by default.
Typing new will also generate a new set of file instructions for writers to read from. This is
not default to allow for two simulation to run the same instructions for observation purposes.

- To run type the following:
- python readerWriters.py 5 yes
- python readerWriters.py 5
- python readerWriters.py 5 no
- python readerWriters.py 5 yes new
- python readerWriters.py 5 no new
- python readerWriters.py 5 new


This will run the program with 5 writers and 25 readers. If yes is passed, it will section off memory when only one memory block is needed. If no is passes, it will not section off memory. If new is passed, it will generate a new set of instructions to read from.

