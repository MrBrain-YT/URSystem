import secrets
import ast

from flask import Flask, request

class RobotManager:
    
    def __init__(self):
        from API.multi_robots_system import URMSystem
        robots = URMSystem().get_robots()
        globals()["is_robot_ready_setted_false"] = {}
        for robot_name in robots.keys():
            globals()["is_robot_ready_setted_false"][robot_name] = True
        self.loger_module = "URManager"
        
    def add_new_robot_ready(self, robot_name:str):
        globals()["is_robot_ready_setted_false"][robot_name] = True
    
    def remove_new_robot_ready(self, robot_name:str):
        del globals()["is_robot_ready_setted_false"][robot_name]
    
    def __call__(self, app: Flask) -> Flask:
        from server_functions import System, User, Robot
        from utils.loger import Robot_loger
        from API.multi_robots_system import URMSystem
        from API.kinematics_manager import KinematicsManager
        from API.access_checker import Access

        access = Access()
        
        """ Get curent robot position """
        @app.route('/GetCurentPosition', methods=['POST'])
        @access.check_robot_or_user(user_role="user")
        def GetCurentPosition():
            info = request.form
            robots = URMSystem().get_robots()
            return str(robots[info.get("Robot")]["Position"])
            
        """ Set curent robot motor position """
        @app.route('/SetCurentMotorsPosition', methods=['POST'])
        @access.check_robot
        def SetCurentMotorPosition():
            info = request.form
            robots = URMSystem().get_robots()
            kinematics:dict = KinematicsManager().get_kinematics()
            for i in range(1, int(robots[info.get("Robot")]["AngleCount"])+1):
                robots[info.get("Robot")]["MotorsPosition"][f"J{i}"] = float(info.get(f'J{i}').replace(",", "."))
                if robots[info.get("Robot")]["Emergency"] == "True":
                    robots[info.get("Robot")]["Position"][f"J{i}"] = float(info.get(f'J{i}').replace(",", "."))
            
            if robots[info.get("Robot")]["Kinematic"] != "None":
                modul = kinematics[info.get("Robot")]
                result_forward:dict = modul.Forward(float(info.get("J1").replace(",", ".")), float(info.get("J2").replace(",", ".")), float(info.get("J3").replace(",", ".")), float(info.get("J4").replace(",", ".")))
                robots[info.get("Robot")]["XYZposition"]["X"] = result_forward.get("X")
                robots[info.get("Robot")]["XYZposition"]["Y"] = result_forward.get("Y")
                robots[info.get("Robot")]["XYZposition"]["Z"] = result_forward.get("Z")        
            
            System().SaveToCache(robots=robots)
            return "True"
            
        """ Get curent robot speed """
        @app.route('/GetCurentSpeed', methods=['POST'])
        @access.check_robot
        def GetCurentSpeed():
            info = request.form
            robots = URMSystem().get_robots()
            return str(robots[info.get("Robot")]["MotorsSpeed"])
            
        """ Get robot ready parametr """
        @app.route('/GetRobotReady', methods=['POST'])
        @access.check_robot
        def GetRobotReady():
            info = request.form
            robots = URMSystem().get_robots()
            return str(robots[info.get("Robot")]["RobotReady"])
            
        """ Set robot ready parametr """
        @app.route('/SetRobotReady', methods=['POST'])
        @access.check_robot
        def SetRobotReady():
            info = request.form
            robots = URMSystem().get_robots()
            
            if info.get('RobotReady') == "False":
                globals()["is_robot_ready_setted_false"][info.get("Robot")] = True
                robots[info.get("Robot")]["RobotReady"] = info.get('RobotReady')
                
            if info.get('RobotReady') == "True":
                if not globals()["is_robot_ready_setted_false"][info.get("Robot")]:
                    return "False"
                else:
                    if not isinstance(robots[info.get("Robot")]["Position"], list):
                        robots[info.get("Robot")]["RobotReady"] = info.get('RobotReady')
                    else:
                        return "False"

            System().SaveToCache(robots=robots)
            User().update_token()
            return "True"
            
        ''' Activate and deativate emergency stop '''
        @app.route('/SetRobotEmergency', methods=['POST'])
        @access.check_robot_user(user_role="user", loger_module=self.loger_module)
        def SetRobotEmergency():
            info = request.form
            robots = URMSystem().get_robots()
            kinematics:dict = KinematicsManager().get_kinematics()
            robots[info.get("Robot")]["Emergency"] = "True" if info.get("State") == "True" else "False"
            if robots[info.get("Robot")]["Emergency"] == "True":
                robots[info.get("Robot")]["Position"] = robots[info.get("Robot")]["MotorsPosition"].copy()
                robots[info.get("Robot")]["MotorsSpeed"] = robots[info.get("Robot")]["StandartSpeed"].copy()
                robots[info.get("Robot")]["RobotReady"] = "False"
                robots[info.get("Robot")]["Program"] = ""
                
            if robots[info.get("Robot")]["Kinematic"] != "None":
                modul = kinematics[info.get("Robot")]
                pos = robots[info.get("Robot")]["Position"]
                result_forward:dict = modul.Forward(pos[0], pos[1], pos[2], pos[3])
                robots[info.get("Robot")]["XYZposition"]["X"] = result_forward.get("X")
                robots[info.get("Robot")]["XYZposition"]["Y"] = result_forward.get("Y")
                robots[info.get("Robot")]["XYZposition"]["Z"] = result_forward.get("Z")   
            
            System().SaveToCache(robots=robots)
            User().update_token()
            Robot_loger(info.get("Robot")).info(f"Emergency stop button activated")
            return "True"

            
        ''' Get emergency stop '''
        @app.route('/GetRobotEmergency', methods=['POST'])
        @access.check_robot
        def GetRobotEmergency():
            info = request.form
            robots = URMSystem().get_robots()
            return robots[info.get("Robot")]["Emergency"]


        """ Curent robot position"""
        @app.route('/CurentPosition', methods=['POST'])
        @access.check_robot_user_prog_token(user_role="user")
        def CurentPosition():
            info = request.form
            robots = URMSystem().get_robots()
            if robots[info.get("Robot")]["RobotReady"] == "True":
                globals()["is_robot_ready_setted_false"][info.get("Robot")] = False
            kinematics:dict = KinematicsManager().get_kinematics()
            while True:
                if robots[info.get("Robot")]["Emergency"] == "True":
                    Robot_loger(info.get("Robot")).error(f"The robot is currently in emergency stop")
                    return "The robot is currently in emergency stop"
                else:
                    if not globals()["is_robot_ready_setted_false"][info.get("Robot")] or bool(robots[info.get("Robot")]["RobotReady"]) == False:
                        continue
                    elif bool(robots[info.get("Robot")]["RobotReady"]) == True and globals()["is_robot_ready_setted_false"][info.get("Robot")] and\
                        not isinstance(robots[info.get("Robot")]["Position"], list):
                            if info.get("angles_data") is None:
                                if Robot.check_angles(info, robots) == False:
                                    Robot_loger(info.get("Robot")).error(f"Values ​​are not validated")
                                    return "Values ​​are not validated"
                                else:
                                    for i in range(1, int(robots[info.get("Robot")]["AngleCount"])+1):
                                        robots[info.get("Robot")]["Position"][f"J{i}"] = float(info.get(f'J{i}'))
                                    
                                    if robots[info.get("Robot")]["Kinematic"] != "None":
                                        modul = kinematics[info.get("Robot")]
                                        result_forward:dict = modul.Forward(float(info.get("J1")), float(info.get("J2")), float(info.get("J3")), float(info.get("J4")))
                                        robots[info.get("Robot")]["XYZposition"]["X"] = result_forward.get("X")
                                        robots[info.get("Robot")]["XYZposition"]["Y"] = result_forward.get("Y")
                                        robots[info.get("Robot")]["XYZposition"]["Z"] = result_forward.get("Z")
                                        
                                    Robot_loger(info.get("Robot")).info(f"""Was setted robot current position: {
                                        info.get('J1')},{info.get('J2')},{info.get('J3')},{info.get('J4')}""")
                            else:
                                # If getted not one point
                                new_pos = ast.literal_eval(info.get("angles_data"))
                                if isinstance(new_pos, list):
                                    robots[info.get("Robot")]["Position"] = new_pos
                                else:
                                    return "Multi points data is not valid"
                                
                            robots[info.get("Robot")]["RobotReady"] = "False"
                            System().SaveToCache(robots=robots)
                            globals()["is_robot_ready_setted_false"][info.get("Robot")] = False
                            User().update_token()
                            return "True"
                            
        """ Remove curent robot point position """
        @app.route('/RemoveCurentPointPosition', methods=['POST'])
        @access.check_robot_user_prog_token(user_role="user")
        def RemoveCurentPointPosition():
            info = request.form
            robots = URMSystem().get_robots()
            if isinstance(robots[info.get("Robot")]["Position"], list):
                if len(robots[info.get("Robot")]["Position"]) > 2:
                    robots[info.get("Robot")]["Position"] = robots[info.get("Robot")]["Position"][1::]
                else:
                    robots[info.get("Robot")]["Position"] = robots[info.get("Robot")]["Position"][-1]
                System().SaveToCache(robots=robots)
                User().update_token()
                return "True"
            elif isinstance(robots[info.get("Robot")]["Position"], dict):
                return "Position is not multi point"
            
        """ Remove all robot point positions """
        @app.route('/RemoveAllPointPosition', methods=['POST'])
        @access.check_robot_user_prog_token(user_role="user")
        def RemoveAllPointPosition():
            info = request.form
            robots = URMSystem().get_robots()
            if isinstance(robots[info.get("Robot")]["Position"], list):
                robots[info.get("Robot")]["Position"] = robots[info.get("Robot")]["Position"][-1]
                System().SaveToCache(robots=robots)
                User().update_token()
                return "True"
            elif isinstance(robots[info.get("Robot")]["Position"], dict):
                return "Position is not multi point"

            
        """ Curent home position"""
        @app.route('/HomePosition', methods=['POST'])
        @access.check_robot_user_prog(user_role="user", loger_module=self.loger_module)
        def HomePosition():
            info = request.form
            robots = URMSystem().get_robots()
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

        """ Curent robot speed """
        @app.route('/CurentSpeed', methods=['POST'])
        @access.check_robot_user_prog_token(user_role="user")
        def CurentSpeed():
            info = request.form
            robots = URMSystem().get_robots()
            if robots[info.get("Robot")]["Emergency"] == "True":
                Robot_loger(info.get("Robot")).error(f"The robot is currently in emergency stop")
                return "The robot is currently in emergency stop"
            else:
                if info.get("angles_data") is None:
                    for i in range(1, int(robots[info.get("Robot")]["AngleCount"])+1):
                        robots[info.get("Robot")]["MotorsSpeed"][f"J{i}"] = float(info.get(f'J{i}'))
                    
                    Robot_loger(info.get("Robot")).info(f"""Was setted robot current speed: {
                        info.get('J1')},{info.get('J2')},{info.get('J3')},{info.get('J4')}""")
                else:
                    # If getted not one point
                    new_pos = ast.literal_eval(info.get("angles_data"))
                    if isinstance(new_pos, list):
                        robots[info.get("Robot")]["MotorsSpeed"] = new_pos
                    else:
                        return "Multi points data is not valid"
                    
                System().SaveToCache(robots=robots)
                User().update_token()
                return "True"
                    
        """ Remove curent robot point speed """
        @app.route('/RemoveCurentPointSpeed', methods=['POST'])
        @access.check_robot_user_prog_token(user_role="user")
        def RemoveCurentPointSpeed():
            info = request.form
            robots = URMSystem().get_robots()
            if isinstance(robots[info.get("Robot")]["MotorsSpeed"], list):
                if len(robots[info.get("Robot")]["MotorsSpeed"]) > 2:
                    robots[info.get("Robot")]["MotorsSpeed"] = robots[info.get("Robot")]["MotorsSpeed"][1::]
                else:
                    robots[info.get("Robot")]["MotorsSpeed"] = robots[info.get("Robot")]["MotorsSpeed"][-1]
                System().SaveToCache(robots=robots)
                User().update_token()
                return "True"
            elif isinstance(robots[info.get("Robot")]["MotorsSpeed"], dict):
                return "MotorsSpeed is not multi point"
            
        """ Remove all robot point speeds """
        @app.route('/RemoveAllPointSpeed', methods=['POST'])
        @access.check_robot_user_prog_token(user_role="user")
        def RemoveAllPointSpeed():
            info = request.form
            robots = URMSystem().get_robots()
            if isinstance(robots[info.get("Robot")]["MotorsSpeed"], list):
                robots[info.get("Robot")]["MotorsSpeed"] = robots[info.get("Robot")]["MotorsSpeed"][-1]
                System().SaveToCache(robots=robots)
                User().update_token()
                return "True"
            elif isinstance(robots[info.get("Robot")]["MotorsSpeed"], dict):
                return "MotorsSpeed is not multi point"


        """ Standart robot speed"""
        @app.route('/StandartSpeed', methods=['POST'])
        @access.check_robot_user_prog(user_role="user", loger_module=self.loger_module)
        def StandartSpeed():
            info = request.form
            robots = URMSystem().get_robots()
            for i in range(1, int(robots[info.get("Robot")]["AngleCount"])+1):
                robots["First"]["StandartSpeed"][f"J{i}"] = float(info.get(f'J{i}'))
            System().SaveToCache(robots=robots)
            User().update_token()
            Robot_loger(info.get("Robot")).info(f"""Was setted robot standart speed: {
                    info.get('J1')},{info.get('J2')},{info.get('J3')},{info.get('J4')}""")
            return "True"

            
        """ Set program """
        @app.route('/SetProgram', methods=['POST'])
        @access.check_robot_user(user_role="user", loger_module=self.loger_module)
        def Program():
            info = request.form
            robots = URMSystem().get_robots()
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


        """ Delete program """
        @app.route('/DeleteProgram', methods=['POST'])
        @access.check_robot_user(user_role="user", loger_module=self.loger_module)
        def DeleteProgram():
            info = request.form
            robots = URMSystem().get_robots()
            robots[info.get("Robot")]["Program"] = ""
            robots[info.get("Robot")]["ProgramToken"] = ""
            System().SaveToCache(robots=robots)
            User().update_token()
            Robot_loger(info.get("Robot")).info(f"Was deleted robot programm")
            return "True"


        """ Get XYZ from angle robot position """
        @app.route('/angle_to_xyz', methods=['POST'])
        @access.check_robot_user(user_role="user", loger_module=self.loger_module)
        def angle_to_xyz():
            info = request.form
            kinematics:dict = KinematicsManager().get_kinematics()
            if kinematics[info.get("Robot")] != "None":
                try:
                    if info.get("positions_data") is None:
                        new_coord = {}
                        modul = kinematics[info.get("Robot")]
                        result_forward:dict = modul.Forward(float(info.get("J1")), float(info.get("J2")), float(info.get("J3")), float(info.get("J4")))
                        new_coord["X"] = result_forward.get("X")
                        new_coord["Y"] = result_forward.get("Y")
                        new_coord["Z"] = result_forward.get("Z")
                        return str(new_coord)
                    else:
                        angles = ast.literal_eval(info.get("angles_data"))
                        if isinstance(angles, list):
                            points = []
                            for pos in angles:
                                point_coords = {}
                                modul = kinematics[info.get("Robot")]
                                # set coords
                                result_inverse:dict = modul.Forward(pos[0], pos[1], pos[2])
                                new_coord["X"] = result_forward.get("X")
                                new_coord["Y"] = result_forward.get("Y")
                                new_coord["Z"] = result_forward.get("Z")
                                points.append(point_coords)
                            return str(points)
                        else:
                            return "Multi points data is not valid"
                except:
                    return "An error has occurred"
            else:
                return "This command does not work if you are not using kinematics"


        """ Get angle from XYZ robot position """
        @app.route('/XYZ_to_angle', methods=['POST'])
        @access.check_robot_user(user_role="user", loger_module=self.loger_module)
        def XYZ_to_angle():
            info = request.form
            robots = URMSystem().get_robots()
            kinematics:dict = KinematicsManager().get_kinematics()
            if kinematics[info.get("Robot")] != "None":
                try:
                    if info.get("positions_data") is None:
                        point_angles = {}
                        modul = kinematics[info.get("Robot")]
                        result_inverse:dict = modul.Inverse(float(info.get("X")), float(info.get("Y")), float(info.get("Z")))
                        for j in range(1, int(robots[info.get("Robot")]["AngleCount"]) + 1):
                            point_angles[f"J{j}"] = result_inverse.get(f"J{j}")
                        return str(point_angles)
                    else:
                        positions = ast.literal_eval(info.get("positions_data"))
                        if isinstance(positions, list):
                            angles = []
                            for pos in positions:
                                
                                point_angles = {}
                                modul = kinematics[info.get("Robot")]
                                result_inverse:dict = modul.Inverse(pos[0], pos[1], pos[2])
                                for j in range(1, int(robots[info.get("Robot")]["AngleCount"]) + 1):
                                    point_angles[f"J{j}"] = result_inverse.get(f"J{j}")
                                angles.append(point_angles)
                            return str(angles)
                        else:
                            return "Multi points data is not valid"
                except:
                    return "An error has occurred"
            else:
                return "This command does not work if you are not using kinematics"

            
        """ Set curent robot XYZ position """
        @app.route('/Move_XYZ', methods=['POST'])
        @access.check_robot_user_prog_token(user_role="user")
        def Move_XYZ():
            info = request.form
            robots = URMSystem().get_robots()
            if robots[info.get("Robot")]["RobotReady"] == "True":
                globals()["is_robot_ready_setted_false"][info.get("Robot")] = False
            kinematics:dict = KinematicsManager().get_kinematics()
            if kinematics[info.get("Robot")] != "None":
                while True:
                    if robots[info.get("Robot")]["Emergency"] == "True":
                        Robot_loger(info.get("Robot")).error(f"The robot is currently in emergency stop")
                        return "The robot is currently in emergency stop"
                    else:
                        if not globals()["is_robot_ready_setted_false"][info.get("Robot")] or bool(robots[info.get("Robot")]["RobotReady"]) == False:
                            continue
                        elif bool(robots[info.get("Robot")]["RobotReady"]) == True and globals()["is_robot_ready_setted_false"][info.get("Robot")] and\
                        not isinstance(robots[info.get("Robot")]["Position"], list):
                            try:
                                if info.get("points_data") is None:
                                    modul = kinematics[info.get("Robot")]
                                    result_inverse:dict = modul.Inverse(float(info.get("X")), float(info.get("Y")), float(info.get("Z")))
                                    for j in range(1, int(robots[info.get("Robot")]["AngleCount"]) + 1):
                                        robots[info.get("Robot")]["Position"][f"J{j}"] = result_inverse.get(f"J{j}")
                                        
                                    robots[info.get("Robot")]["XYZposition"]["X"] = float(info.get("X"))
                                    robots[info.get("Robot")]["XYZposition"]["Y"] = float(info.get("Y"))
                                    robots[info.get("Robot")]["XYZposition"]["Z"] = float(info.get("Z"))
                                    
                                    Robot_loger(info.get("Robot")).info(f"""The robot has been moved to coordinates: X-{
                                        info.get("X")},Y-{info.get("Y")},Z-{info.get("Z")}""")

                                else:
                                    # If getted not one point
                                    new_positions = ast.literal_eval(info.get("points_data"))
                                    if isinstance(new_positions, list):
                                        angles = []
                                        for pos in new_positions:
                                            modul = kinematics[info.get("Robot")]
                                            result_inverse:dict = modul.Inverse(float(info.get("X")), float(info.get("Y")), float(info.get("Z")))
                                            angles.append(result_inverse)
                                        robots[info.get("Robot")]["Position"] = angles
                                    else:
                                        return "Multi points data is not valid"
                                    
                                robots[info.get("Robot")]["RobotReady"] = "False"
                                System().SaveToCache(robots=robots)
                                globals()["is_robot_ready_setted_false"][info.get("Robot")] = False
                                User().update_token()
                                return "True"
                            except:
                                return "An error has occurred"       
            else:
                return "This command does not work if you are not using kinematics"


        ''' Set minimal angle of rotation '''
        @app.route('/MinAngles', methods=['POST'])
        @access.check_robot_user_prog(user_role="administrator", loger_module=self.loger_module)
        def MinAngles():
            info = request.form
            robots = URMSystem().get_robots()
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
                

        ''' Set maximum angle of rotation '''
        @app.route('/MaxAngles', methods=['POST'])
        @access.check_robot_user_prog(user_role="administrator", loger_module=self.loger_module)
        def MaxAngles():
            info = request.form
            robots = URMSystem().get_robots()
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

        ''' Set program is running '''
        @app.route('/SetProgramRun', methods=['POST'])
        @access.check_user(user_role="System", loger_module=self.loger_module)
        def SetProgramRun():
            info = request.form
            robots = URMSystem().get_robots()
            robots[info.get("Robot")]["ProgramRunning"] = info.get("State")
            System().SaveToCache(robots=robots)
            User().update_token()
            return robots[info.get("Robot")]["ProgramRunning"]
        
        
        return app