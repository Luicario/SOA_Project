from nameko.web.handlers import http
from pkg_resources import ResolutionError
from werkzeug.wrappers import Response
import uuid
from nameko.rpc import RpcProxy
from dependencies.session import SessionProvider

from distutils.log import debug
from flask import request, Flask

from calculator import idx_palindrome_prime
from calculator import idx_prime


app = Flask(__name__)

name = "gateway_service"
user_rpc = RpcProxy('user_service')
session_provider = SessionProvider()

@app.route('/login', methods=['POST'])
def login(self, request):
    user_data = self.user_rpc.user_login(request.form['username'],request.form['password'])
    session_id = self.session_provider.set_session(user_data)
    response = Response(str(user_data))
    response.set_cookie('SESSID', session_id)
    response.set_cookie('USERNAME', request.form['username'])
    return response

@app.route('/login', methods=['POST'])
def register(self, request):
    result = self.user_rpc.user_add(request.form['username'],request.form['password'])
    if (result.length() == 0):
        self.user_rpc.user_add(request.form['username'],request.form['password'])
        return Response("Register Success")
    else:
        return Response("Register Failed, Data already exist")

@app.route('/logout', methods=['GET'])
def logout(self, request):
        session_id = request.cookies.get('SESSID')
        self.session_provider.get_session(session_id)
        response = Response("Logout success")
        response.set_cookie('SESSID', '', expires=0)
        return response

@app.route('/check', methods=['GET'])
def check(self, request):
        cookies = request.cookies
        return Response(cookies['SESSID'])

@app.route('/prime/<int:index>', methods=['GET'])
def prime(index):
    cookies = request.cookies
    if cookies:
        result = idx_prime.delay(index)
        return {'result': result.get()}
    else:
        response = Response('You need to Login First')
        return response 

@app.route('/primepal/<int:index>', methods=['GET'])
def primepal(index):
    result = idx_palindrome_prime.delay(index)
    return {'result': result.get()}

app.run(port=8000, debug = True)