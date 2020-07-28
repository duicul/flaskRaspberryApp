from flask import Flask,session,request,render_template
#from inputpin import InputPin
#from time import sleep
import json
from regressionaprox import aggregate_data,display_regions
import requests
import traceback
from data_classes import Temperature_Data,Voltage_Data,AC_Data

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


@app.route('/ac')
def ac():
        data=vd.extract_last()
        if data==None:
                return {}
        #print(data)
        #r = requests.get(home_station_url+"/voltage")
        return {"date":data[1],"voltage":data[2],"current":data[3],"power":data[4],"energy":data[5]}

@app.route('/home_station/voltage_data')
def home_station_voltage_data():
        items=int(request.args["items"])
        volt=[]
        try:
                volt = vd.extract_all_interval(items)
        except:
                logging.error(str(traceback.format_exc()))
        #print(data)
        t=[]
        for i in volt:
            t.append({"date":i[1],"volt1":i[2]})    
        return json.dumps(t)

@app.route('/home_station/ac_data')
def home_station_ac_data():
        items=int(request.args["items"])
        #print(items)
        temp=[]
        try:
                data = acd.extract_all_interval(items)
        except:
                logging.error(str(traceback.format_exc()))
        #print(data)
        t=[]
        for i in data:
            t.append({"date":i[1],"voltage":i[2],"current":i[3],"power":i[4],"energy":i[5]})    
        return json.dumps(t)
       
@app.route('/home_station/temperature_data')
def  home_station_temperature_data():
        items=int(request.args["items"])
        #print(items)
        temp=[]
        try:
                temp = td.extract_all_interval(items)
        except:
                logging.error(str(traceback.format_exc()))
        #print(data)
        t=[]
        for i in temp:
            t.append({"date":i[1],"temp1":i[2],"temp2":i[3]})    
        return json.dumps(t)

@app.route('/home_station/remove_wrong_value')
def remove_wrong():
        td.remove_wrong_value();
        vd.remove_wrong_value()
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
