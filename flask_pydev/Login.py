from flask import Flask,session,request,render_template
#from inputpin import InputPin
#from time import sleep
import json
import os
import numpy as np
from regressionaprox import aggregate_data,display_regions
import requests
import traceback
from data_classes import Temperature_Data,Voltage_Data,AC_Data
from weather import Weather
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = '571ba9$#/~90'

home_station_url="http://192.168.1.6"
polling_period=1800

try:
	file=open("data.json","r")
	file_json=json.load(file)
	home_station_url=file_json["url"]
	polling_period=file_json["period"]
	file.close()
except:
	file_json={"url":home_station_url,"period":polling_period}
	file=open("data.json","w")
	json.dump(file_json,file)
	file.close()


td=Temperature_Data("measure.db",home_station_url,'werkzeug')
vd=Voltage_Data("measure.db",home_station_url,'werkzeug')
acd=AC_Data("measure.db",home_station_url,'werkzeug')


@app.route('/current_timestamp')
def current_timestamp():
	return str(td.current_timestamp())
	
@app.route('/cpu_gpu_temp')
def cpu_gpu_temp():
	temps = os.popen('vcgencmd measure_temp').read().replace("\n","<br>")
	return temps

@app.route('/memory_usage')
def memory_usage():
	memory = os.popen('free -ht').read().replace("\n","<br>").replace(" ","&nbsp;&nbsp;")
	return memory

@app.route('/disk_usage')
def disk_usage():
	memory = os.popen('df -H').read().replace("\n","<br>").replace(" ","&nbsp;&nbsp;")
	return memory

@app.route('/data_retr')
def data_status():
	return "okay stubbed" #data_retr.showdata()

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/covid_data_all/<case_type>/<api>/<data_type>/<predict_len>/<pol_grade>',methods = ['POST'])
def extract_data_pol(api,predict_len,pol_grade,case_type,data_type):
        #print(api)
        #print(case_type)
        #print(data_type)
        #print(predict_len)
        #print(pol_grade)
        #print(request.form) 
        #print(request.form['countries'])
        countries=json.loads(request.form['countries'])
        #print(countries)
        return aggregate_data(pol_grade,countries,data_type,case_type,predict_len,api)

@app.route('/covid_data/<case_type>/<api>/<data_type>',methods = ['POST'])
def extract_data(api,case_type,data_type):
        #print(api)
        #print(case_type)
        #print(data_type)
        #print(request.form)
        #print(request.form['countries'])
        countries=json.loads(request.form['countries'])
        return aggregate_data(0,countries,data_type,case_type,0,api)

@app.route('/regions/<case_type>/<api>/<data_type>',methods = ['POST'])
def extract_regions(api,case_type,data_type):
        #print(api)
        #print(case_type)
        #print(data_type)
        #print(request.form)
        #print(request.form['countries'])
        countries=json.loads(request.form['countries'])
        ret = display_regions(countries,data_type,case_type,api)
        #print(ret)
        return ret

@app.route('/force_poll')
def force_poll():
	td.poll_value()
	vd.poll_value()
	acd.poll_value()
	return ""

@app.route('/temperature')
def temperature():
        data=td.extract_last()
        if data==None:
                return {}
        #print(data)
        #r = requests.get(home_station_url+"/temperature")
        return {"date":data[1],"temp1":data[2],"temp2":data[3]}
        

@app.route('/voltage')
def voltage():
        data=vd.extract_last()
        if data==None:
                return {}
        #print(data)
        #r = requests.get(home_station_url+"/voltage")
        return {"date":data[1],"volt1":data[2]}

def reset_config_weather():
	file_json={"api_key":"random","city":"random"}
	file=open("config_weather.json","w")
	json.dump(file_json,file)
	file.close()

@app.route('/weather')
def weather():
	city=""
	api_key=""
	try:
		file=open("config_weather.json","r")
		file_json=json.load(file)
		file.close()
		city=file_json["city"]
		api_key=file_json["api_key"]
	except:
		reset_config_weather()
	weat=Weather(api_key,city,'werkzeug')
	return json.dumps(weat.request_data())

@app.route('/ac')
def ac():
        data=acd.extract_last()
        if data==None:
                return {}
        #print(data)
        #r = requests.get(home_station_url+"/ac")
        #print("data "+str(data))
        return {"date":data[1],"voltage":data[2],"current":data[3],"power":data[4],"energy":data[5]}

@app.route('/home_station/voltage_data')
def home_station_voltage_data():
        #items=int()
        volt=[]
        try:
                volt = vd.extract_all_interval(request.args["items"])
        except:
                logging.error(str(traceback.format_exc()))
        #print(data)
        t=[]
        for i in volt:
            t.append({"date":i[1],"volt1":i[2]})    
        return json.dumps(t)

@app.route('/home_station/ac_data')
def home_station_ac_data():
        #items=int(request.args["items"])
        #print(items)
        data=[]
        try:
                data = acd.extract_all_interval(request.args["items"])
        except:
                logging.error(str(traceback.format_exc()))
        #print(data)
        t=[]
        for i in data:
            t.append({"date":i[1],"voltage":i[2],"current":i[3],"power":i[4],"energy":i[5]})    
        return json.dumps(t)
       
@app.route('/home_station/temperature_data')
def  home_station_temperature_data():
        #items=int(request.args["items"])
        #print(items)
        temp=[]
        try:
                temp = td.extract_all_interval(request.args["items"])
        except:
                logging.getLogger('werkzeug').error(str(traceback.format_exc()))
        #print(data)
        t=[]
        for i in temp:
            t.append({"date":i[1],"temp1":i[2],"temp2":i[3]}) 
        
        pol_grade=2
        predict_len=8
        dataset_size=10 if len(t)>10 else len(t)
        pol_regr_y_t1=[]
        pol_regr_y_t2=[]
        try:
        	if dataset_size > 0:
        		data_t1=[t[i]["temp1"] for i in range(len(t)-dataset_size,len(t))]
        		data_t2=[t[i]["temp2"] for i in range(len(t)-dataset_size,len(t))]
        		
        		poly_fit_t1 = np.poly1d(np.polyfit(np.array(range(dataset_size)),np.array(data_t1),pol_grade))
        		pol_regr_y_t1=[round(poly_fit_t1(xi),2) for xi in range(dataset_size,dataset_size+predict_len)]
        		
        		poly_fit_t2 = np.poly1d(np.polyfit(np.array(range(dataset_size)),np.array(data_t2),pol_grade))
        		pol_regr_y_t2=[round(poly_fit_t2(xi),2) for xi in range(dataset_size,dataset_size+predict_len)]  
        except Exception:
        	logging.getLogger('werkzeug').error(str(traceback.format_exc()))
        	pol_regr_y_t1=[]
        	pol_regr_y_t2=[]
        predictions=[]
        if len(pol_regr_y_t1)==len(pol_regr_y_t2):
        	for i in range(len(pol_regr_y_t1)):
        		pred_date_time=datetime.strptime(t[len(t)-1]["date"],"%Y-%m-%d %H:%M:%S")+ timedelta(minutes = (i+1)*15)
        		predictions.append({"date":str(pred_date_time),"temp1":pol_regr_y_t1[i],"temp2":pol_regr_y_t2[i]})
        
        result={"recorded":t,"predict":predictions}
        
        return json.dumps(result)

@app.route('/home_station/remove_wrong_value')
def remove_wrong():
        td.remove_wrong_value()
        vd.remove_wrong_value()
        acd.remove_wrong_value()
        return ""

#@app.route('/home_station/clean')
#def home_station_clean():
#        clean_table();
#        return ""
        
@app.route('/home_station')
def home_station():
	return render_template('home_measure.html')

@app.route('/home_station/restart')
def home_station_restart():
	try:
		requests.get(home_station_url+"/restart")
	except:
		pass
	return "restarted"

@app.route('/covid')
def index():
	if 'username' in session:
		username = session['username']
	else:   username="anonymous"
	return render_template('login.html',name=username)

if __name__ == '__main__':
   import logging
   import logging.handlers
   handler = logging.handlers.RotatingFileHandler(
        'error.log',
        maxBytes=1024 * 1024)
   handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
   logging.getLogger('werkzeug').setLevel(logging.INFO)
   logging.getLogger('werkzeug').addHandler(handler)
   app.logger.setLevel(logging.WARNING) 
   app.logger.addHandler(handler)
   app.run(debug = True,host='0.0.0.0')     
