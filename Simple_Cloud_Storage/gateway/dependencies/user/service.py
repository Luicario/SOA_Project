from nameko.rpc import rpc
import databasewrapper

class UserService:
    name = 'user_service'
    database = databasewrapper.Database()

    @rpc
    def add_user(self, username, password):
        res = self.database.add_user(username,password)
        return res

    @rpc
    def login_user(self, username, password):
        res = self.database.login_user(username, password)
        return res