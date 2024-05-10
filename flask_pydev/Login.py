from flask import Flask,session,request,render_template,redirect, url_for,Response,jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json
#from inputpin import InputPin
#from time import sleep
import json
import os
import time
import speedmeasure

from datetime import datetime, timedelta
from regressionaprox import aggregate_data,display_regions
import requests
import traceback
from data_classes import Outside_Data,Temperature_Split_Data,Voltage_Data,AC_Data
from authorization import Authorization
from config_class import Config_Data,Config
from user_class import UserAnonym,LoginAttempt_Data,LoginAttempt
from flask_login import LoginManager,login_user,login_required,logout_user,current_user,login_url
import html
login_manager = LoginManager()


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(hours=1)
FlaskJSON(app)

home_station_url="http://192.168.1.6"
polling_period=1800
import logging.handlers
handler = logging.handlers.RotatingFileHandler(
        'logs/error_flask.log',
        backupCount=20,
        maxBytes=1024 * 1024)
handlerconsole = logging.StreamHandler()
handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
logging.getLogger('werkzeug').setLevel(logging.INFO)
logging.getLogger('werkzeug').addHandler(handler)
logging.getLogger('werkzeug').addHandler(handlerconsole)
app.logger.setLevel(logging.WARNING) 
app.logger.addHandler(handler)
login_manager.init_app(app)
login_manager.anonymous_user = UserAnonym
login_manager.login_view = 'login'

tsd=Temperature_Split_Data("db/measure.db",'werkzeug')
vd=Voltage_Data("db/measure.db",'werkzeug')
acd=AC_Data("db/measure.db",'werkzeug')
od=Outside_Data("db/measure.db",'werkzeug')
aut=Authorization()
cd=Config_Data("db/config.db",'werkzeug')
lad=LoginAttempt_Data("db/loginattempt.db",'werkzeug')
attempt_period=timedelta(hours=4)

max_attempts=5
@app.errorhandler(401)
def custom_401(error):
    return Response('<Why access is denied string goes here...>', 401, {'WWW-Authenticate':'Basic realm="Login Required"'})

#@app.before_request
#def make_session_permanent():
#    session.permanent = True
#    app.permanent_session_lifetime = timedelta(minutes=30)

@login_manager.unauthorized_handler
def unauthorized():
    if request.method == 'GET':
        return redirect(login_url('/home_station', request.url))
    else:
        return dict(error=True, message="Please log in for access."), 403

@login_manager.user_loader
def load_user(user_id):
    user = aut.user_data.getUser(user_id)
    return user

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_station'))

@app.route('/change_password',methods = ['POST'])
@login_required
def change_password():
    user = current_user.user_name
    try:
        user_name = user
        password = html.escape(request.form['password_change'])
        mail = html.escape(request.form['mail_change'])
        confirm_password = html.escape(request.form['confirm_password_change'])
        if(password != confirm_password):
            return redirect(url_for('home_station_config'))
        aut.removeUser(user_name)
        aut.registerUser(user_name, password, mail)
    except:
        logging.getLogger('werkzeug').error(str(traceback.format_exc()))
        return redirect(url_for('home_station'))
    session.clear()
    return redirect(url_for('home_station'))

@app.route('/register',methods = ['POST'])
@login_required
def register():
    session.clear()
    try:
        user_name = html.escape(request.form['user_name_register'])
        password = html.escape(request.form['password_register'])
        confirm_password = html.escape(request.form['confirm_password_register'])
        if(password != confirm_password):
            return redirect(url_for('home_station_config'))
        mail = html.escape(request.form['mail_register'])
        aut.removeUser(user_name)
        aut.registerUser(user_name, password, mail)
    except:
        logging.getLogger('werkzeug').error(str(traceback.format_exc()))
    return redirect(url_for('home_station'))


@app.route('/login',methods = ['POST'])
def login():
    try:
        user_name = html.escape(request.form['user_name'])
        password = html.escape(request.form['password'])
        remember=False
        try:
            remember = html.escape(request.form['remember'])
        except:
            logging.getLogger('werkzeug').info("remeber is False")
        epochtime=time.mktime((datetime.now()-attempt_period).timetuple())
        user = aut.loginUser(user_name, password,request.remote_addr,epochtime)
        if(user != None):
            if(user.countReached()):
                return redirect(url_for('home_station'))
            remember_duration = timedelta(days=20) if remember else None 
            if(user.is_authenticated):
                lad.addAttempt(LoginAttempt(user_name,request.remote_addr,None,True))
            else:
                lad.addAttempt(LoginAttempt(user_name,request.remote_addr,None,False))               
            login_user(user,True,remember_duration)
        else:
            lad.addAttempt(LoginAttempt(user_name,request.remote_addr,None,False))
         
    except:
        lad.addAttempt(LoginAttempt(user_name,request.remote_addr,None,False))
        logging.getLogger('werkzeug').error(str(traceback.format_exc()))
    return redirect(url_for('home_station'))

@app.route('/get_login_attempts')
@login_required
def get_login_attempts():
    la = list(map(lambda l : l.toJSON(),lad.getAllAttemptsUser(current_user.user_name, None)))
    la.reverse()
    return jsonify(la)

@app.route('/current_timestamp')
@login_required
def current_timestamp():
    return str(tsd.current_timestamp())


@app.route('/cpu_gpu_temp')
@login_required
def cpu_gpu_temp():
    temps = os.popen('vcgencmd measure_temp').read().replace("\n","<br>")
    return temps

@app.route('/memory_usage')
@login_required
def memory_usage():
    memory = os.popen('free -ht').read().replace("\n","<br>").replace(" ","&nbsp;&nbsp;")
    return memory

@app.route('/disk_usage')
@login_required
def disk_usage():
    memory = os.popen('df -H').read().replace("\n","<br>").replace(" ","&nbsp;&nbsp;")
    return memory

@app.route('/data_retr')
@login_required
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
        countries=json.loads(html.escape(request.form['countries']))
        #print(countries)
        return aggregate_data(pol_grade,countries,data_type,case_type,predict_len,api)

@app.route('/covid_data/<case_type>/<api>/<data_type>',methods = ['POST'])
def extract_data(api,case_type,data_type):
        countries=json.loads(html.escape(request.form['countries']))
        return aggregate_data(0,countries,data_type,case_type,0,api)

@app.route('/regions/<case_type>/<api>/<data_type>',methods = ['POST'])
def extract_regions(api,case_type,data_type):
        countries=json.loads(html.escape(request.form['countries']))
        ret = display_regions(countries,data_type,case_type,api)
        return ret

@app.route('/force_poll')
@login_required
def force_poll():
    user = current_user.user_name
    if(user!=None):
        config=cd.getConfig(user)
        tsd.poll_value(config.url)
        vd.poll_value(config.url)
        acd.poll_value(config.url)
        od.poll_value()
    return ""

@app.route('/convert_old')
@login_required
def convert_old():
    user=current_user.user_name
    if(user!=None):
        config=cd.getConfig(user)
        tsd.convert_old(config.url)
    return "success"
    
@app.route('/temperature')
@login_required
def temperature():
    data=tsd.extract_last()
    if data==None:
        return jsonify({})
    return jsonify(data)#{"date":data[1],"temp1":data[2],"temp2":data[3]}

@app.route('/home_station/powmr')
@login_required
def powmr_poll():
    try:
        return jsonify(requests.get("https://192.168.0.11/powmr"))      
    except:
        return "error"
    
@app.route('/voltage')
@login_required
def voltage():
    data=vd.extract_last()
    if data==None:
        return jsonify({})
    return jsonify({"date":data[1],"volt1":data[2]})

def reset_config_weather():
    file_json={"api_key":"random","city":"random"}
    file=open("json/config_weather.json","w")
    json.dump(file_json,file)
    file.close()

@app.route('/weather')
@login_required
def weather():
    return jsonify(od.poll_value())

@app.route('/ac')
@login_required
def ac():
    data=acd.extract_last()
    if data==None:
        return jsonify({})
    return jsonify({"date":data[1],"voltage":data[2],"current":data[3],"power":data[4],"energy":data[5]})

@app.route('/home_station/voltage_data')
@login_required
def home_station_voltage_data():
    volt=[]
    interval=False
    compare=False
    try:
        interval=True if request.args["interval"] == "true" else False
    except:
        pass
    try:
        compare=True if request.args["compare"] == "true" else False
    except:
        pass
    if(interval):
        try:
            volt = vd.extract_all_between(request.args["fdate"], request.args["ldate"])
        except:
            logging.error(str(traceback.format_exc()))
        t=[]
        for i in volt:
            t.append({"date":i[1],"volt1":i[2]})    
        return jsonify(t)
    elif(compare):
        try:
            data = vd.extractCompare(request.args["date1"], request.args["date2"])
        except:
            logging.error(str(traceback.format_exc()))
        t=[]
        for i in data:
            t.append({"date":i[1],"volt1":i[2]})
        return jsonify(t)
    else:
        try:
            volt = vd.extract_all_interval(request.args["items"])
        except:
            logging.error(str(traceback.format_exc()))
        #print(data)
        t=[]
        for i in volt:
            t.append({"date":i[1],"volt1":i[2]})    
        return jsonify(t)
    

@app.route('/home_station/ac_data')
@login_required
def home_station_ac_data():
    data=[]
    interval=False
    compare=False
    try:
        interval=True if request.args["interval"] == "true" else False
    except:
        pass
    try:
        compare=True if request.args["compare"] == "true" else False
    except:
        pass
    if(interval):
        try:
            data = acd.extract_all_between(request.args["fdate"], request.args["ldate"])
        except:
            logging.error(str(traceback.format_exc()))
        t=[]
        for i in data:
            t.append({"date":i[1],"voltage":i[2],"current":i[3],"power":i[4],"energy":i[5]})    
        return jsonify(t)
    elif(compare):
        try:
            data = acd.extractCompare(request.args["date1"], request.args["date2"])
        except:
            logging.error(str(traceback.format_exc()))
        t=[]
        for i in data:
            t.append({"date":i[1],"voltage":i[2],"current":i[3],"power":i[4],"energy":i[5]})    
        return jsonify(t)
    else:
        try:
            data = acd.extract_all_interval(request.args["items"])
        except:
            logging.error(str(traceback.format_exc()))
        t=[]
        for i in data:
            t.append({"date":i[1],"voltage":i[2],"current":i[3],"power":i[4],"energy":i[5]})    
        return jsonify(t)
       
@app.route('/home_station/temperature_data')
@login_required
def  home_station_temperature_data():
    temp=[]
    interval=False
    compare=False
    try:
        interval=True if request.args["interval"] == "true" else False
    except:
        pass
    try:
        compare=True if request.args["compare"] == "true" else False
    except:
        pass
    if(interval):
        try:
            temp = tsd.extract_all_between(request.args["fdate"], request.args["ldate"])
        except:
            logging.error(str(traceback.format_exc()))
        t={}
        for id in range(1,11):
            t[str(id)]=[{"date":i[1],"value":i[3]} for i in list(filter(lambda i :i[2]==id,temp))]
            print(t)
        result={"recorded":t,"predict":[]}
        return jsonify(result)
    elif(compare):
        try:
            temp = tsd.extractCompare(request.args["date1"], request.args["date2"])
        except:
            logging.error(str(traceback.format_exc()))
        t={}
        for id in range(1,11):
            t[str(id)]=[{"date":i[1],"value":i[3]} for i in list(filter(lambda i :i[2]==id,temp))]
            print(t)
        result={"recorded":t,"predict":[]}
        return jsonify(result)
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
        return jsonify(result)
    
@app.route('/home_station')
def home_station():    
    try:
        epochtime=time.mktime((datetime.now()-attempt_period).timetuple())
        logins=logins = len(list(filter(lambda logatt:not logatt.success,lad.getAllAttemptsIp(request.remote_addr, epochtime))))
        current_user.attempts=logins
        if(not current_user.is_authenticated):
            return render_template("login.html")
        else:
            return render_template('home_measure.html')
    except:
        logging.getLogger('werkzeug').error(str(traceback.format_exc()))
        return render_template('login.html')

@app.route('/home_station/get_config')
@login_required
def home_station_get_config():    
    user = current_user.user_name
    config=cd.getConfig(user)
    return jsonify(config.toJSON())

@app.route('/home_station/update_config',methods = ['POST'])
@login_required
def home_station_update_config():    
    user = current_user.user_name
    url = html.escape(request.form['url'])
    period = html.escape(request.form['period'])
    c = Config(user,url,period)
    cd.updateConfig(c)
    print(c)
    return render_template('config.html')
    
@app.route('/home_station/config')
@login_required
def home_station_config():
    user_name = current_user.user_name
    try:
        print(user_name)
        if(user_name == None):
            return render_template("login.html")
        else:
            return render_template('config.html')
    except:
        logging.getLogger('werkzeug').error(str(traceback.format_exc()))
        return render_template('login.html') 
    
@app.route('/home_station/control')
@login_required
def home_station_control():
    try:
        user_name = current_user.user_name
        print(user_name)
        if(user_name == None):
            return render_template("login.html")
        else:
            return render_template('control.html')
    except:
        logging.getLogger('werkzeug').error(str(traceback.format_exc()))
        return render_template('login.html') 
    
@app.route('/home_station/login_attempt')
@login_required
def home_station_login_attempt():
    try:
        user_name = current_user.user_name
        print(user_name)
        if(user_name == None):
            return render_template("login.html")
        else:
            return render_template('loginattempt.html')
    except:
        logging.getLogger('werkzeug').error(str(traceback.format_exc()))
        return render_template('login.html')

@app.route('/home_station/restart')
@login_required
def home_station_restart():
    try:
        requests.get(home_station_url+"/restart")
    except:
        pass
    return "restarted"

@app.route('/home_station/remove_wrong_value')
@login_required
def remove_wrong_value():
    tsd.remove_wrong_value()
    acd.remove_wrong_value()
    vd.remove_wrong_value()
    return ""

@app.route('/speed_test/<tries>',methods = ['GET'] )
@as_json
def speed_test_one(tries):
    try:
        tries=int(tries)
    except:
        tries = 1
    if(tries>5):
        tries = 5
    data = speedmeasure.run_test(tries)
    return data

@app.route('/speed_test',methods = ['GET'] )
@as_json
def speed_test():
    data = speedmeasure.run_test(1)
    return data

@app.route('/covid')
def index():
    if 'username' in session:
        username = session['username']
    else:   username="anonymous"
    return render_template('covid.html',name=username)

if __name__ == '__main__':
    app.run(debug = True,host='0.0.0.0')     
