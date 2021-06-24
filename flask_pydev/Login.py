from flask import Flask,session,request,render_template,redirect, url_for,Response
#from inputpin import InputPin
#from time import sleep
import json
import os
from regressionaprox import aggregate_data,display_regions
import requests
import traceback
from data_classes import Outside_Data,Temperature_Split_Data,Voltage_Data,AC_Data
from authorization import Authorization
from datetime import timedelta
from config_class import Config_Data,Config_Handler

app = Flask(__name__)
app.secret_key = '571ba9$#/~90'

home_station_url="http://192.168.1.6"
polling_period=1800
import logging.handlers
handler = logging.handlers.RotatingFileHandler(
        'logs/error_flask.log',
        backupCount=20,
        maxBytes=1024 * 1024)
handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
logging.getLogger('werkzeug').setLevel(logging.INFO)
logging.getLogger('werkzeug').addHandler(handler)
app.logger.setLevel(logging.WARNING) 
app.logger.addHandler(handler)

tsd=Temperature_Split_Data("measure.db",'werkzeug')
vd=Voltage_Data("measure.db",'werkzeug')
acd=AC_Data("measure.db",'werkzeug')
od=Outside_Data("measure.db",'werkzeug')
aut=Authorization()

cd=Config_Data("config.db",'werkzeug')

@app.errorhandler(401)
def custom_401(error):
    return Response('<Why access is denied string goes here...>', 401, {'WWW-Authenticate':'Basic realm="Login Required"'})

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_station'))

@app.route('/login',methods = ['POST'])
def login():
    att = 0
    try:
        att=session["attempt"]
    except:
        session["attempt"]=0
        pass
    session["attempt"]=att+1
    if(att>5):
        return redirect(url_for('home_station'))
    try:
        user_name = request.form['user_name']
        password = request.form['password']
        user = aut.loginUser(user_name, password)
        if(user != None):
            session["attempt"]=0
            session["user_name"]=user_name
    except:
        logging.getLogger('werkzeug').error(str(traceback.format_exc()))
    return redirect(url_for('home_station'))
    
@app.route('/current_timestamp')
def current_timestamp():
    try:
        user = session["user_name"]
    except:
        return redirect(url_for('home_station'))
    return str(tsd.current_timestamp())


@app.route('/cpu_gpu_temp')
def cpu_gpu_temp():
    try:
        user = session["user_name"]
    except:
        return redirect(url_for('home_station'))
    temps = os.popen('vcgencmd measure_temp').read().replace("\n","<br>")
    return temps

@app.route('/memory_usage')
def memory_usage():
    try:
        user = session["user_name"]
    except:
        return redirect(url_for('home_station'))
    memory = os.popen('free -ht').read().replace("\n","<br>").replace(" ","&nbsp;&nbsp;")
    return memory

@app.route('/disk_usage')
def disk_usage():
    try:
        user = session["user_name"]
    except:
        return redirect(url_for('home_station'))
    memory = os.popen('df -H').read().replace("\n","<br>").replace(" ","&nbsp;&nbsp;")
    return memory

@app.route('/data_retr')
def data_status():
    try:
        user = session["user_name"]
    except:
        return redirect(url_for('home_station'))
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
        countries=json.loads(request.form['countries'])
        return aggregate_data(0,countries,data_type,case_type,0,api)

@app.route('/regions/<case_type>/<api>/<data_type>',methods = ['POST'])
def extract_regions(api,case_type,data_type):
        countries=json.loads(request.form['countries'])
        ret = display_regions(countries,data_type,case_type,api)
        return ret

@app.route('/force_poll')
def force_poll():
    user = None
    try:
        user = session["user_name"]
    except:
        return redirect(url_for('home_station'))
    if(user!=None):
        config=cd.getConfig(user)
        tsd.poll_value(config.url)
        vd.poll_value(config.url)
        acd.poll_value(config.url)
        od.poll_value(config.url)
    return ""

@app.route('/convert_old')
def convert_old():
    user=None
    try:
        user = session["user_name"]
    except:
        return redirect(url_for('home_station'))
    if(user!=None):
        config=cd.getConfig(user)
        tsd.convert_old(config.url)
    return "success"
    
@app.route('/temperature')
def temperature():
    try:
        user = session["user_name"]
    except:
        return redirect(url_for('home_station'))
    data=tsd.extract_last()
    if data==None:
        return {}
    return str(data)#{"date":data[1],"temp1":data[2],"temp2":data[3]}
        

@app.route('/voltage')
def voltage():
    try:
        user = session["user_name"]
    except:
        return redirect(url_for('home_station'))
    data=vd.extract_last()
    if data==None:
        return {}
    return json.dumps({"date":data[1],"volt1":data[2]})

def reset_config_weather():
    try:
        user = session["user_name"]
    except:
        return redirect(url_for('home_station'))
    file_json={"api_key":"random","city":"random"}
    file=open("config_weather.json","w")
    json.dump(file_json,file)
    file.close()

@app.route('/weather')
def weather():
    try:
        user = session["user_name"]
    except:
        return redirect(url_for('home_station'))
    return json.dumps(od.poll_value())

@app.route('/ac')
def ac():
    try:
        user = session["user_name"]
    except:
        return redirect(url_for('home_station'))
    data=acd.extract_last()
    if data==None:
        return {}
    return json.dumps({"date":data[1],"voltage":data[2],"current":data[3],"power":data[4],"energy":data[5]})

@app.route('/home_station/voltage_data')
def home_station_voltage_data():
    try:
        user = session["user_name"]
    except:
        return redirect(url_for('home_station'))
    volt=[]
    interval=False
    try:
        interval=True if request.args["interval"] == "true" else False
    except:
        pass
    if(interval):
        try:
            volt = tsd.extract_all_between(request.args["fdate"], request.args["ldate"])
        except:
            logging.error(str(traceback.format_exc()))
    else:
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
    try:
        user = session["user_name"]
    except:
        return redirect(url_for('home_station'))
    data=[]
    interval=False
    try:
        interval=True if request.args["interval"] == "true" else False
    except:
        pass
    if(interval):
        try:
            data = acd.extract_all_between(request.args["fdate"], request.args["ldate"])
        except:
            logging.error(str(traceback.format_exc()))
    else:
        try:
            data = acd.extract_all_interval(request.args["items"])
        except:
            logging.error(str(traceback.format_exc()))
    t=[]
    for i in data:
        t.append({"date":i[1],"voltage":i[2],"current":i[3],"power":i[4],"energy":i[5]})    
    return json.dumps(t)
       
@app.route('/home_station/temperature_data')
def  home_station_temperature_data():
    try:
        user = session["user_name"]
    except:
        return redirect(url_for('home_station'))
    temp=[]
    interval=False
    try:
        interval=True if request.args["interval"] == "true" else False
    except:
        pass
    if(interval):
        try:
            temp = tsd.extract_all_between(request.args["fdate"], request.args["ldate"])
        except:
            logging.error(str(traceback.format_exc()))
    else:
        try:
            temp = tsd.extract_all_interval(request.args["items"])
        except:
            logging.getLogger('werkzeug').error(str(traceback.format_exc()))
    t={}
    for id in range(1,11):
        t[str(id)]=[{"date":i[1],"value":i[3]} for i in list(filter(lambda i :i[2]==id,temp))]
    print(t)
    result={"recorded":t,"predict":[]}
        
    return json.dumps(result)
        
@app.route('/home_station')
def home_station():
    attempt=0
    try:
        attempt = session["attempt"]
    except:
        pass
    session["attempt"] = attempt
        
    user_name = None
    try:
        user_name = session["user_name"]
        print(user_name)
        if(user_name == None):
            return render_template("login.html")
        else:
            return render_template('home_measure.html')
    except:
        logging.getLogger('werkzeug').error(str(traceback.format_exc()))
        return render_template('login.html')    

@app.route('/home_station/restart')
def home_station_restart():
    try:
        user = session["user_name"]
    except:
        return redirect(url_for('home_station'))
    try:
        requests.get(home_station_url+"/restart")
    except:
        pass
    return "restarted"

@app.route('/home_station/remove_wrong_value')
def remove_wrong_value():
    try:
        user = session["user_name"]
    except:
        return redirect(url_for('home_station'))
    tsd.remove_wrong_value()
    acd.remove_wrong_value()
    vd.remove_wrong_value()
    return ""

@app.route('/covid')
def index():
    try:
        user = session["user_name"]
    except:
        return redirect(url_for('home_station'))
    if 'username' in session:
        username = session['username']
    else:   username="anonymous"
    return render_template('covid.html',name=username)

if __name__ == '__main__':
    app.run(debug = True,host='0.0.0.0')     
