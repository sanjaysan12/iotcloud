from flask import Flask,redirect,url_for,request,render_template,session,Blueprint
from src.User import User
from src import get_config
from blueprints import home
bp = Blueprint("apiv1",__name__,url_prefix="/api/v1")

@bp.route("/auth",methods=['POST'])
def authenticate():
    if session.get('authenticated'):
        return{
            "message": "Already Authenticated",
            "authenticated": True
        },202
    else:
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            try:
                User.login(username,password)
                session['authenticated']=True
                
                # return {
                #     "message": "Successfully Authenticated",
                #     "authenticated": True
                # },200
                return redirect("/dashboard")
            except Exception as e:
                print("Login Failed",e)
                return {
                    "message": str(e),
                    "authenticated": False
                },401
        else:
            return {
                    "message": "Not enough parameters",
                    "authenticated": False
                },400
            
@bp.route("/deauth")
def deauth():
    if session.get('authenticated'):
        session['authenticated'] = False
        session.clear()
        return{
            "message": "Successfully Deauthed",
            "authenticated": False
        },200
        
    else:
        return{
            "message": "Already Deauthed",
            "authenticated": False
        },200
        
    
    
    
    