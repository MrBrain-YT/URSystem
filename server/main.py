import ssl
import importlib

from flask import Flask
from threading import Thread

import configuration.robots_cache as robots_cache
from server_functions import User, System
import utils.programs_starter as programs_starter
from utils.loger import Loger
from API.frames_manager import FramesManager
from API.multi_robots_system import URMSystem
from API.accounts_manager import AccountManager
from API.logs_manager import LogsManager
from API.tools_manager import ToolsManager
from API.kinematics_manager import KinematicsManager
from API.robot_manager import RobotManager

# Importing robots from cache
robots_list = robots_cache.robots
robots = robots_cache.robots.keys()
for robot in robots:
    robots_list[robot]["Program"] = ""
    robots_list[robot]["ProgramRunning"] = "False"
    robots_list[robot]["RobotReady"] = "True"
    robots_list[robot]["Emergency"] = "False"
    robots_list[robot]["MotorsSpeed"] = robots_list[robot]['StandartSpeed'].copy()
    if isinstance(robots_list[robot]["Position"], dict):
        robots_list[robot]["Position"] = robots_list[robot]["MotorsPosition"].copy()
    elif isinstance(robots_list[robot]["Position"], list):
        robots_list[robot]["Position"] = robots_list[robot]["Position"][0].copy()
    
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
users = User().update_token()
loger = Loger()


""" Server """
app = Flask(__name__)

""" Init server functions"""
app = FramesManager(frames)(app, loger)

""" URS tool system """
app = ToolsManager(tools)(app, loger)

""" URMSystem """ # URMS - United Robotics Multi System
app = URMSystem(Robots)(app, loger)

""" URAccount """
app = AccountManager(users)(app, loger)

""" URLogs """
app = LogsManager()(app, frames)

""" Kinematics manager """
app = KinematicsManager(kinematics)(app, loger)

""" Robot manager """
app = RobotManager()(app, loger)


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
        <model-viewer class="model" src="static/Robot.gltf" ar ar-modes="webxr scene-viewer quick-look" camera-controls poster="poster.webp" shadow-intensity="1">
        </model-viewer>
        
    </body>
    <style>
        .model{
            width: 700px;
            height: 1000px;
        }
    </style>
</html>"""

# @app.route("/Robot.gltf")
# def model():
#     return open("./Robot.gltf", "rb").read()


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
    
    