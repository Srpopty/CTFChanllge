import base64
import cPickle
import hashlib
import json
import os
import re
import sqlite3
import time
from contextlib import closing

from flask import Flask, g, make_response, render_template, request, session, abort
from flask_session import Session
from jinja2 import Environment

Jinja2 = Environment()
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/opt/session/'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_FILE_THRESHOLD'] = 500
app.config['SESSION_FILE_MODE'] = 384
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_COOKIE_NAME'] = 'PHPSESSID'
black_list = [
    'app', '.py', 'kill', 'shutdown', 'rm', '.sql', '>', '.log', '.db', 'session', 'database', 'base', 'hex'
]
methods = ['get', 'post', 'head', 'put', 'delete', 'options']
sess = Session()
sess.init_app(app)
SALT = '_Y0uW1llN3verKn0w1t_'


def connect_db():
    return sqlite3.connect('/opt/database/confusion2.db')


def init_db():
    if os.path.exists('/opt/database/confusion2.db') is False:
        with closing(connect_db()) as db:
            with app.open_resource('init.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


# Fake PHP :>
def handle_response(response):
    response.headers['Server'] = 'Apache/2.4.10 (Debian)'
    response.headers['X-Powered-By'] = 'PHP/7.1.7'
    return response


def redirect(url, msg=''):
    strings = '<script>alert("%s");window.location.href="%s";</script>' % (
        msg, url) if msg != '' else '<script>window.location.href="%s";</script>' % url
    return handle_response(make_response(strings, 302))


def base64_url_encode(text):
    return base64.b64encode(text).replace('+', '-').replace('/', '_').replace('=', '')


def base64_url_decode(text):
    text = text.replace('-', '+').replace('_', '/')
    while True:
        try:
            result = base64.b64decode(text)
        except TypeError:
            text += '='
        else:
            break
    return result


def create_jwt(data, kid):
    jwt_header = base64_url_encode(
        '{"typ":"JWT","alg":"sha256","kid":"%s"}' % kid)
    jwt_payload = base64_url_encode('{"data":"%s"}' % data)
    jwt_signature = base64_url_encode(hashlib.sha256(
        jwt_header + '.' + jwt_payload + SALT).hexdigest())
    return jwt_header + '.' + jwt_payload + '.' + jwt_signature


def verify_jwt(jwt):
    jwt = jwt.split('.')
    if len(jwt) == 3:
        return jwt[2] == base64_url_encode(hashlib.sha256(jwt[0] + '.' + jwt[1] + SALT).hexdigest())
    else:
        return False


def unserialize(data):
    if data[:32] == 'O:4:"User":2:{s:9:"user_data";s:':
        data = data.split(':')
        if int(data[7]) == len(data[8][1:-3]):
            return cPickle.loads(str(data[8][1:-3]))
    return None


def check_username(username):
    return re.match(r'^[A-Za-z0-9_]+$', username) is not None


@app.before_request
def before_request():
    try:
        g.db = connect_db()
        with open('/opt/log/access.log', 'ab') as log:
            log.write(
                '%s --- [ %s ] "%s %s %s" --- %s --- %s --- %s -\n' % (
                    request.environ['REMOTE_ADDR'],
                    time.strftime("%d/%B/%Y %H:%M:%S", time.localtime()),
                    request.environ['REQUEST_METHOD'],
                    request.full_path,
                    request.environ['SERVER_PROTOCOL'],
                    repr(request.cookies),
                    repr(request.form)[19:-1],
                    repr(request.headers)[15:-1],
                )
            )
    except Exception as e:
        with open('/opt/log/error.log', 'ab') as log:
            log.write(e.message + '\n')
        abort(500)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/.htaccess')
def forbidden():
    return handle_response(make_response(
        render_template(
            '403.html',
            error_url=request.path,
            server_name=request.host.split(':')[0],
            server_port=int(request.host.split(':')[1])),
        403)
    )


@app.errorhandler(404)
def not_found(error):
    return handle_response(make_response(
        render_template(
            '404.html',
            error_url=request.path,
            server_name=request.host.split(':')[0],
            server_port=int(request.host.split(':')[1])),
        404)
    )


@app.errorhandler(500)
def internal_error(error):
    return handle_response(make_response(
        render_template(
            '500.html',
            error_url=request.path,
            server_name=request.host.split(':')[0],
            server_port=int(request.host.split(':')[1])),
        500)
    )


@app.route('/', methods=methods)
@app.route('/index.php', methods=methods)
def index():
    try:
        if 'login' in session and 'token' in request.cookies.keys():
            if verify_jwt(request.cookies['token']) is True:
                data = json.loads(base64_url_decode(
                    request.cookies['token'].split('.')[1]))['data']
                for bad_string in black_list:
                    if bad_string in data:
                        session.pop('login', None)
                        return redirect('/login.php', 'Do not JIAOSHI! You can not use it. Please login again.')
                data = unserialize(data)
                if data is not None:
                    return handle_response(make_response(render_template('home.html', username=data[0])))
                else:
                    session.pop('login', None)
                    return redirect('/login.php', 'Invalid data! Please login again.')
            else:
                session.pop('login', None)
                return redirect('/login.php', 'Invalid token! Please login again.')
        else:
            return handle_response(make_response(render_template('index.html')))
    except Exception as e:
        with open('/opt/log/error.log', 'ab') as log:
            log.write(e.message + '\n')
        abort(500)


@app.route('/logout.php', methods=methods)
def logout():
    try:
        session.pop('login', None)
        return redirect('/index.php')
    except Exception as e:
        with open('/opt/log/error.log', 'ab') as log:
            log.write(e.message + '\n')
        abort(500)


@app.route('/login.php', methods=methods)
def login():
    try:
        if 'login' in session:
            return redirect('/index.php')
        if request.method == 'POST':
            if ('username' in request.form.keys() and isinstance(request.form['username'], basestring)) and (
                    'password' in request.form.keys() and isinstance(request.form['password'], basestring)):
                if 'verify' in session and hashlib.md5(request.form['verify']).hexdigest()[:6] == session.pop('verify', None):
                    username = request.form['username']
                    if check_username(username) is True:
                        password = hashlib.md5(
                            request.form['password']).hexdigest()
                        query_result = query_db(
                            'select id, password from users where username = ?', (username,))
                        if len(query_result) != 0 and query_result[0]['password'] == password:
                            pickle_data = cPickle.dumps([username, password])
                            data = json.dumps(
                                'O:4:"User":2:{s:9:"user_data";s:%d:"%s";}' % (len(pickle_data), pickle_data))[1:-1]
                            resp = redirect('/index.php', 'Login success!')
                            resp.set_cookie('token', create_jwt(
                                data, query_result[0]['id']))
                            session['login'] = True
                            return resp
                        else:
                            return redirect('/login.php', 'Username or password error!')
                    else:
                        return redirect('/login.php', 'Invalid username!')
                else:
                    return redirect('/login.php', 'Invalid verify!')
        session['verify'] = hashlib.md5(os.urandom(24)).hexdigest()[:6]
        return handle_response(make_response(render_template('login.html', verify=session['verify'])))
    except Exception as e:
        with open('/opt/log/error.log', 'ab') as log:
            log.write(e.message + '\n')
        abort(500)


@app.route('/register.php', methods=methods)
def register():
    try:
        if 'username' in session:
            return redirect('/index.php')
        if request.method == 'POST':
            if ('username' in request.form.keys() and isinstance(request.form['username'], basestring)) and (
                    'password' in request.form.keys() and isinstance(request.form['password'], basestring)) and (
                    'verify' in request.form.keys() and isinstance(request.form['verify'], basestring)):
                if 'verify' in session and hashlib.md5(request.form['verify']).hexdigest()[:6] == session.pop('verify', None):
                    username = request.form['username']
                    if check_username(username) is True:
                        if len(query_db('select * from users where username = ?', (username,))) == 0:
                            password = hashlib.md5(
                                request.form['password']).hexdigest()
                            query_db(
                                'insert into users (username, password) values (?, ?)', (username, password))
                            g.db.commit()
                            return redirect('/login.php', 'Register success!')
                        else:
                            return redirect('/register.php', 'Username exists!')
                    else:
                        return redirect('/register.php', 'Invalid username!')
                else:
                    return redirect('/register.php', 'Invalid verify!')
        session['verify'] = hashlib.md5(os.urandom(24)).hexdigest()[:6]
        return handle_response(make_response(render_template('register.html', verify=session['verify'])))
    except Exception as e:
        with open('/opt/log/error.log', 'ab') as log:
            log.write(e.message + '\n')
        abort(500)


if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=23333, debug=False)
