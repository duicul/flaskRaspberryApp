from flask import Flask,session,url_for, request
def show():
	if 'username' in session:
		username = session['username']
		return str(username)
	else:
		return "anonymous"
