from flask import Flask,session, redirect, url_for, request,render_template
#from inputpin import InputPin
from time import sleep
import json
from regressionaprox import aggregate_data,display_regions
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

@app.route('/')
def index():
	if 'username' in session:
		username = session['username']
	else:   username="anonymous"
	return render_template('login.html',name=username)
	
if __name__ == '__main__':
   import logging
   logging.basicConfig(filename='error.log',level=logging.INFO)
   app.run(debug = True,host='0.0.0.0')
