from flask import Flask,session, redirect, url_for, request,render_template
#from inputpin import InputPin
from time import sleep
import json
from regressionaprox import aggregate_data
app = Flask(__name__)
app.secret_key = '571ba9$#/~90'

@app.route('/data_retr')
def data_status():
	return "okay stubbed" #data_retr.showdata()

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name


"""
@app.route('/loginstatus.py')
def loginstatus():
	return myloginstatus.show()

@app.route('/login',methods = ['POST'])
def login():
   if request.method == 'POST':
           ed=Extractdata_Config("../config.txt")
           print(request.form['user_txt'])
           print(request.form['pass_txt'])
           if ed.getUsername() == request.form['user_txt'] and ed.testPassword(request.form['pass_txt']):
                session['username'] = ed.getUsername()
                print(session['username'])
                return "okay"
   return "error" #redirect('/')
"""
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

@app.route('/')
def index():
	if 'username' in session:
		username = session['username']
	else:   username="anonymous"
	return render_template('login.html',name=username)

"""
@app.route('/gauge_show')
def gauge_show():
	return render_template('gauge.html')

@app.route('/read_sensor/<sensor_type>/<pin>',methods=['GET'])
def read_sensor(sensor_type,pin):
        ip=InputPin(pin,sensor_type)
        return json.dumps(ip.show_sensor_data())

@app.route('/on')
def turnon():
	LED(47).on()

@app.route('/getconfigdata')
def getdata():
	return getconfigdata("../config.txt")

@app.route('/getpassworddata')
def getpassdata():
	return getpassworddata("../config.txt")

@app.route('/setconfigdata',methods = ['POST'])
def setdata():
        if request.method == 'POST':
                print("set config data method = post ")
                user = request.form['user']
                password = request.form['pass']
                ip = request.form['ip']
                port = request.form['port']
                refresh_in = request.form['refresh_in']
                refresh_out = request.form['refresh_out']
                logtime = request.form['logtime']
                print(str(user)+" "+str(password)+" "+str(ip)+" "+str(port)+" "+str(refresh_in)+" "+str(refresh_out)+" "+str(logtime))
                setconfigdata("../config.txt",user,password,ip,port,refresh_in,refresh_out,logtime)
                print("config data set")
                return "okay"

@app.route('/changeuserpassword',methods = ['POST'])
def setpass():
        if request.method == 'POST':
                user = request.form['user']
                password = request.form['pass']
                setpassword("../config.txt",user,password)
                print("config data set")
                return "okay"

@app.route('/getwifidata')
def getdata_wifi():
	return getwifidata("/etc/wpa_supplicant/wpa_supplicant.conf")

@app.route('/setwifidata',methods = ['POST'])
def setdata_wifi():
        if request.method == 'POST':
                print("set wifi data method = post ")
                ssid = request.form['wifi_ssid']
                psk = request.form['wifi_psk']
                print(str(ssid)+" "+str(psk))
                setwifidata("/etc/wpa_supplicant/wpa_supplicant.conf",ssid,psk)
                print("config wifi set")
                return "okay"

@app.route('/board_status')
def board_status():
	return 'temperature humidity pin settings'	

@app.route('/off')
def turnoff():
	LED(47).off()

@app.route('/logout')
def logout():
	session.pop('username',None)
	return redirect('/')
	
"""
if __name__ == '__main__':
   app.run(debug = True,host='0.0.0.0')

