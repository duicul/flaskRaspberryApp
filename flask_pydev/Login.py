from flask import Flask,session,request,render_template
#from inputpin import InputPin
#from time import sleep
import json
from regressionaprox import aggregate_data,display_regions
import requests
from monitor import extract_all_interval,extract_last,poll_value,remove_wrong_value
import traceback
app = Flask(__name__)
app.secret_key = '571ba9$#/~90'

home_station_url="http://192.168.1.6"
polling_period=1800

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
        poll_value(home_station_url)
        return ""

@app.route('/temperature')
def temperature():
        data=extract_last()
        if data==None:
                return {}
        #print(data)
        #r = requests.get(home_station_url+"/temperature")
        return {"date":data[1],"temp1":data[2],"temp2":data[3]}
        

@app.route('/voltage')
def voltage():
        data=extract_last()
        if data==None:
                return {}
        #print(data)
        #r = requests.get(home_station_url+"/voltage")
        return {"date":data[1],"volt1":data[4]}


@app.route('/home_station/data')
def home_station_data():
        items=int(request.args["items"])
        #print(items)
        try:
                data = extract_all_interval(items)
        except:
                logging.error(str(traceback.format_exc()))
                data=[]
        #print(data)
        t=[]
        for i in data:
            t.append({"date":i[1],"temp1":i[2],"temp2":i[3],"volt1":i[4]})    
        return json.dumps(t)

@app.route('/home_station/remove_wrong_value')
def remove_wrong():
        remove_wrong_value();
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
	requests.get(home_station_url+"/restart")

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
