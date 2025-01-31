import secrets
import ast
import json

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
            return json.dumps({"status": True, "info": f"Current robot '{info.get('Robot')}' angles position", "data": robots[info.get("Robot")]["Position"]}), 200
        
        """ Get curent robot position """
        @app.route('/GetXYZPosition', methods=['POST'])
        @access.check_robot_or_user(user_role="user")
        def GetXYZPosition():
            info = request.form
            robots = URMSystem().get_robots()
            return json.dumps({"status": True, "info": f"Current robot '{info.get('Robot')}' cartesian position", "data": robots[info.get("Robot")]["XYZposition"]}), 200
        
        """ Get robot angles count """
        @app.route('/GetRobotAnglesCount', methods=['POST'])
        @access.check_robot_or_user(user_role="user")
        def GetRobotAnglesCount():
            info = request.form
            robots = URMSystem().get_robots()
            return json.dumps({"status": True, "info": f"Current robot '{info.get('Robot')}' angles count", "data": robots[info.get("Robot")]["AngleCount"]}), 200
            
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
                robots[info.get("Robot")]["XYZposition"]["x"] = result_forward.get("X")
                robots[info.get("Robot")]["XYZposition"]["y"] = result_forward.get("Y")
                robots[info.get("Robot")]["XYZposition"]["z"] = result_forward.get("Z")        
            
            System().SaveToCache(robots=robots)
            return json.dumps({"status": True, "info": f"Motors position for robot '{info.get('Robot')}' has been setted"}), 200
            
        """ Get curent robot speed """
        @app.route('/GetCurentSpeed', methods=['POST'])
        @access.check_robot
        def GetCurentSpeed():
            info = request.form
            robots = URMSystem().get_robots()
            return json.dumps({"status": True, "info": f"Current robot '{info.get('Robot')}' angles speed", "data": robots[info.get("Robot")]["MotorsSpeed"]}), 200
            
        """ Get robot ready parametr """
        @app.route('/GetRobotReady', methods=['POST'])
        @access.check_robot
        def GetRobotReady():
            info = request.form
            robots = URMSystem().get_robots()
            return json.dumps({"status": True, "info": f"Current robot '{info.get('Robot')}' RobotReady parameter", "data": robots[info.get("Robot")]["RobotReady"]}), 200
        
        ''' Get emergency stop '''
        @app.route('/GetRobotEmergency', methods=['POST'])
        @access.check_robot
        def GetRobotEmergency():
            info = request.form
            robots = URMSystem().get_robots()
            return json.dumps({"status": True, "info": f"Current robot '{info.get('Robot')}' Emergency parameter", "data": robots[info.get("Robot")]["Emergency"]}), 200
            
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
                    return json.dumps({"status": False, "info": "The RobotReady parameter was not been seted"}), 400
                else:
                    if not isinstance(robots[info.get("Robot")]["Position"], list):
                        robots[info.get("Robot")]["RobotReady"] = info.get('RobotReady')
                    else:
                        return json.dumps({"status": False, "info": "The RobotReady parameter was not been seted"}), 400

            System().SaveToCache(robots=robots)
            User().update_token()
            return json.dumps({"status": True, "info": "The RobotReady parameter was been seted"}), 200
            
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
                robots[info.get("Robot")]["XYZposition"]["x"] = result_forward.get("X")
                robots[info.get("Robot")]["XYZposition"]["y"] = result_forward.get("Y")
                robots[info.get("Robot")]["XYZposition"]["z"] = result_forward.get("Z")   
            
            System().SaveToCache(robots=robots)
            User().update_token()
            Robot_loger(info.get("Robot")).info(f"Emergency stop button activated")
            return json.dumps({"status": True, "info": "The Emergency parameter was been seted"}), 200

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
                    log_message = f"The robot '{info.get('Robot')}' is currently in emergency stop"
                    Robot_loger(info.get("Robot")).error(log_message)
                    return json.dumps({"status": False, "info": log_message}), 400
                else:
                    if not globals()["is_robot_ready_setted_false"][info.get("Robot")] or bool(robots[info.get("Robot")]["RobotReady"]) == False:
                        continue
                    elif bool(robots[info.get("Robot")]["RobotReady"]) == True and globals()["is_robot_ready_setted_false"][info.get("Robot")] and\
                        not isinstance(robots[info.get("Robot")]["Position"], list):
                            if info.get("angles_data") is None:
                                if Robot.check_angles(info, robots) == False:
                                    log_message = "Angles values ​​are not correct"
                                    Robot_loger(info.get("Robot")).error(log_message)
                                    return json.dumps({"status": False, "info": log_message}), 400
                                else:
                                    for i in range(1, int(robots[info.get("Robot")]["AngleCount"])+1):
                                        robots[info.get("Robot")]["Position"][f"J{i}"] = float(info.get(f'J{i}'))
                                    
                                    if robots[info.get("Robot")]["Kinematic"] != "None":
                                        modul = kinematics[info.get("Robot")]
                                        result_forward:dict = modul.Forward(float(info.get("J1")), float(info.get("J2")), float(info.get("J3")), float(info.get("J4")))
                                        robots[info.get("Robot")]["XYZposition"]["x"] = result_forward.get("X")
                                        robots[info.get("Robot")]["XYZposition"]["y"] = result_forward.get("Y")
                                        robots[info.get("Robot")]["XYZposition"]["z"] = result_forward.get("Z")
                                        
                                    Robot_loger(info.get("Robot")).info(f"""Was setted robot current position: {
                                        info.get('J1')},{info.get('J2')},{info.get('J3')},{info.get('J4')}""")
                            else:
                                # If getted not one point
                                new_pos = ast.literal_eval(info.get("angles_data"))
                                if isinstance(new_pos, list):
                                    robots[info.get("Robot")]["Position"] = new_pos
                                else:
                                    return json.dumps({"status": False, "info": "Multi points data is not valid"}), 400
                                
                            robots[info.get("Robot")]["RobotReady"] = "False"
                            System().SaveToCache(robots=robots)
                            globals()["is_robot_ready_setted_false"][info.get("Robot")] = False
                            User().update_token()
                            return json.dumps({"status": True, "info": f"Current robot '{info.get('Robot')}' position was been seted"}), 200
                            
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
                return json.dumps({"status": True, "info": "Curent robot point position was been removed"}), 200
            elif isinstance(robots[info.get("Robot")]["Position"], dict):
                return json.dumps({"status": False, "info": "Curent robot point position is not multi point"}), 400
            
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
                return json.dumps({"status": True, "info": "All robot points from multi point position was been removed"}), 200
            elif isinstance(robots[info.get("Robot")]["Position"], dict):
                return json.dumps({"status": False, "info": "Curent robot point position is not multi point"}), 400
            
        """ Curent home position"""
        @app.route('/HomePosition', methods=['POST'])
        @access.check_robot_user_prog(user_role="user", loger_module=self.loger_module)
        def HomePosition():
            info = request.form
            robots = URMSystem().get_robots()
            if Robot.check_angles(info, robots) == False:
                log_message = "Angles values ​​are not correct"
                Robot_loger(info.get("Robot")).error(log_message)
                return json.dumps({"status": False, "info": log_message}), 400
            else:
                for i in range(1, int(robots[info.get("Robot")]["AngleCount"])+1):
                    robots[info.get("Robot")]["HomePosition"][f"J{i}"] = float(info.get(f'J{i}'))
                System().SaveToCache(robots=robots)
                User().update_token()
                
                Robot_loger(info.get("Robot")).info(f"""Was setted robot home position: {
                    info.get('J1')},{info.get('J2')},{info.get('J3')},{info.get('J4')}""")
                return json.dumps({"status": True, "info": f"Was setted robot '{info.get('Robot')}' home position"}), 200

        """ Curent robot speed """
        @app.route('/CurentSpeed', methods=['POST'])
        @access.check_robot_user_prog_token(user_role="user")
        def CurentSpeed():
            info = request.form
            robots = URMSystem().get_robots()
            if robots[info.get("Robot")]["Emergency"] == "True":
                log_message = f"The robot is currently in emergency stop"
                Robot_loger(info.get("Robot")).error(log_message)
                return json.dumps({"status": False, "info": log_message}), 400
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
                        return json.dumps({"status": False, "info": "Multi points agle speed data is not valid"}), 400
                    
                System().SaveToCache(robots=robots)
                User().update_token()
                return json.dumps({"status": True, "info": "The robot speed parameter was been seted"}), 200
                    
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
                return json.dumps({"status": True, "info": "Curent robot point speed was been removed"}), 200
            elif isinstance(robots[info.get("Robot")]["MotorsSpeed"], dict):
                return json.dumps({"status": False, "info": "Curent robot point speed is not multi point"}), 400
            
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
                return json.dumps({"status": True, "info": "All robot points from multi point speed was been removed"}), 200
            elif isinstance(robots[info.get("Robot")]["Position"], dict):
                return json.dumps({"status": False, "info": "Curent robot point speed is not multi point"}), 400

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
            return json.dumps({"status": True, "info": "The robot default speed parameter was been seted"}), 200
            
        """ Set program """
        @app.route('/SetProgram', methods=['POST'])
        @access.check_robot_user(user_role="user", loger_module=self.loger_module)
        def Program():
            info = request.form
            robots = URMSystem().get_robots()
            if robots[info.get("Robot")]["Emergency"] == "True":
                log_message = f"The robot '{info.get('Robot')}' is currently in emergency stop"
                Robot_loger(info.get("Robot")).error(log_message)
                return json.dumps({"status": False, "info": log_message}), 400
            else:
                robots[info.get("Robot")]["Program"] = info.get('Program')
                robots[info.get("Robot")]["ProgramToken"] = secrets.token_hex(16)
                System().SaveToCache(robots=robots)
                User().update_token()
                log_message = "Was setted robot programm"
                Robot_loger(info.get("Robot")).info(log_message)
                return json.dumps({"status": True, "info": log_message}), 200

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
            log_message = "Was deleted robot programm"
            Robot_loger(info.get("Robot")).info(log_message)
            return json.dumps({"status": True, "info": log_message}), 200


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
                        new_coord["x"] = result_forward.get("x")
                        new_coord["y"] = result_forward.get("y")
                        new_coord["z"] = result_forward.get("z")
                        return json.dumps({"status": True, "info": "Angles to cartesian point converter", "data": new_coord}), 200
                    else:
                        angles = ast.literal_eval(info.get("angles_data"))
                        if isinstance(angles, list):
                            points = []
                            for pos in angles:
                                point_coords = {}
                                modul = kinematics[info.get("Robot")]
                                # set coords
                                result_inverse:dict = modul.Forward(pos[0], pos[1], pos[2])
                                new_coord["x"] = result_forward.get("x")
                                new_coord["y"] = result_forward.get("y")
                                new_coord["z"] = result_forward.get("z")
                                points.append(point_coords)
                            return json.dumps({"status": True, "info": "(multi) angles to cartesian points converter", "data": points}), 200
                        else:
                            return json.dumps({"status": False, "info": "Multi points data is not valid"}), 400
                except:
                    return json.dumps({"status": False, "info": "An error has occurred"}), 400
            else:
                return json.dumps({"status": False, "info": "This command does not work if you are not using kinematics"}), 400

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
                        result_inverse:dict = modul.Inverse(float(info.get("x")), float(info.get("y")), float(info.get("z")))
                        for j in range(1, int(robots[info.get("Robot")]["AngleCount"]) + 1):
                            point_angles[f"J{j}"] = result_inverse.get(f"J{j}")
                        return json.dumps({"status": True, "info": "Cartesian point to angles converter", "data": point_angles}), 200
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
                            return json.dumps({"status": True, "info": "(multi) cartesian point to angles converter", "data": angles}), 200
                        else:
                            return json.dumps({"status": False, "info": "Multi points data is not valid"}), 400
                except:
                    return json.dumps({"status": False, "info": "An error has occurred"}), 400
            else:
                return json.dumps({"status": False, "info": "This command does not work if you are not using kinematics"}), 400
            
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
                        log_message = f"The robot '{info.get('Robot')}' is currently in emergency stop"
                        Robot_loger(info.get("Robot")).error(log_message)
                        return json.dumps({"status": False, "info": log_message}), 400
                    else:
                        if not globals()["is_robot_ready_setted_false"][info.get("Robot")] or bool(robots[info.get("Robot")]["RobotReady"]) == False:
                            continue
                        elif bool(robots[info.get("Robot")]["RobotReady"]) == True and globals()["is_robot_ready_setted_false"][info.get("Robot")] and\
                        not isinstance(robots[info.get("Robot")]["Position"], list):
                            try:
                                if info.get("points_data") is None:
                                    modul = kinematics[info.get("Robot")]
                                    result_inverse:dict = modul.Inverse(float(info.get("x")), float(info.get("y")), float(info.get("z")))
                                    for j in range(1, int(robots[info.get("Robot")]["AngleCount"]) + 1):
                                        robots[info.get("Robot")]["Position"][f"J{j}"] = result_inverse.get(f"J{j}")
                                        
                                    robots[info.get("Robot")]["XYZposition"]["x"] = float(info.get("x"))
                                    robots[info.get("Robot")]["XYZposition"]["y"] = float(info.get("y"))
                                    robots[info.get("Robot")]["XYZposition"]["z"] = float(info.get("z"))
                                    
                                    Robot_loger(info.get("Robot")).info(f"""The robot has been moved to coordinates: X-{
                                        info.get("X")},Y-{info.get("Y")},Z-{info.get("Z")}""")
                                else:
                                    # If getted not one point
                                    new_positions = ast.literal_eval(info.get("points_data"))
                                    if isinstance(new_positions, list):
                                        angles = []
                                        for pos in new_positions:
                                            modul = kinematics[info.get("Robot")]
                                            result_inverse:dict = modul.Inverse(float(info.get("x")), float(info.get("y")), float(info.get("z")))
                                            angles.append(result_inverse)
                                        robots[info.get("Robot")]["Position"] = angles
                                    else:
                                        return json.dumps({"status": False, "info": "Multi points data is not valid"}), 400
                                    
                                robots[info.get("Robot")]["RobotReady"] = "False"
                                System().SaveToCache(robots=robots)
                                globals()["is_robot_ready_setted_false"][info.get("Robot")] = False
                                User().update_token()
                                return json.dumps({"status": True, "info": f"Current robot '{info.get('Robot')}' cartesian position was been seted"}), 200
                            except:
                                return json.dumps({"status": False, "info": "An error has occurred"}), 400    
            else:
                return json.dumps({"status": False, "info": "This command does not work if you are not using kinematics"}), 400

        ''' Set minimal angle of rotation '''
        @app.route('/MinAngles', methods=['POST'])
        @access.check_robot_user_prog(user_role="administrator", loger_module=self.loger_module)
        def MinAngles():
            info = request.form
            robots = URMSystem().get_robots()
            if robots[info.get("Robot")]["Emergency"] == "True":
                log_message = f"The robot '{info.get('Robot')}' is currently in emergency stop"
                Robot_loger(info.get("Robot")).error(log_message)
                return json.dumps({"status": False, "info": log_message}), 400
            else:
                for i in range(1, int(robots[info.get("Robot")]["AngleCount"])+1):
                    robots[info.get("Robot")]["MinAngles"][f"J{i}"] = float(info.get(f'J{i}'))
                System().SaveToCache(robots=robots)
                User().update_token()
                Robot_loger(info.get("Robot")).info(f"""Was setted robot minimal angles: {
                    info.get('J1')},{info.get('J2')},{info.get('J3')},{info.get('J4')}""")
                return json.dumps({"status": True, "info": f"Robot '{info.get('Robot')}' minimal angles data was been seted"}), 200
                

        ''' Set maximum angle of rotation '''
        @app.route('/MaxAngles', methods=['POST'])
        @access.check_robot_user_prog(user_role="administrator", loger_module=self.loger_module)
        def MaxAngles():
            info = request.form
            robots = URMSystem().get_robots()
            if robots[info.get("Robot")]["Emergency"] == "True":
                log_message = f"The robot '{info.get('Robot')}' is currently in emergency stop"
                Robot_loger(info.get("Robot")).error(log_message)
                return json.dumps({"status": False, "info": log_message}), 400
            else:
                for i in range(1, int(robots[info.get("Robot")]["AngleCount"])+1):
                    robots[info.get("Robot")]["MaxAngles"][f"J{i}"] = float(info.get(f'J{i}'))
                System().SaveToCache(robots=robots)
                User().update_token()
                Robot_loger(info.get("Robot")).info(f"""Was setted robot maximal angles: {
                    info.get('J1')},{info.get('J2')},{info.get('J3')},{info.get('J4')}""")
                return json.dumps({"status": True, "info": f"Robot '{info.get('Robot')}' maximal angles data was been seted"}), 200

        ''' Set program is running '''
        @app.route('/SetProgramRun', methods=['POST'])
        @access.check_user(user_role="System", loger_module=self.loger_module)
        def SetProgramRun():
            info = request.form
            robots = URMSystem().get_robots()
            robots[info.get("Robot")]["ProgramRunning"] = info.get("State")
            System().SaveToCache(robots=robots)
            User().update_token()
            return json.dumps({"status": True, "info": f"Robot '{info.get('Robot')}' ProgramRun parameter was been seted"}), 200
        
        return app