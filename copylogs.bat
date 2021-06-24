@ECHO OFF
mkdir logs
mkdir database
mkdir json
SET /P PASS="Password: "
::ECHO %PASS%
pscp -i ../Rpi/privatekey.ppk -pw %PASS% "pi@ipnfofuxpslepnbjo.go.ro:/home/pi/flaskRaspberryApp/flask_pydev/logs/*.log*" "logs/"
ssh -i ../Rpi/privatekey.ppk -pw %PASS% "cd /var/log/uwsgi/app; sudo chmod a+r *;"
pscp -i ../Rpi/privatekey.ppk -pw %PASS% "pi@ipnfofuxpslepnbjo.go.ro:/var/log/uwsgi/app/*" "logs/"
pscp -i ../Rpi/privatekey.ppk -pw %PASS% "pi@ipnfofuxpslepnbjo.go.ro:/home/pi/flaskRaspberryApp/flask_pydev/*.db" "database/"
pscp -i ../Rpi/privatekey.ppk -pw %PASS% "pi@ipnfofuxpslepnbjo.go.ro:/home/pi/flaskRaspberryApp/flask_pydev/*.json" "json/"
::pscp -pw %PASS% "pi@ipnfofuxpslepnbjo.go.ro:/var/log/uwsgi/app/*.log*" "logs/"
pscp -i ../Rpi/privatekey.ppk -pw %PASS% "pi@ipnfofuxpslepnbjo.go.ro:/var/log/auth.log" "logs/auth.log"
::pscp pi@homenetworkdomain.go.ro:/home/pi/error.log logs/error.log
::pscp pi@homenetworkdomain.go.ro:/home/pi/error_monitor.log logs/error_monitor.log