'''
Created on Oct 27, 2020

@author: duicul
'''
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
#str_out="http{\n"
str_out="include       mime.types;\n"
#str_out+="types {\n"
#str_out+="    text/vtt vtt;\n"
#str_out+="}\n"
str_out+="server { \n"
str_out+="    listen 5000;\n"
str_out+="server_name 0.0.0.0; # customize with your domain name\n"
str_out+="\n"
str_out+="\n"
str_out+="    access_log  "+BASE_DIR+"/logs/access.log;\n"
str_out+="    error_log  "+BASE_DIR+"/logs/error.log;\n"
str_out+="    location / {\n"
str_out+="        # django running in uWSGI\n"
str_out+="        uwsgi_pass unix:///run/uwsgi/app/flaskRaspPi/socket;\n"
str_out+="        include uwsgi_params;\n"
str_out+="        uwsgi_read_timeout 300s;\n"
str_out+="        client_max_body_size 32m;\n"
str_out+="    }\n"
str_out+="\n"
str_out+="    location /static/ {\n"
#str_out+="        internal;\n" 
str_out+="       # static files\n"
str_out+="       alias "+os.path.join(BASE_DIR,"static")+"/; # ending slash is required\n"
str_out+="    }\n"
str_out+="\n"
str_out+="}\n"
#str_out+="}\n"
f = open("/etc/nginx/sites-enabled/flaskRaspPi", "w")
f.write(str_out)
f.close()
myCmd = 'service nginx restart'
os.system(myCmd)