import ssl
import importlib

from flask import Flask
from threading import Thread

import configuration.cache.robots_cache as robots_cache
from utils.user_updater import update_token
import utils.programs_starter as programs_starter
from utils.logger import Logger
from API.frames_manager import FramesManagerAPI
from API.multi_robots_manager import MultiRobotsManagerAPI
from API.accounts_manager import AccountManagerAPI
from API.logs_manager import LogsManagerAPI
from API.tools_manager import ToolsManagerAPI
from API.bases_manager import BasesManagerAPI
from API.kinematics_manager import KinematicsManagerAPI
from API.robot_manager import RobotManagerAPI
from utils.public_loader.loader import loader
from utils.multicast_dns import register_mdns_service

# Importing robots from cache
robots_list = robots_cache.robots
_robots = robots_cache.robots.keys()
for robot in _robots:
    robots_list[robot]["Program"] = ""
    robots_list[robot]["ProgramRunning"] = False
    robots_list[robot]["RobotReady"] = True
    robots_list[robot]["PositionID"] = ""
    robots_list[robot]["Emergency"] = False
    robots_list[robot]["MotorsSpeed"] = robots_list[robot]['StandartSpeed'].copy()
    if isinstance(robots_list[robot]["Position"], dict):
        robots_list[robot]["Position"] = robots_list[robot]["MotorsPosition"].copy()
    elif isinstance(robots_list[robot]["Position"], list):
        robots_list[robot]["Position"] = robots_list[robot]["Position"][0].copy()
    
# importing all kinematics
kinematics = {}
for robot in _robots:
    if robots_list[robot]["Kinematic"] == "None":
        kinematics[robot] = "None"
    else:
        try:
            # import kinematics.First.kin
            kinematics[robot] = importlib.import_module(
                f'kinematics.{robots_list[robot]["Kinematic"]}.kin')
        except:
            # send to logs!
            print(f"For robot '{robot}' kinematic file not found ")

# Set global variables
robots = robots_list
tools = robots_cache.tools
bases = robots_cache.bases
frames = robots_cache.frames
users = update_token()
loger = Logger()

""" Server """
app = Flask(__name__)

""" Frames manager """
app = FramesManagerAPI(frames)(app)

""" URS tools system """
app = ToolsManagerAPI(tools)(app)

""" URS bases system """
app = BasesManagerAPI(bases)(app)

""" URMSystem """ # URMS - United Robotics Multi System
app = MultiRobotsManagerAPI(robots)(app)

""" URAccount """
app = AccountManagerAPI(users)(app)

""" URLogs """
app = LogsManagerAPI()(app)

""" Kinematics manager """
app = KinematicsManagerAPI(kinematics)(app)

""" Robot manager """
app = RobotManagerAPI(robots)(app)

""" Public loader """
loader.init_app(app)
app = loader.app

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

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    # MDNS registrate
    register_mdns_service(host=host, port=port)
    loger.info(module="URDomen", msg="Multicast DNS service registered")
    # Creating SSL context
    context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('SSL\\URSystem.crt','SSL\\URSystem.key')
    loger.info(module="URSecurity", msg="Succes load SSL")
    # Starting server
    server = Thread(target=lambda: app.run(host=host, port=port, ssl_context=context)) #
    server.start()
    loger.info(module="web components", msg="Succes starting server")
    # Starting UPStarter
    ups = Thread(target=lambda:programs_starter.UPS())
    ups.start()
    loger.info(module="UPStarter", msg="Succes starting UPStarter")
    # Joining processes
    loger.info(module="URSystem", msg="System started")
    ups.join()
    server.join()