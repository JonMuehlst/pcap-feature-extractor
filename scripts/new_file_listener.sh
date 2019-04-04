#!/bin/bash

### input: a folder path and a port number.
### output: full path of newly created files to netcat
# This script listens to created files in the input dir

# inotifywait -m -e create /path/to/dir | while read x y z ; do echo $x$z ; done | nc -lk 9999

inotifywait -m -e close_write  $1 | while read x y z ; do echo $x$z ; done | nc -lk $2
