from flask import Flask,redirect,url_for,request,render_template
import os
import math
import json

def get_config(key):
    config_file = "/home/ksanjay02444/iot/config.json" # always use absolute path, not relative path
    file = open(config_file, "r")
    config = json.loads(file.read())
    file.close()
    
    if key in config:
        return config[key]
    else:
        raise Exception("Key {} is not found in config.json".format(key))

basename = get_config("basename")

app = Flask(__name__, static_folder='assets',static_url_path=basename)


@app.route(basename+"/helloworld")
def helloworld():
    return render_template('helloworld.html')


@app.route(basename+'/hello')
def hello_world():
    return "Hello World"

@app.route(basename+'/' , methods=['GET','POST'])
def welcome():
    return "Welcome to our website"

@app.route(basename+'/url')
def url():
    return 'www.google.com'

@app.route(basename+'/math/sqrt',methods=['GET','POST'])
def sqrt():
    return {
        "result": math.sqrt(int(request.form['num']))
    }

@app.route(basename+'/whoami')
def whoami():
    return os.popen('whoami').read()
@app.route(basename+'/cpuinfo')

def cpuinfo():
    if isadmin() == 'yes':
        # return redirect(url_for('error',errorcode=1000))
        # return redirect("http://google.com")
        return redirect(basename+'/error/1000')
        
    else:
        return "<pre>"+os.popen('cat /proc/cpuinfo').read()+"</pre>"

@app.route(basename+'/error/<int:errorcode>')
def error(errorcode):
    if errorcode == 1000:
        return "This app is Running with the root user, Which is Dangerous"
    elif errorcode == 1001:
        return "Some other error"
    else:
        return "unknown error"
# app.add_url_rule(basename+'/whoami','whoami',whoami)
# app.add_url_rule(basename+'/cpuinfo','cpuinfo',cpuinfo)

@app.route(basename+'/echo/<string>')
def echo(string):
    return f"{string}"

@app.route(basename+'/isadmin')
def isadmin():
    if whoami() == 'root\n':
        return "yes"
    else :
        return "no"

@app.route(basename+'/echo')
def null_echo():
    return "Please give enter some input : /echo/{string}"

# dynamic routing
@app.route(basename+'/pow/<int:a>/<int:b>')
def pow(a,b):
    try:
        return "The power of a and b is {}".format(math.pow(a,b))
    except:
        return "The given input is High"
@app.route(basename+'/path/<path:a>')
def path(a): 
    # return "<code>"+a+"</code>"
    return a 
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
    
 
 