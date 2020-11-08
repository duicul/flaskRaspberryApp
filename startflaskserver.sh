#!/bin/bash
#
### BEGIN INIT INFO
# Provides:          pitracker
# Required-Start:    $all
# Required-Stop:     
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Track pi.
# Description:       This service is used to track a pi.
### END INIT INFO
HOME=/home/pi
USER=pi
(python3 ~/flaskRaspberryApp/flask_pydev/monitor.py)&
