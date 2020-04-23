#!/bin/bash
process="flask"
if [ $# -gt 0 ]
then
  process=$1
fi
echo $process
ps aux | head -n 1
ps aux | grep -E "((^USER)|($process))"
