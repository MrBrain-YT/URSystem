import requests, json, time
import secrets

# url = "http://127.0.0.1:5000/CurentMotorsPosition"
# data = {
#     "Robot": "First",
#     "J1": 500,
#     "J2": 0,
#     "J3": 0,
#     "J4": 0,
#     "J5": 0,
#     "J6": 0
#     }


# code = '''import time
# while True:
#     print("hello2")
#     '''.encode().hex()
# url = "http://127.0.0.1:5000/SetProgram"
# data = {
#     "Robot": "First",
#     "Program": ""
#     }


# url = "http://127.0.0.1:5000/SetProgramRun"
# data = {
#     "Robot": "First",
#     "State": "False"
#     }


# url = "http://127.0.0.1:5000/GetRobots"
# data = {

# }

# url = "http://127.0.0.1:5000/MaxAngles"
# data = {
#     "Robot": "Vasia",
#     "J1": 100,
#     "J2": 0,
#     "J3": 0,
#     "J4": 0,
#     "J5": 0,
#     "J6": 0,
#     "J7": 0
#     }

# url = "http://127.0.0.1:5000/URLogs"
# data = {
#     "Robot": "First",
#     "Type": "ERROR",
#     "Text": "Started"
#     }

# url = "http://127.0.0.1:5000/URTools"
# data = {
#     "Id": "hello2",
#     "Type": "write",
#     "Cfg": "0|0|0"
#     }

# print(requests.get(url).text)

# url = "http://127.0.0.1:5000/Emergency"
# data = {
#     "Robot": "First",
#     "State": "True"
#     }

# url = "http://127.0.0.1:5000/CreateRobot"
# data = {
#     "Robot": "Vasia",
#     "Angle": 7,
#     "Kinematic" : "" 
#     }

# url = "http://127.0.0.1:5000/GetRobot"
# data = {
#     "Robot": "First", 
#     "token": "f5d9bdd8ffa3b2195736ea54a84e0bd85d03b95d6f0163e9da529bb1adceb42",
#     "cert": "50eb40bd317a38dc09bfcb8d4e19ff5403689b7ba2d7ef94d7ce8dcb9d43eeb60f383e5ee50e41628e9f6fc93588fb6d093dcb32d2cbff18a034d42bb3caf7ff"
#     }

# url = "http://127.0.0.1:5000/GetAccounts"
# data = {
#     }

# url = "http://127.0.0.1:5000/SetProgramRun"
# data = {
#     "Robot": "First",
#     "State": "False"
#     }

# url = "http://127.0.0.1:5000/XYZ"
# data = {
#     "Robot": "First",
#     "X": 100,
#     "Y": 0,
#     "Z": 0
#     }


# while True:
# resp = requests.post(url, data=json.loads(json.dumps(data, ensure_ascii=False))).text
# print(resp)
#     time.sleep(1)



# SQL example
import sqlite3
con = sqlite3.connect("server\\Databases\\Users.sqlite")
cur = con.cursor()
# cur.execute("UPDATE users SET password = '', name = '' WHERE name = 'System'")
# # cur.execute("DELETE FROM 'users' WHERE token = '6f1604743b8691eb8d1d35a26ffc144de5624aa6d140f1425a54d8a50c5f7227'")
cur.execute(f"INSERT INTO users VALUES ('First', '12345', 'robot', '{secrets.token_hex(32)}')")
con.commit()
con.close()


# url = f"https://{'localhost'}:{'5000'}/GetRoleAccount"
# data = {
#     "name": "SuperAdmin",
#     "password": "12345", 
#     "token": "15244dfbf0c9bd8378127e990c48e5a68b8c5a5786f34704bc528c9d91dbc84a"
#     }
# resp = requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
# print(resp)

