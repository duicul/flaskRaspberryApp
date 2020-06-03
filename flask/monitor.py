import time
import datetime
import requests
import json

def start():
    i=0
    try:
        file=open("data.json","r")
        file_json=json.load(file)
        file.close()
    except:
        file_json=[]
    home_station_url="http://192.168.1.6"
    while i<100:
        i+=1
        time_stamp=str(datetime.datetime.now())
        temp = requests.get(home_station_url+"/temperature").json()
        volt = [requests.get(home_station_url+"/voltage").json()["volt1"] for i in range(3)]
        data={}
        data["time_stamp"]=time_stamp
        data["temp1"]=temp["temp1"]
        data["temp2"]=temp["temp2"]
        data["volt"]=sum(volt)/len(volt)
        file_json.append(data)
        file=open("data.json","w")
        json.dump(file_json,file)
        file.close()
        print(data)
        time.sleep(1800)

if __name__ == "__main__":
    start()
