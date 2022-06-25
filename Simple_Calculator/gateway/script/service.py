from nameko.rpc import rpc

import gateway.script.dependencies as dependencies

class RoomService:

    name = 'user_service'

    database = dependencies.Database()

    @rpc
    def get_all_user(self):
        return self.database.getallusers()
    @rpc
    def user_login(self, username, password):
        return self.database.login(username, password)
    @rpc
    def user_add(self, username, password):
        return self.database.adduser(username, password)
    
    @rpc
    def combination(self, string):
        return self.database.combination(string)

    @rpc
    def permutation(self, string):
        return self.database.permutation(string)