from flask import Flask
app = Flask(__name__)

@app.route('/<name>')
def hello_user(name):
   return "<p><font color=\"red\">Hello %s</font></p>" % name

@app.route('/')
def hello_world():
   return "<p><font color=\"blue\">Hello World</font></p>"

if __name__ == '__main__':
   app.run(debug=True,host='0.0.0.0')
