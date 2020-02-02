from app import app
from flask import request
import dateutil.parser as parser
import geopy.distance as geo
import random
from flask import jsonify
import time
import datetime

@app.route('/')
def default():
    return 'Home'

user_dict = {'Dylan':'nmf', 'Chris':'tu', 'Nick':'ts'}
in_session = {}
path_dict = {'Dylan': {1580040000: (33.649888, -117.839939)}, 'Chris': {1580040000: (33.649888, -117.839839)}, 'Nick': {1580040000: (33.649888, -117.839939)}}#{'Dylan':{}, 'Chris':{}, 'Nick':{}}
disease_dict = {'influenza':5760, 'coronavirus':20160}
sick_dict = {'Dylan':{}, 'Chris':{}, 'Nick':{}}
maybe_cont = {'Dylan':[], 'Chris':[], 'Nick':[]}
stats = {'location':{'timestamp':"2020-01-26T012:00:00.000Z",'coords':{'latitude':33.649888, 'longitude':-117.839839}}}

def time_convert(time):
    return int(parser.parse(time).strftime('%s'))//60

def coord_convert(a,b):
    return float(geo.distance(a,b).km)//0.001

@app.route('/test')
def test():
    raise

@app.route('/login')
def login(): 
    global session
    username = request.args.get('user')
    password = request.args.get('pass')

    if (username in user_dict):
        if (password == user_dict[username]):
            if (username not in in_session.values()):
                while True:
                    session = random.randint(0,100)
                    if (session not in in_session):
                        break
                in_session[session] = username
                stats['auth_token'] = session
                if (len(maybe_cont[username]) > 0):
                    return jsonify({'sick': maybe_cont[username], 'id': session})
                return jsonify({'id': session})
            return jsonify({'error':'user already logged in'})
        return jsonify({'error':'incorrect password'})
    return jsonify({'error':'incorrect username and/or password'})

@app.route('/refresh')
def refresh():
    session_id = int(request.args.get('id'))
    if (session_id in in_session):
        return jsonify(maybe_cont[in_session[session_id]])
    return 'uhoh'

@app.route('/logout')
def logout():
    session_id = int(request.args.get('id'))
    if (session_id in in_session):
        del in_session[session_id]
    return 'success'
    
@app.route('/track', methods=['GET', 'POST'])
def track():
    session_id = int(stats['auth_token'])
    time = time_convert(stats['location']['timestamp'])
    location = (stats['location']['coords']['latitude'], stats['location']['coords']['longitude'])
    
    if (session_id in in_session):
        path_dict[in_session[session_id]][time] = location
        return 'a'
    else:
        return jsonify({'error':'invalid session id'})

@app.route('/sick')
def sick():
    session_id = int(request.args.get('id'))
    disease = request.args.get('d')
    ti = request.args.get('time')
    tyme = (time.mktime(datetime.datetime.strptime(ti, "%m/%d/%Y").timetuple()))//60
    try:
        user = in_session[session_id]
    except KeyError:
        return jsonify({'error':'invalid session id'})

    if (disease in disease_dict):
        sick_dict[user][disease] = (tyme - disease_dict[disease])
    else:
        return jsonify({'error':'invalid disease'})
    cont_times = [t for t in path_dict[user] if t >= sick_dict[user][disease]]
    for person in user_dict:
        if (person != in_session[session_id]):
            for t in cont_times:
                if t in path_dict[person] and (coord_convert(path_dict[user][t], path_dict[person][t]) <= 10):
                    maybe_cont[person].append({'disease':disease, 'time_met':t, 'time_reported':time.time()//1, 'coords':path_dict[user][t], 'distance':coord_convert(path_dict[user][t], path_dict[person][t])})
                    break
    return jsonify(maybe_cont)

@app.route('/cured')
def cured():
    session_id = int(request.args.get('id'))
    disease = request.args.get('d')
    try:
        user = in_session[session_id]
    except KeyError:
        return jsonify({'error':'invalid session id'})

    if (disease in sick_dict[user]):
        del sick_dict[user][disease]
    else:
        return jsonify({'error':'invalid disease'})

#http://127.0.0.1:5000/login?user=Dylan&pass=nmf
