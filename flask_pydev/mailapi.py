import smtplib
import json
from email.mime.text import MIMEText
import logging
import traceback
from smtplib import SMTPAuthenticationError
def read_mail_config():
    try:
        file=open("json/mailconfig.json","r")
        file_json=json.load(file)
        file.close()
    except:
        file_json={"temp1":{"min":10,"max":90},"temp2":{"min":10,"max":90},"mail_account":{"user":"random","mail":"random@gmail.com","pass":"random"},"receivers":["random@random.com"]}
        file=open("json/mailconfig.json","w")
        #print(file_json)
        json.dump(file_json,file)
        file.close()
    return file_json

def send_mail(msg):
    try:
        config_data=read_mail_config()
    
        msg = MIMEText(msg)

        msg['Subject'] = 'Critical temperature'
        msg['From'] = 'home_station'
        msg['To'] = 'client'
    
        receivers = config_data["receivers"]
        main_acc= config_data["mail_account"]
        sender = main_acc["mail"]
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            try:
                server.starttls()
                server.login(main_acc["user"], main_acc["pass"])
                server.sendmail(sender, receivers, msg.as_string())
                #print("Successfully sent email")
            except SMTPAuthenticationError as e:
                logging.getLogger("monitor_logger").error(str(traceback.format_exc()))
                pass
    except Exception as e:
        logging.getLogger("monitor_logger").error(str(traceback.format_exc()))
        pass
if __name__ == "__main__":
    send_mail("Temperatura atinsa : 95C ")
