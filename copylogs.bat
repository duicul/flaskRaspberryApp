mkdir logs
mkdir database
pscp "pi@ipnfofuxpslepnbjo.go.ro:/home/pi/*.log" "logs/"
pscp "pi@ipnfofuxpslepnbjo.go.ro:/home/pi/*.db" "database/"
::pscp pi@homenetworkdomain.go.ro:/home/pi/error.log logs/error.log
::pscp pi@homenetworkdomain.go.ro:/home/pi/error_monitor.log logs/error_monitor.log