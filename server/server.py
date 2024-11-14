import os
import secrets
import shutil
import ssl
import sqlite3
import importlib
import ast

from flask import Flask, request
from threading import Thread

import server.configuration.robots_cache as robots_cache
from server.server_functions import Robot, System, User
import server.configuration.server_token as server_token
import server.utils.programs_starter as programs_starter
from server.utils.loger import Loger, Robot_loger
from server.API.frames import Frames
from server.API.multi_robots_system import URMSystem

# Importing robots from cache
robots_list = robots_cache.robots
robots = robots_cache.robots.keys()
for robot in robots:
    robots_list[robot]["Program"] = ""
    robots_list[robot]["ProgramRunning"] = "False"
    robots_list[robot]["RobotReady"] = "True"
    robots_list[robot]["Emergency"] = "False"
    robots_list[robot]["MotorsSpeed"] = robots_list[robot]['StandartSpeed'].copy()
    robots_list[robot]["Position"] = robots_list[robot]["MotorsPosition"].copy()
    
# importing all kinematics
kinematics = {}
for robot in robots:
    if robots_list[robot]["Kinematic"] == "None":
        kinematics[robot] = "None"
    else:
        try:
            kinematics[robot] = importlib.import_module(
                f'kinematics.{robots_list[robot]["Kinematic"]}.kin')
        except:
            # send to logs!
            print(f"For robot '{robot}' kinematic file not found ")

# Set global variables
Robots = robots_list
tools = robots_cache.tools
frames = robots_cache.frames
users = User.update_token()
loger = Loger()

def update_users():
    global users
    users = User.update_token()

""" Server """
app = Flask(__name__)

""" Init server functions"""
app = Frames(app, Robots, tools, frames, users, loger)

""" URMSystem """ # URMS - United Robotics Multi System
app = URMSystem(app, Robots, tools, frames, users, loger)

""" URAccount """
@app.route("/CreateAccount", methods=['POST'])
def CreateAccount():
    info = request.form
    if User.role_access(info.get("token"), "administrator", users):
        if info.get("name") not in users:
            while True:
                token = secrets.token_hex(32)
                tokens = []
                for i in [i for i in users]:
                    tokens.append(users.get(i)["token"])
                if token not in tokens:
                    break
                con = sqlite3.connect("Databases\\Users.sqlite")
                cur = con.cursor()
                res = cur.execute(f"INSERT INTO users VALUES ('{info.get('name')}', '{info.get('password')}', '{info.get('user_role')}', '{token}')")
                con.commit()
                loger.info("URAccount", f"Account was created with name-{info.get('name')} and password-{info.get('password')}")
                update_users()
                loger.info("URAccount", f"Фccount with name: {info.get('name')} was created")
                return token
        else:
            loger.info("URAccount", f"The account has already been created")
            return "The account has already been created"
    else:
        loger.warning("URAccount", f"User access denied to create account. User with token: {info.get('token')}")
        return "You don't have enough rights"
    
@app.route("/DeleteAccount", methods=['POST'])
def DeleteAccount():
    info = request.form
    if User.role_access(info.get("token"), "SuperAdmin", users):
        if info.get("name") in users:
            con = sqlite3.connect("Databases\\Users.sqlite")
            cur = con.cursor()
            res = cur.execute(f"DELETE FROM 'users' WHERE name = '{info.get('name')}'")
            con.commit()
            update_users()
            loger.info("URAccount", f"Фccount with name: {info.get('name')} was deleted")
            return "True"
        else:
            return "No such account exists"
    else:
        loger.warning("URAccount", f"User access denied to delete account. User with token: {info.get('token')}")
        return "You don't have enough rights"
    
# get account
@app.route("/GetAccounts", methods=['POST'])
def GetAccounts():
    info = request.form
    if User.role_access(info.get("token"), "SuperAdmin", users):
        user = {}
        for i in users.copy():
            user[i] = users.get(i) if users[i]["role"] != "SuperAdmin" else None
        update_users()
        return user
    else:
        loger.warning("URAccount", f"User access denied to get accounts. User with token: {info.get('token')}")
        return "You don't have enough rights"
    
# get role account
@app.route("/GetRoleAccount", methods=['POST'])
def GetRoleAccount():
    info = request.form
    if info.get("server_token") == server_token.reg_token:
        update_users()
        if info.get("name") in users:
            if users[info.get("name")]["password"] == info.get("password"):
                return f"{users[info.get('name')]['role']},{users[info.get('name')]['token']}"
            else:
                loger.error("URAccount", f"Password incorrect")
                return "False"
        else:
            loger.error("URAccount", f"Name not in users")
            return "False"
    else:
        loger.error("URAccount", f"Server token incorrect")
        return "Server token incorrect"

# change password
@app.route("/ChangePass", methods=['POST'])
def change_password():
    info = request.form
    if User.role_access(info.get("token"), "SuperAdmin", users):
        con = sqlite3.connect("Databases\\Users.sqlite")
        cur = con.cursor()
        cur.execute(f"UPDATE users SET password = '{info.get('password')}' WHERE name = '{info.get('name')}'")
        con.commit()
        con.close()
        update_users()
        loger.info("URAccount", f"Password was changed for account with name: {info.get('name')}")
        return "True"
    else:
        loger.warning("URAccount", f"User access denied to change password. User with token: {info.get('token')}")
        return "You don't have enough rights"
    
# get user token
@app.route("/GetToken", methods=['POST'])
def get_user_token():
    info = request.form
    if User.role_access(info.get("token"), "SuperAdmin", users):
        con = sqlite3.connect("Databases\\Users.sqlite")
        cur = con.cursor()
        cur.execute(f"SELECT token FROM users WHERE name = '{info.get('name')}, password = '{info.get('password')}'")
        token = cur.fetchone()
        con.commit()
        con.close()
        return token
    else:
        loger.warning("URAccount", f"User access denied to get token. User with token: {info.get('token')}")
        return "You don't have enough rights"
    
# change user token
@app.route("/ChangeToken", methods=['POST'])
def changedoken():
    info = request.form
    if User.role_access(info.get("token"), "SuperAdmin", users):
        while True:
            token = secrets.token_hex(32)
            tokens = []
            for i in [i for i in users]:
                tokens.append(users.get(i)["token"])
            if token not in tokens:
                break
        con = sqlite3.connect("Databases\\Users.sqlite")
        cur = con.cursor()
        cur.execute(f"UPDATE users SET token = '{token}' WHERE name = '{info.get('name')}' and password = '{info.get('password')}'")
        con.commit()
        con.close()
        loger.info("URAccount", f"Token was changed for account with name: {info.get('name')}")
        return token
    else:
        loger.warning("URAccount", f"User access denied to change token. User with token: {info.get('token')}")
        return "You don't have enough rights"

""" URLogs """
# get log
@app.route("/URLog", methods=['POST'])
def URLog():
    if User.role_access(request.form.get("token"), "user", users):
        update_users()
        return Robots[request.form.get("Robot")]["Logs"] 
    else:
        return "You are not on the users list"

# add new log
@app.route("/URLogs", methods=['POST'])
def URLogs():
    info = request.form
    if User.role_access(info.get("token"), "user", users):
            Robot_loger(info.get("Robot")).debug(info.get("Text"))
            System.SaveToCache(Robots, tools, frames)
            update_users()
            return "True"
    else:
        return "You are not on the users list"

""" URS tool system """
# get tools
@app.route("/URTools", methods=['POST'])
def Tools():
    if User.role_access(request.form.get("token"), "administrator", users):
        update_users()
        return str(tools)
    else:
        loger.warning("URTools", f"User access denied to get tools. User with token: {request.form.get('token')}")
        return "You don't have enough rights"

# get and set tool configuration
@app.route("/URTool", methods=['POST'])
def Tool():
    info = request.form
    if User.role_access(info.get("token"), "user", users):
        if info.get("type") == "write":
            if info.get("id") in [i for i in tools.values()]:
                tools[info.get("id")] = info.get("config")
                System.SaveToCache(Robots, tools, frames)
                update_users()
                return "True"
            else:
                loger.error("URTools", f"The tool {info.get('id')} has not been created and cannot be modified")
                return "The tool has not been created"
        else:
            return tools[info.get("id")]
    else:
        return "You are not on the users list"

# creating tool 
@app.route("/URTC", methods=['POST'])
def URTC():
    info = request.form
    if User.role_access(info.get("token"), "administrator", users):
        if info.get("id") not in [i for i in tools.values()]:
            tools[info.get("id")] = ""
            System.SaveToCache(Robots, tools, frames)
            update_users()
            loger.info("URTools", f"Tool {info.get('id')} was created")
            return "True"
        else:
            loger.error("URTools", f"The tool {info.get('id')} already exists")
            return "The tool already exists"
    else:
        loger.warning("URTools", f"User access denied to create tool. User with token: {request.form.get('token')}")
        return "You don't have enough rights"
    
# delete tool
@app.route("/URTD", methods=['POST'])
def URTD():
    global tools
    info = request.form
    if User.role_access(info.get("token"), "administrator", users):
        del tools[info.get("id")]
        System.SaveToCache(Robots, tools, frames)
        update_users()
        loger.info("URTools", f"Tool {info.get('id')} was deleted")
        return "True"
    else:
        loger.warning("URTools", f"User access denied to delete tool. User with token: {request.form.get('token')}")
        return "You don't have enough rights"





""" hello message """
@app.route("/")
def URGreetings():
    # home site
    return """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>3D Object</title>
        <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.3.0/model-viewer.min.js"></script>
    </head>
    <body>
        <model-viewer class="model" src="Robot.gltf" ar ar-modes="webxr scene-viewer quick-look" camera-controls poster="poster.webp" shadow-intensity="1">
        </model-viewer>
        
    </body>
    <style>
        .model{
            width: 700px;
            height: 1000px;
        }
    </style>
</html>"""

@app.route("/Robot.gltf")
def model():
    return open("./Robot.gltf", "rb").read()





""" Add kinematics to system """
@app.route("/AddKinematics", methods=['POST'])
def AddKinematics():
    info = request.form
    if User.role_access(info.get("token"), "administrator", users):
        zip_path = f"./kinematics/{request.files.get('file').filename}"
        request.files.get("file").save(zip_path)
        shutil.unpack_archive(filename=zip_path, extract_dir=zip_path.replace(".zip", ""), format="zip")
        os.remove(zip_path)
        loger.info("URSystem", f"Added new kinematic with work name: {request.files.get('file')}")
        return "True"
    else:
        loger.warning("URSystem", f"User access denied to add kinematic. User with token: {request.form.get('token')}")
        return "You don't have enough rights"

""" Bind kinematics to robot """
@app.route("/BindKinematics", methods=['POST'])
def BindKinematics():
    info = request.form
    if User.role_access(info.get("token"), "administrator", users) and Robot.robot_access(Robots, info.get("Robot"), info.get("Code")):
        Robots[info.get("Robot")]["Kinematic"] = info.get('Kinematics') if \
            os.path.exists(f"./kinematics/{info.get('Kinematics')}") else Robots[info.get("Robot")]["Kinematic"]
            
        if Robots[info.get("Robot")]["Kinematic"] == info.get('Kinematics'):
            loger.info("URSystem", f"Was created associate kinematics-{info.get('Kinematics')} and robot-{info.get('Robot')}")
            return "True"
        else:
            loger.error("URSystem", f"Not created associate kinematics-{info.get('Kinematics')} and robot-{info.get('Robot')}")
            return "It was not possible to associate kinematics with the robot because it is missing"
    else:
        loger.warning("URSystem", f"User access denied to bind kinematic. User with token: {request.form.get('token')}")
        return "You don't have enough rights"
    
""" Get curent robot position"""
@app.route('/GetCurentPosition', methods=['POST'])
def GetCurentPosition():
    info = request.form
    if Robot.is_robot(info.get("token"), users):
        return str(Robots[info.get("Robot")]["Position"])
    else:
        return "Your account is not a robot account"
    
""" Set curent robot motor position"""
@app.route('/SetCurentMotorPosition', methods=['POST'])
def SetCurentMotorPosition():
    info = request.form
    if Robot.is_robot(info.get("token"), users):
        for i in range(1, int(Robots[info.get("Robot")]["AngleCount"])+1):
            Robots[info.get("Robot")]["MotorsPosition"][f"J{i}"] = float(info.get(f'J{i}').replace(",", "."))
            if Robots[info.get("Robot")]["Emergency"] == "True":
                Robots[info.get("Robot")]["Position"][f"J{i}"] = float(info.get(f'J{i}').replace(",", "."))
        return "True"
    else:
        return "Your account is not a robot account"
    
""" Get curent robot speed """
@app.route('/GetCurentSpeed', methods=['POST'])
def GetCurentSpeed():
    info = request.form
    if Robot.is_robot(info.get("token"), users):
        return str(Robots[info.get("Robot")]["MotorsSpeed"])
    else:
        return "Your account is not a robot account"
    
""" Get robot ready parametr """
@app.route('/GetRobotReady', methods=['POST'])
def GetRobotReady():
    info = request.form
    if Robot.is_robot(info.get("token"), users):
        return str(Robots[info.get("Robot")]["RobotReady"])
    else:
        return "Your account is not a robot account"
    
""" Set robot ready parametr """
@app.route('/SetRobotReady', methods=['POST'])
def SetRobotReady():
    info = request.form
    if Robot.is_robot(info.get("token"), users):
        Robots[info.get("Robot")]["RobotReady"] = info.get('RobotReady')
        System.SaveToCache(Robots, tools, frames)
        update_users()
        return "True"
    else:
        return "Your account is not a robot account"
    
''' Activate and deativate emergency stop '''
@app.route('/SetRobotEmergency', methods=['POST'])
def SetRobotEmergency():
    info = request.form
    if (User.role_access(info.get("token"), "user", users) and \
    Robot.robot_access(Robots, info.get("Robot"), info.get("Code"))) or Robot.is_robot(info.get("token"), users):
        Robots[info.get("Robot")]["Emergency"] = "True" if info.get("State") == "True" else "False"
        Robots[info.get("Robot")]["Position"] = Robots[info.get("Robot")]["MotorsPosition"].copy()
        Robots[info.get("Robot")]["RobotReady"] = "False"
        Robots[info.get("Robot")]["Program"] = ""
        System.SaveToCache(Robots, tools, frames)
        update_users()
        Robot_loger(info.get("Robot")).info(f"Emergency stop button activated")
        return "True"
    else:
        loger.warning("URSystem", f"User access denied to set robot emergency because this not robot account. User with token: {request.form.get('token')}")
        return "Your account is not a robot account"
    
''' Get emergency stop '''
@app.route('/GetRobotEmergency', methods=['POST'])
def GetRobotEmergency():
    info = request.form
    if Robot.is_robot(info.get("token"), users):
        return Robots[info.get("Robot")]["Emergency"]
    else:
        return "Your account is not a robot account"

""" Curent robot position"""
@app.route('/CurentPosition', methods=['POST'])
def CurentPosition():
    info = request.form
    if (User.role_access(info.get("token"), "user", users) and \
    Robot.robot_access(Robots, info.get("Robot"), info.get("Code"))) or Robot.is_robot(info.get("token"), users):
        while True:
            if Robots[info.get("Robot")]["Emergency"] == "True":
                Robot_loger(info.get("Robot")).error(f"The robot is currently in emergency stop")
                return "The robot is currently in emergency stop"
            else:
                if Robots[info.get("Robot")]["RobotReady"] == "False":
                    continue
                else:
                    if Robot.check_angles(info, Robots) == False:
                        Robot_loger(info.get("Robot")).error(f"Values ​​are not validated")
                        return "Values ​​are not validated"
                    else:
                        for i in range(1, int(Robots[info.get("Robot")]["AngleCount"])+1):
                            Robots[info.get("Robot")]["Position"][f"J{i}"] = float(info.get(f'J{i}'))
                        if Robots[info.get("Robot")]["Kinematic"] != "None":
                            modul = kinematics[info.get("Robot")]
                            result_forward = modul.Forward(float(info.get("J1")), float(info.get("J2")), float(info.get("J3")), float(info.get("J4")))
                            Robots[info.get("Robot")]["XYZposition"]["X"] = result_forward[0]
                            Robots[info.get("Robot")]["XYZposition"]["Y"] = result_forward[1]
                            Robots[info.get("Robot")]["XYZposition"]["Z"] = result_forward[2]
                        System.SaveToCache(Robots, tools, frames)
                        update_users()
                        Robot_loger(info.get("Robot")).info(f"""Was setted robot current position: {
                            info.get('J1')},{info.get('J2')},{info.get('J3')},{info.get('J4')}""")
                        return "True"
    else:
        return "You are not on the users list"
    
""" Curent home position"""
@app.route('/HomePosition', methods=['POST'])
def HomePosition():
    info = request.form
    if User.role_access(info.get("token"), "user", users) and Robot.robot_access(Robots, info.get("Robot"), info.get("Code")):
        if Robot.check_angles(info, Robots) == False:
            Robot_loger(info.get("Robot")).error(f"Values ​​are not validated")
            return "Values ​​are not validated"
        else:
            for i in range(1, int(Robots[info.get("Robot")]["AngleCount"])+1):
                Robots[info.get("Robot")]["HomePosition"][f"J{i}"] = float(info.get(f'J{i}'))
            System.SaveToCache(Robots, tools, frames)
            update_users()
            Robot_loger(info.get("Robot")).info(f"""Was setted robot home position: {
                info.get('J1')},{info.get('J2')},{info.get('J3')},{info.get('J4')}""")
            return "True"
    else:
        return "You are not on the users list"

""" Curent robot speed """
@app.route('/CurentSpeed', methods=['POST'])
def CurentSpeed():
    info = request.form
    if (User.role_access(info.get("token"), "user", users) and \
    Robot.robot_access(Robots, info.get("Robot"), info.get("Code"))) or Robot.is_robot(info.get("token"), users):
        if Robots[info.get("Robot")]["Emergency"] == "True":
            Robot_loger(info.get("Robot")).error(f"The robot is currently in emergency stop")
            return "The robot is currently in emergency stop"
        else:
            for i in range(1, int(Robots[info.get("Robot")]["AngleCount"])+1):
                Robots[info.get("Robot")]["MotorsSpeed"][f"J{i}"] = float(info.get(f'J{i}'))
            System.SaveToCache(Robots, tools, frames)
            update_users()
            Robot_loger(info.get("Robot")).info(f"""Was setted robot current speed: {
                info.get('J1')},{info.get('J2')},{info.get('J3')},{info.get('J4')}""")
            return "True"
    else:
        return "You are not on the users list"

""" Standart robot speed"""
@app.route('/StandartSpeed', methods=['POST'])
def StandartSpeed():
    info = request.form
    if User.role_access(info.get("token"), "user", users) and Robot.robot_access(Robots, info.get("Robot"), info.get("Code")):
        for i in range(1, int(Robots[info.get("Robot")]["AngleCount"])+1):
            Robots["First"]["StandartSpeed"][f"J{i}"] = float(info.get(f'J{i}'))
        System.SaveToCache(Robots, tools, frames)
        update_users()
        Robot_loger(info.get("Robot")).info(f"""Was setted robot standart speed: {
                info.get('J1')},{info.get('J2')},{info.get('J3')},{info.get('J4')}""")
        return "True"
    else:
        return "You are not on the users list"
    
""" Set program """
@app.route('/SetProgram', methods=['POST'])
def Program():
    info = request.form
    if User.role_access(info.get("token"), "user", users) and Robot.robot_access(Robots, info.get("Robot"), info.get("Code")):
        if Robots[info.get("Robot")]["Emergency"] == "True":
            Robot_loger(info.get("Robot")).error(f"The robot is currently in emergency stop")
            return "The robot is currently in emergency stop"
        else:
            Robots[info.get("Robot")]["Program"] = info.get('Program')
            update_users()
            Robot_loger(info.get("Robot")).info(f"Was setted robot programm")
            return "True"
    else:
        return "You are not on the users list"

""" Delete program """
@app.route('/DeleteProgram', methods=['POST'])
def DeleteProgram():
    info = request.form
    if User.role_access(info.get("token"), "user", users) and Robot.robot_access(Robots, info.get("Robot"), info.get("Code")):
        Robots[info.get("Robot")]["Program"] = ""
        System.SaveToCache(Robots, tools, frames)
        update_users()
        Robot_loger(info.get("Robot")).info(f"Was deleted robot programm")
        return "True"
    else:
        return "You are not on the users list"

""" Get angle from XYZ robot position """
@app.route('/angle_to_xyz', methods=['POST'])
def angle_to_xyz():
    info = request.form
    if (User.role_access(info.get("token"), "user", users) and \
    Robot.robot_access(Robots, info.get("Robot"), info.get("Code"))) or Robot.is_robot(info.get("token"), users):
        if kinematics[info.get("Robot")] != "None":
            try:
                new_coord = {}
                modul = kinematics[info.get("Robot")]
                result_forward = modul.Forward(float(info.get("J1")), float(info.get("J2")), float(info.get("J3")), float(info.get("J4")))
                new_coord["X"] = result_forward[0]
                new_coord["Y"] = result_forward[1]
                new_coord["Z"] = result_forward[2]
                return str(new_coord)
            except:
                return "An error has occurred"
        else:
            return "This command does not work if you are not using kinematics"
    else:
        return "You are not on the users list"

""" Get angle from XYZ robot position """
@app.route('/XYZ_to_angle', methods=['POST'])
def XYZ_to_angle():
    info = request.form
    if (User.role_access(info.get("token"), "user", users) and \
    Robot.robot_access(Robots, info.get("Robot"), info.get("Code"))) or Robot.is_robot(info.get("token"), users):
        if kinematics[info.get("Robot")] != "None":
            try:
                new_angles = {}
                modul = kinematics[info.get("Robot")]
                result_inverse = modul.Inverse(float(info.get("X")), float(info.get("Y")), float(info.get("Z")))
                for j in range(1, int(Robots[info.get("Robot")]["AngleCount"]) + 1):
                    new_angles[f"J{j}"] = result_inverse[j-1]
                return str(new_angles)
            except:
                return "An error has occurred"
        else:
            return "This command does not work if you are not using kinematics"
    else:
        return "You are not on the users list" 
    
""" Set curent robot XYZ position """
@app.route('/Move_XYZ', methods=['POST'])
def Move_XYZ():
    info = request.form
    if User.role_access(info.get("token"), "user", users) and Robot.robot_access(Robots, info.get("Robot"), info.get("Code")):
        if kinematics[info.get("Robot")] != "None":
            while True:
                if Robots[info.get("Robot")]["Emergency"] == "True":
                    Robot_loger(info.get("Robot")).error(f"The robot is currently in emergency stop")
                    return "The robot is currently in emergency stop"
                else:
                    if Robots[info.get("Robot")]["RobotReady"] == "False":
                        continue
                    else:
                        try:
                            modul = kinematics[info.get("Robot")]
                            result_inverse = modul.Inverse(float(info.get("X")), float(info.get("Y")), float(info.get("Z")))
                            for j in range(1, int(Robots[info.get("Robot")]["AngleCount"]) + 1):
                                Robots[info.get("Robot")]["Position"][f"J{j}"] = result_inverse[j-1]
                                
                            Robots[info.get("Robot")]["XYZposition"]["X"] = float(info.get("X"))
                            Robots[info.get("Robot")]["XYZposition"]["Y"] = float(info.get("Y"))
                            Robots[info.get("Robot")]["XYZposition"]["Z"] = float(info.get("Z"))
                            System.SaveToCache(Robots, tools, frames)
                            update_users()
                            Robot_loger(info.get("Robot")).info(f"""The robot has been moved to coordinates: X-{
                                info.get("X")},Y-{info.get("Y")},Z-{info.get("Z")}""")
                            return "True"
                        except:
                            return "An error has occurred"
        else:
            return "This command does not work if you are not using kinematics"
    else:
        return "You are not on the users list"

''' Set minimal angle of rotation '''
@app.route('/MinAngles', methods=['POST'])
def MinAngles():
    info = request.form
    if User.role_access(info.get("token"), "administrator", users) and Robot.robot_access(Robots, info.get("Robot"), info.get("Code")):
        if Robots[info.get("Robot")]["Emergency"] == "True":
            Robot_loger(info.get("Robot")).error(f"The robot is currently in emergency stop")
            return "The robot is currently in emergency stop"
        else:
            for i in range(1, int(Robots[info.get("Robot")]["AngleCount"])+1):
                Robots[info.get("Robot")]["MinAngles"][f"J{i}"] = float(info.get(f'J{i}'))
            System.SaveToCache(Robots, tools, frames)
            update_users()
            Robot_loger(info.get("Robot")).info(f"""Was setted robot minimal angles: {
                info.get('J1')},{info.get('J2')},{info.get('J3')},{info.get('J4')}""")
            return Robots[info.get("Robot")]["MinAngles"]
    else:
        loger.warning("URSystem", f"User access denied to set robot {info.get('Robot')} minimal angles. User with token: {request.form.get('token')}")
        return "You don't have enough rights"

''' Set maximum angle of rotation '''
@app.route('/MaxAngles', methods=['POST'])
def MaxAngles():
    info = request.form
    if User.role_access(info.get("token"), "administrator", users) and Robot.robot_access(Robots, info.get("Robot"), info.get("Code")):
        if Robots[info.get("Robot")]["Emergency"] == "True":
            Robot_loger(info.get("Robot")).error(f"The robot is currently in emergency stop")
            return "The robot is currently in emergency stop"
        else:
            for i in range(1, int(Robots[info.get("Robot")]["AngleCount"])+1):
                Robots[info.get("Robot")]["MaxAngles"][f"J{i}"] = float(info.get(f'J{i}'))
            System.SaveToCache(Robots, tools, frames)
            update_users()
            Robot_loger(info.get("Robot")).info(f"""Was setted robot maximal angles: {
                info.get('J1')},{info.get('J2')},{info.get('J3')},{info.get('J4')}""")
            return Robots[info.get("Robot")]["MaxAngles"]
    else:
        loger.warning("URSystem", f"User access denied to set robot {info.get('Robot')} maximal angles. User with token: {request.form.get('token')}")
        return "You don't have enough rights"

''' Set program is running '''
@app.route('/SetProgramRun', methods=['POST'])
def SetProgramRun():
    info = request.form
    if User.role_access(info.get("token"), "System", users):
        Robots[info.get("Robot")]["ProgramRunning"] = info.get("State")
        update_users()
        return Robots[info.get("Robot")]["ProgramRunning"]
    else:
        return "You don't have enough rights"


if __name__ == "__main__":
    # Creating SSL context
    context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('SSL\\URSystem.crt','SSL\\URSystem.key')
    loger.info("URSecurity", "Succes load SSL")
    # Starting server
    server = Thread(target= lambda: app.run(host="localhost", ssl_context=context))
    server.start()
    loger.info("web components", "Succes starting server")
    # Starting UPStarter
    ups = Thread(target=lambda:programs_starter.UPS())
    ups.start()
    loger.info("UPStarter", "Succes starting UPStarter")
    # Joining processes
    loger.info("URSystem", "System started")
    ups.join()
    server.join()
    
    