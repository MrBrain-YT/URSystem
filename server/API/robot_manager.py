import time
import secrets

from flask import Flask, request

class RobotManager:
    
    def __init__(self):
        self.is_robot_ready_setted_false = True
    
    def __call__(self, app: Flask, loger) -> Flask:
        from server_functions import System, User, Robot
        from utils.loger import Robot_loger
        from API.multi_robots_system import URMSystem
        from API.kinematics_manager import KinematicsManager
        
        """ Get curent robot position"""
        @app.route('/GetCurentPosition', methods=['POST'])
        def GetCurentPosition():
            info = request.form
            robots = URMSystem().get_robots()
            if Robot.is_robot(info.get("token")):
                return str(robots[info.get("Robot")]["Position"])
            else:
                return "Your account is not a robot account"
            
        """ Set curent robot motor position"""
        @app.route('/SetCurentMotorPosition', methods=['POST'])
        def SetCurentMotorPosition():
            info = request.form
            robots = URMSystem().get_robots()
            if Robot.is_robot(info.get("token")):
                for i in range(1, int(robots[info.get("Robot")]["AngleCount"])+1):
                    robots[info.get("Robot")]["MotorsPosition"][f"J{i}"] = float(info.get(f'J{i}').replace(",", "."))
                    if robots[info.get("Robot")]["Emergency"] == "True":
                        robots[info.get("Robot")]["Position"][f"J{i}"] = float(info.get(f'J{i}').replace(",", "."))
                System().SaveToCache(robots=robots)
                return "True"
            else:
                return "Your account is not a robot account"
            
        """ Get curent robot speed """
        @app.route('/GetCurentSpeed', methods=['POST'])
        def GetCurentSpeed():
            info = request.form
            robots = URMSystem().get_robots()
            if Robot.is_robot(info.get("token")):
                return str(robots[info.get("Robot")]["MotorsSpeed"])
            else:
                return "Your account is not a robot account"
            
        """ Get robot ready parametr """
        @app.route('/GetRobotReady', methods=['POST'])
        def GetRobotReady():
            info = request.form
            robots = URMSystem().get_robots()
            if Robot.is_robot(info.get("token")):
                return str(robots[info.get("Robot")]["RobotReady"])
            else:
                return "Your account is not a robot account"
            
        """ Set robot ready parametr """
        @app.route('/SetRobotReady', methods=['POST'])
        def SetRobotReady():
            info = request.form
            robots = URMSystem().get_robots()
            if Robot.is_robot(info.get("token")):
                robots[info.get("Robot")]["RobotReady"] = info.get('RobotReady')
                if info.get('RobotReady') == "False":
                    self.is_robot_ready_setted_false = True
                    print("test")
                System().SaveToCache(robots=robots)
                User().update_token()
                return "True"
            else:
                return "Your account is not a robot account"
            
        ''' Activate and deativate emergency stop '''
        @app.route('/SetRobotEmergency', methods=['POST'])
        def SetRobotEmergency():
            info = request.form
            robots = URMSystem().get_robots()
            if (User.role_access(info.get("token"), "user") and \
            Robot.robot_access(robots, info.get("Robot"), info.get("Code"))) or Robot.is_robot(info.get("token")):
                robots[info.get("Robot")]["Emergency"] = "True" if info.get("State") == "True" else "False"
                robots[info.get("Robot")]["Position"] = robots[info.get("Robot")]["MotorsPosition"].copy()
                robots[info.get("Robot")]["RobotReady"] = "False"
                robots[info.get("Robot")]["Program"] = ""
                System().SaveToCache(robots=robots)
                User().update_token()
                Robot_loger(info.get("Robot")).info(f"Emergency stop button activated")
                return "True"
            else:
                loger.warning("URSystem", f"User access denied to set robot emergency because this not robot account. User with token: {request.form.get('token')}")
                return "Your account is not a robot account"
            
        ''' Get emergency stop '''
        @app.route('/GetRobotEmergency', methods=['POST'])
        def GetRobotEmergency():
            info = request.form
            robots = URMSystem().get_robots()
            if Robot.is_robot(info.get("token")):
                return robots[info.get("Robot")]["Emergency"]
            else:
                return "Your account is not a robot account"

        """ Curent robot position"""
        @app.route('/CurentPosition', methods=['POST'])
        def CurentPosition():
            info = request.form
            robots = URMSystem().get_robots()
            kinematics:dict = KinematicsManager().get_kinematics()
            if (User.role_access(info.get("token"), "user") and \
            Robot.robot_access(robots, info.get("Robot"), info.get("Code"))) or Robot.is_robot(info.get("token")):
                while True:
                    if robots[info.get("Robot")]["Emergency"] == "True":
                        Robot_loger(info.get("Robot")).error(f"The robot is currently in emergency stop")
                        return "The robot is currently in emergency stop"
                    else:
                        if not self.is_robot_ready_setted_false and bool(robots[info.get("Robot")]["RobotReady"]) == False:
                            continue
                        elif bool(robots[info.get("Robot")]["RobotReady"]) == True or self.is_robot_ready_setted_false:
                            if robots[info.get("Robot")]["RobotReady"] == "False":
                                continue
                            else:
                                if Robot.check_angles(info, robots) == False:
                                    Robot_loger(info.get("Robot")).error(f"Values ​​are not validated")
                                    return "Values ​​are not validated"
                                else:
                                    robots[info.get("Robot")]["RobotReady"] = "False"
                                    
                                    for i in range(1, int(robots[info.get("Robot")]["AngleCount"])+1):
                                        robots[info.get("Robot")]["Position"][f"J{i}"] = float(info.get(f'J{i}'))   
                                    
                                    if robots[info.get("Robot")]["Kinematic"] != "None":
                                        modul = kinematics[info.get("Robot")]
                                        result_forward = modul.Forward(float(info.get("J1")), float(info.get("J2")), float(info.get("J3")), float(info.get("J4")))
                                        robots[info.get("Robot")]["XYZposition"]["X"] = result_forward[0]
                                        robots[info.get("Robot")]["XYZposition"]["Y"] = result_forward[1]
                                        robots[info.get("Robot")]["XYZposition"]["Z"] = result_forward[2]
                                        
                                    self.is_robot_ready_setted_false = False
                                    
                                    System().SaveToCache(robots=robots)
                                    User().update_token()
                                    Robot_loger(info.get("Robot")).info(f"""Was setted robot current position: {
                                        info.get('J1')},{info.get('J2')},{info.get('J3')},{info.get('J4')}""")
                                    
                                    time.sleep(2)
                                    return "True"
                            
            else:
                return "You are not on the users list"
            
        """ Curent home position"""
        @app.route('/HomePosition', methods=['POST'])
        def HomePosition():
            info = request.form
            robots = URMSystem().get_robots()
            if User.role_access(info.get("token"), "user") and Robot.robot_access(robots, info.get("Robot"), info.get("Code")):
                if Robot.check_angles(info, robots) == False:
                    Robot_loger(info.get("Robot")).error(f"Values ​​are not validated")
                    return "Values ​​are not validated"
                else:
                    for i in range(1, int(robots[info.get("Robot")]["AngleCount"])+1):
                        robots[info.get("Robot")]["HomePosition"][f"J{i}"] = float(info.get(f'J{i}'))
                    System().SaveToCache(robots=robots)
                    User().update_token()
                    
                    Robot_loger(info.get("Robot")).info(f"""Was setted robot home position: {
                        info.get('J1')},{info.get('J2')},{info.get('J3')},{info.get('J4')}""")
                    return "True"
            else:
                return "You are not on the users list"

        """ Curent robot speed """
        @app.route('/CurentSpeed', methods=['POST'])
        def CurentSpeed():
            info = request.form
            robots = URMSystem().get_robots()
            if (User.role_access(info.get("token"), "user") and \
            Robot.robot_access(robots, info.get("Robot"), info.get("Code"))) or Robot.is_robot(info.get("token")):
                if robots[info.get("Robot")]["Emergency"] == "True":
                    Robot_loger(info.get("Robot")).error(f"The robot is currently in emergency stop")
                    return "The robot is currently in emergency stop"
                else:
                    for i in range(1, int(robots[info.get("Robot")]["AngleCount"])+1):
                        robots[info.get("Robot")]["MotorsSpeed"][f"J{i}"] = float(info.get(f'J{i}'))
                    System().SaveToCache(robots=robots)
                    User().update_token()
                    Robot_loger(info.get("Robot")).info(f"""Was setted robot current speed: {
                        info.get('J1')},{info.get('J2')},{info.get('J3')},{info.get('J4')}""")
                    return "True"
            else:
                return "You are not on the users list"

        """ Standart robot speed"""
        @app.route('/StandartSpeed', methods=['POST'])
        def StandartSpeed():
            info = request.form
            robots = URMSystem().get_robots()
            if User.role_access(info.get("token"), "user") and Robot.robot_access(robots, info.get("Robot"), info.get("Code")):
                for i in range(1, int(robots[info.get("Robot")]["AngleCount"])+1):
                    robots["First"]["StandartSpeed"][f"J{i}"] = float(info.get(f'J{i}'))
                System().SaveToCache(robots=robots)
                User().update_token()
                Robot_loger(info.get("Robot")).info(f"""Was setted robot standart speed: {
                        info.get('J1')},{info.get('J2')},{info.get('J3')},{info.get('J4')}""")
                return "True"
            else:
                return "You are not on the users list"
            
        """ Set program """
        @app.route('/SetProgram', methods=['POST'])
        def Program():
            info = request.form
            robots = URMSystem().get_robots()
            if User.role_access(info.get("token"), "user") and Robot.robot_access(robots, info.get("Robot"), info.get("Code")):
                if robots[info.get("Robot")]["Emergency"] == "True":
                    Robot_loger(info.get("Robot")).error(f"The robot is currently in emergency stop")
                    return "The robot is currently in emergency stop"
                else:
                    robots[info.get("Robot")]["Program"] = info.get('Program')
                    robots[info.get("Robot")]["ProgramToken"] = secrets.token_hex(16)
                    System().SaveToCache(robots=robots)
                    User().update_token()
                    Robot_loger(info.get("Robot")).info(f"Was setted robot programm")
                    return "True"
            else:
                return "You are not on the users list"

        """ Delete program """
        @app.route('/DeleteProgram', methods=['POST'])
        def DeleteProgram():
            info = request.form
            robots = URMSystem().get_robots()
            if User.role_access(info.get("token"), "user") and Robot.robot_access(robots, info.get("Robot"), info.get("Code")):
                robots[info.get("Robot")]["Program"] = ""
                robots[info.get("Robot")]["ProgramToken"] = ""
                System().SaveToCache(robots=robots)
                User().update_token()
                Robot_loger(info.get("Robot")).info(f"Was deleted robot programm")
                return "True"
            else:
                return "You are not on the users list"

        """ Get XYZ from angle robot position """
        @app.route('/angle_to_xyz', methods=['POST'])
        def angle_to_xyz():
            info = request.form
            robots = URMSystem().get_robots()
            kinematics:dict = KinematicsManager().get_kinematics()
            if (User.role_access(info.get("token"), "user") and \
            Robot.robot_access(robots, info.get("Robot"), info.get("Code"))) or Robot.is_robot(info.get("token")):
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
            robots = URMSystem().get_robots()
            kinematics:dict = KinematicsManager().get_kinematics()
            if (User.role_access(info.get("token"), "user") and \
            Robot.robot_access(robots, info.get("Robot"), info.get("Code"))) or Robot.is_robot(info.get("token")):
                if kinematics[info.get("Robot")] != "None":
                    try:
                        new_angles = {}
                        modul = kinematics[info.get("Robot")]
                        result_inverse = modul.Inverse(float(info.get("X")), float(info.get("Y")), float(info.get("Z")))
                        for j in range(1, int(robots[info.get("Robot")]["AngleCount"]) + 1):
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
            robots = URMSystem().get_robots()
            kinematics:dict = KinematicsManager().get_kinematics()
            if User.role_access(info.get("token"), "user") and Robot.robot_access(robots, info.get("Robot"), info.get("Code")):
                if kinematics[info.get("Robot")] != "None":
                    while True:
                        if robots[info.get("Robot")]["Emergency"] == "True":
                            Robot_loger(info.get("Robot")).error(f"The robot is currently in emergency stop")
                            return "The robot is currently in emergency stop"
                        else:
                            if robots[info.get("Robot")]["RobotReady"] == "False":
                                continue
                            else:
                                try:
                                    modul = kinematics[info.get("Robot")]
                                    result_inverse = modul.Inverse(float(info.get("X")), float(info.get("Y")), float(info.get("Z")))
                                    for j in range(1, int(robots[info.get("Robot")]["AngleCount"]) + 1):
                                        robots[info.get("Robot")]["Position"][f"J{j}"] = result_inverse[j-1]
                                        
                                    robots[info.get("Robot")]["XYZposition"]["X"] = float(info.get("X"))
                                    robots[info.get("Robot")]["XYZposition"]["Y"] = float(info.get("Y"))
                                    robots[info.get("Robot")]["XYZposition"]["Z"] = float(info.get("Z"))
                                    System().SaveToCache(robots=robots)
                                    User().update_token()
                                    
                                    Robot_loger(info.get("Robot")).info(f"""The robot has been moved to coordinates: X-{
                                        info.get("X")},Y-{info.get("Y")},Z-{info.get("Z")}""")
                                    
                                    time.sleep(2)
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
            robots = URMSystem().get_robots()
            if User.role_access(info.get("token"), "administrator") and Robot.robot_access(robots, info.get("Robot"), info.get("Code")):
                if robots[info.get("Robot")]["Emergency"] == "True":
                    Robot_loger(info.get("Robot")).error(f"The robot is currently in emergency stop")
                    return "The robot is currently in emergency stop"
                else:
                    for i in range(1, int(robots[info.get("Robot")]["AngleCount"])+1):
                        robots[info.get("Robot")]["MinAngles"][f"J{i}"] = float(info.get(f'J{i}'))
                    System().SaveToCache(robots=robots)
                    User().update_token()
                    Robot_loger(info.get("Robot")).info(f"""Was setted robot minimal angles: {
                        info.get('J1')},{info.get('J2')},{info.get('J3')},{info.get('J4')}""")
                    return robots[info.get("Robot")]["MinAngles"]
            else:
                loger.warning("URSystem", f"User access denied to set robot {info.get('Robot')} minimal angles. User with token: {request.form.get('token')}")
                return "You don't have enough rights"

        ''' Set maximum angle of rotation '''
        @app.route('/MaxAngles', methods=['POST'])
        def MaxAngles():
            info = request.form
            robots = URMSystem().get_robots()
            if User.role_access(info.get("token"), "administrator") and Robot.robot_access(robots, info.get("Robot"), info.get("Code")):
                if robots[info.get("Robot")]["Emergency"] == "True":
                    Robot_loger(info.get("Robot")).error(f"The robot is currently in emergency stop")
                    return "The robot is currently in emergency stop"
                else:
                    for i in range(1, int(robots[info.get("Robot")]["AngleCount"])+1):
                        robots[info.get("Robot")]["MaxAngles"][f"J{i}"] = float(info.get(f'J{i}'))
                    System().SaveToCache(robots=robots)
                    User().update_token()
                    Robot_loger(info.get("Robot")).info(f"""Was setted robot maximal angles: {
                        info.get('J1')},{info.get('J2')},{info.get('J3')},{info.get('J4')}""")
                    return robots[info.get("Robot")]["MaxAngles"]
            else:
                loger.warning("URSystem", f"User access denied to set robot {info.get('Robot')} maximal angles. User with token: {request.form.get('token')}")
                return "You don't have enough rights"

        ''' Set program is running '''
        @app.route('/SetProgramRun', methods=['POST'])
        def SetProgramRun():
            info = request.form
            robots = URMSystem().get_robots()
            if User.role_access(info.get("token"), "System"):
                robots[info.get("Robot")]["ProgramRunning"] = info.get("State")
                System().SaveToCache(robots=robots)
                User().update_token()
                return robots[info.get("Robot")]["ProgramRunning"]
            else:
                return "You don't have enough rights"
            
        return app