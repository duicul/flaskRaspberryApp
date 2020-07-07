import smtplib
import json
from email.mime.text import MIMEText
import logging
import traceback

def read_mail_config():
    try:
        file=open("mailconfig.json","r")
        file_json=json.load(file)
        file.close()
    except:
        file_json={"temp1":{"min":10,"max":90},"temp2":{"min":10,"max":90},"mail_account":{"user":"random","mail":"random@gmail.com","pass":"random"},"receivers":["random@random.com"]}
        file=open("mailconfig.json","w")
        #print(file_json)
        json.dump(file_json,file)
        file.close()
    return file_json

def send_mail(msg):
    
    config_data=read_mail_config()
    
    msg = MIMEText(msg)

    msg['Subject'] = 'Critical temperature'
    msg['From'] = 'home_station'
    msg['To'] = 'client'
    
    receivers = config_data["receivers"]
    main_acc= config_data["mail_account"]
    sender = main_acc["mail"]
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(main_acc["user"], main_acc["pass"])
            server.sendmail(sender, receivers, msg.as_string())
            #print("Successfully sent email")

if __name__ == "__main__":
    send_mail("Temperatura atinsa : 95C ")
