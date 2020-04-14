#!/bin/bash
chmod a+x $(pwd)/startflaskserver.sh;
cat startflaskserver.sh > /etc/init.d/startflaskserver.sh;
chmod a+x /etc/init.d/startflaskserver.sh;
