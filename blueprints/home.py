from flask import Flask,redirect,url_for,request,render_template,session,Blueprint,jsonify

bp = Blueprint("home",__name__,url_prefix="/")

@bp.route("/")
def home():
    return "Iam Home"

@bp.route("/info")
def info():
  
    client_ip = request.remote_addr
    user_agent = request.user_agent.string
    headers = dict(request.headers)
    response_data = {
        'client_ip': client_ip,
        'user_agent': user_agent,
        'headers': headers  # Include all headers for inspection if needed
    }
    return jsonify(response_data)


@bp.route("/dashboard")
def dashboard():
    
    return render_template('_master.html',session =session)