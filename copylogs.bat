@ECHO OFF
mkdir logs
mkdir database
SET /P PASS="Password: "
::ECHO %PASS%
pscp -pw %PASS% "pi@ipnfofuxpslepnbjo.go.ro:/home/pi/*.log" "logs/"
pscp -pw %PASS% "pi@ipnfofuxpslepnbjo.go.ro:/home/pi/*.db" "database/"
pscp -pw %PASS% "pi@ipnfofuxpslepnbjo.go.ro:/var/log/auth.log" "logs/auth.log"
::pscp pi@homenetworkdomain.go.ro:/home/pi/error.log logs/error.log
::pscp pi@homenetworkdomain.go.ro:/home/pi/error_monitor.log logs/error_monitor.log