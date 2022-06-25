import queue
from nameko.extensions import DependencyProvider
import mysql.connector
import uuid
import hashlib
from mysql.connector import Error
from mysql.connector import pooling

class DatabaseWrapper:
    connection = None

    def __init__(self, connection):
        self.connection = connection

    def add_user(self, username, password):
        cursor = self.connection.cursor(dictionary=True)
        res = {
            'status':'error',
            'message':"Something went wrong!!!",
        }
        query = "SELECT * FROM users WHERE name='"+username+"'"
        cursor.execute(query)
        if(len(cursor.fetchall()) == 0):
            if(len(password) >= 8):
                passwordhash = hashlib.md5(password.encode())
                query = "INSERT INTO users (id,name,password) VALUES ('"+str(uuid.uuid4())+"','"+username+"','"+passwordhash.hexdigest()+"')"
                cursor.execute(query)
                self.connection.commit()
                cursor.close()
                res['message'] = "Success add user " + username
                res['status'] = 'success'
            else:
                res['message'] = "password must be at least 8 characters"
        else:
            res['message'] = "username "+username+" already exists"
        return res

    def __del__(self):
        self.connection.close()

    def login_user(self,username,password):
        cursor = self.connection.cursor(dictionary=True)
        res = {
            'status':"error",
            'message':"Something went wrong!!!",
            'data': {}
        }
        password_hash = hashlib.md5(password.encode())
        query = "SELECT COUNT(id) AS count FROM users WHERE name='"+username+"'"
        cursor.execute(query)
        count = cursor.fetchone()['count']
        if(count == 1):
            query = "SELECT * FROM users WHERE name='"+username+"' AND password='"+password_hash.hexdigest()+"'"
            cursor.execute(query)
            row = cursor.fetchone()

            if(row == None):
                res['message'] = "Wrong Password"
            else:
                res['data'] = row
                res['message'] = "Login Success"
                res['status'] = "success"
        else:
            res['message'] = "User "+username+" not found"
        
        return res



class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='localhost',
                database='dbsimplecloudstorage',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL` using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())