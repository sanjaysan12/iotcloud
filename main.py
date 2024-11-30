import sys
sys.path.append('/home/ksanjay02444/iot')
from flask import Flask,redirect,url_for,request,render_template,session
from src.User import User
from src import get_config
from blueprints import home,api,files




application = app = Flask(__name__, static_folder='assets',static_url_path="/")

app.secret_key = get_config("secret_key")
app.register_blueprint(home.bp)
app.register_blueprint(api.bp)
app.register_blueprint(files.bp)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=1111)
    
 
 