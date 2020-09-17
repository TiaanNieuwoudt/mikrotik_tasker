import routeros_api
import datetime
from tools import devices_by_submaps

USERNAMES = [Enter list of usernames here]
PASSWORDS = [Enter list of passwords here]


class Entity:
    def __init__(self, ip_addr):
        self.identity = None
        self.ip_addr = ip_addr
        self.username = None
        self.password = None
        self.port = 8728
        self.api = None
        self.routerboard = None
        self.build = None
        self.submap = None

    def __del__(self):
        print("Instance terminated")

    def create_connection(self,  __username, __password, bruteforce=False):



        if bruteforce:
            for _username in USERNAMES:
                for _password in PASSWORDS:



                    try:
                        connection = routeros_api.RouterOsApiPool(self.ip_addr, username=_username, password=_password,
                                                                  plaintext_login=False, port=self.port)

                        self.api = connection.get_api()
                        self.username, self.password = _username, _password
                        self.sys_info()
                        return self.api

                    except routeros_api.exceptions.RouterOsApiConnectionError:
                        print("Connection Failed")
                        with open('ERROR_sites.txt', 'a+') as file:
                            file.write("{}\n".format(self.ip_addr))
                        return False

                    except routeros_api.exceptions.RouterOsApiCommunicationError:
                        print("invalid user name or password")




                        try:
                            connection = routeros_api.RouterOsApiPool(self.ip_addr, username=_username, password=_password, plaintext_login=True, port=self.port)
                            self.api = connection.get_api()
                            self.username, self.password = _username, _password
                            self.sys_info()
                            return self.api

                        except routeros_api.exceptions.RouterOsApiCommunicationError:
                            if _password == PASSWORDS[-1] and _username == USERNAMES[-1]:
                                with open('ERROR_sites.txt', 'a+') as file:
                                    file.write("{}\n".format(self.ip_addr))

                        except AttributeError:
                            if _password == PASSWORDS[-1] and _username == USERNAMES[-1]:
                                print("Attribute error")
                                with open('ERROR_sites.txt', 'a+') as file:
                                    file.write("{}\n".format(self.ip_addr))

        else:

            try:
                connection = routeros_api.RouterOsApiPool(self.ip_addr, username=__username, password=__password,
                                                          plaintext_login=False, port=self.port)

                self.api = connection.get_api()
                self.username, self.password = __username, __password
                self.sys_info()
                return self.api

            except routeros_api.exceptions.RouterOsApiCommunicationError:
                print('Could not log into router')
                return False



    def run_script(self, source, name):
        prefix = self.api.get_resource('/sys/script')
        prefix.add(name=name, source=source)
        self.api.get_resource('/sys/script').call('run', {'id': name})
        prefix.remove(id=name)


    def sys_info(self):
        identity = self.api.get_resource('/sys/identity')
        resource = self.api.get_resource('/sys/resource')
        id = identity.get()
        model = resource.get()
        self.identity = id[0]["name"]
        self.routerboard = model[0]["board-name"]
        return self.routerboard, self.identity

    def add_user(self, new_user, new_password, protected_users):
        if self.username not in protected_users:

            user_path = self.api.get_resource('/user')
            try:
                user_path.add(name=new_user, password=new_password, disabled='no', group='full')
            except routeros_api.exceptions.RouterOsApiCommunicationError:
                print('user already exists')
            self.username = new_user
            self.password = new_password

    def delete_additional_users(self):
        user_path = self.api.get_resource('/user')
        users = user_path.get()
        curr_users = list()
        for user in users:
            curr_users.append(user['name'])

            if user['name'] != self.username:
                user_path.remove(numbers=user['name'])

        with open('device_passwords.txt', 'a+') as file:
            file.write(
                "Device --> {}\nusernames --> {}\nsubmap --> {}\n\n".format(self.identity, curr_users, self.submap))


    def get_dude_device(self, name):
        dude_path = self.api.get_resource('/dude/device')
        device = dude_path.set(name=name, username=username)
        print(device)


connect = Entity(sample IP)
connect.create_connection(username, password)
connect.get_dude_device(device by name)

