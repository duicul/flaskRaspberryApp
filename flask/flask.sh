#!/bin/bash
echo $#
str=Login.py
if test $# -ge 1
then str=$1
fi
echo  $str
set FLASK_APP=$str
python $str
