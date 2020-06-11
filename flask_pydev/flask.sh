#!/bin/bash
str=~/flaskRaspberryApp/flask_pydev/Login.py
if test $# -ge 1
then str=$1
fi
echo  $str
set FLASK_APP=$str
python3 $str
