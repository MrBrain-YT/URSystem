import ssl
import importlib

from flask import Flask
from threading import Thread

import configuration.cache.robots_cache as robots_cache
# Import api
from api.frames_manager import FramesManagerAPI
from api.multi_robots_manager import MultiRobotsManagerAPI
from api.accounts_manager import AccountManagerAPI
from api.logs_manager import LogsManagerAPI
from api.tools_manager import ToolsManagerAPI
from api.bases_manager import BasesManagerAPI
from api.kinematics_manager import KinematicsManagerAPI
from api.robot_manager import RobotManagerAPI
from api.certs_manager import CertsManagerAPI
# import views
from views.home import home_bp
from views.certs import certs_bp
# import utilities
import utils.programs_starter as programs_starter
from utils.logger import Logger
from utils.public_loader.loader import loader
from utils.multicast_dns import register_mdns_service
from utils.certs_signer import create_certs
from utils.user_updater import update_token
from utils.sni_registator import SNIRegistrator

# Importing robots from cache
robots_list = robots_cache.robots
_robots = robots_cache.robots.keys()
for robot in _robots:
    robots_list[robot]["Program"] = ""
    robots_list[robot]["ProgramRunning"] = False
    robots_list[robot]["RobotReady"] = True
    robots_list[robot]["PositionID"] = ""
    robots_list[robot]["Emergency"] = False
    robots_list[robot]["MotorsSpeed"] = robots_list[robot]['standardSpeed'].copy()
    if isinstance(robots_list[robot]["Position"], dict):
        robots_list[robot]["Position"] = robots_list[robot]["MotorsPosition"].copy()
    elif isinstance(robots_list[robot]["Position"], list):
        robots_list[robot]["Position"] = robots_list[robot]["Position"][0].copy()
    
# importing all kinematics
kinematics = {}
for robot in _robots:
    if robots_list[robot]["Kinematic"] == None:
        kinematics[robot] = None
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
logger = Logger()

""" Server """
app = Flask(__name__,
            template_folder="templates",
            static_folder="static")

""" Frames manager """
app.register_blueprint(FramesManagerAPI(frames)())

""" URS tools system """
app.register_blueprint(ToolsManagerAPI(tools)())

""" URS bases system """
app.register_blueprint(BasesManagerAPI(bases)())

""" URMSystem """ # URMS - United Robotics Multi System
app.register_blueprint(MultiRobotsManagerAPI(robots)())

""" URAccount """
app.register_blueprint(AccountManagerAPI(users)())

""" URLogs """
app.register_blueprint(LogsManagerAPI()())

""" Kinematics manager """
app.register_blueprint(KinematicsManagerAPI(kinematics)())

""" Robot manager """
app.register_blueprint(RobotManagerAPI(robots)())

""" Certificates manager """
app.register_blueprint(CertsManagerAPI()())

""" Other sites """
app.register_blueprint(home_bp)
app.register_blueprint(certs_bp)

""" Public loader """
loader.init_app(app)
app = loader.app

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    # MDNS registrate
    register_mdns_service(host=host, port=port)
    logger.info(module="URDomen", msg="Multicast DNS service registered")
    # Creating SSL context
    create_certs()
    context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.sni_callback = SNIRegistrator(context).get_sni_callback()
    logger.info(module="URSecurity", msg="Succes load SSL")
    # Starting server
    server = Thread(target=lambda: app.run(host=host, port=port, ssl_context=context))
    server.start()
    logger.info(module="web components", msg="Succes starting server")
    # Starting UPStarter
    ups = Thread(target=lambda:programs_starter.UPS())
    ups.start()
    logger.info(module="UPStarter", msg="Succes starting UPStarter")
    # Joining processes
    logger.info(module="URSystem", msg="System started")
    ups.join()
    server.join()