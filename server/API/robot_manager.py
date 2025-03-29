import secrets
import ast
import time

from flask import Flask, request, jsonify

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
            info = request.json
            time.sleep(0.2)
            robots = URMSystem().get_robots()
            return jsonify({"status": True, "info": f"Curent robot '{info.get('robot')}' angles position", "data": robots[info.get("robot")]["Position"]}), 200
        
        """ Get curent robot speed """
        @app.route('/GetCurentSpeed', methods=['POST'])
        @access.check_robot
        def GetCurentSpeed():
            info = request.json
            time.sleep(0.2)
            robots = URMSystem().get_robots()
            return jsonify({"status": True, "info": f"Curent robot '{info.get('robot')}' angles speed", "data": robots[info.get("robot")]["MotorsSpeed"]}), 200
        
        """ Get curent robot position """
        @app.route('/GetXYZPosition', methods=['POST'])
        @access.check_robot_or_user(user_role="user")
        def GetXYZPosition():
            info = request.json
            robots = URMSystem().get_robots()
            return jsonify({"status": True, "info": f"Curent robot '{info.get('robot')}' cartesian position", "data": robots[info.get("robot")]["XYZposition"]}), 200
        
        """ Get robot angles count """
        @app.route('/GetRobotAnglesCount', methods=['POST'])
        @access.check_robot_or_user(user_role="user")
        def GetRobotAnglesCount():
            info = request.json
            robots = URMSystem().get_robots()
            return jsonify({"status": True, "info": f"Curent robot '{info.get('robot')}' angles count", "data": robots[info.get("robot")]["AngleCount"]}), 200
            
        """ Set curent robot motor position """
        @app.route('/SetCurentMotorsPosition', methods=['POST'])
        @access.check_robot
        def SetCurentMotorPosition():
            info = request.json
            robots = URMSystem().get_robots()
            kinematics:dict = KinematicsManager().get_kinematics()
            for i in range(1, int(robots[info.get("robot")]["AngleCount"])+1):
                robots[info.get("robot")]["MotorsPosition"][f"J{i}"] = info.get("angles").get(f'J{i}')
                if robots[info.get("robot")]["Emergency"] == True:
                    robots[info.get("robot")]["Position"][f"J{i}"] = info.get("angles").get(f'J{i}')
            
            if robots[info.get("robot")]["Kinematic"] != "None":
                modul = kinematics[info.get("robot")]
                result_forward:dict = modul.Forward(info.get("angles").get("J1"), info.get("angles").get("J2"), info.get("angles").get("J3"), info.get("angles").get("J4"))
                robots[info.get("robot")]["XYZposition"]["x"] = result_forward.get("x")
                robots[info.get("robot")]["XYZposition"]["y"] = result_forward.get("y")
                robots[info.get("robot")]["XYZposition"]["z"] = result_forward.get("z")        
            
            System().SaveToCache(robots=robots)
            return jsonify({"status": True, "info": f"Motors position for robot '{info.get('robot')}' has been setted"}), 200
            
        """ Get robot ready parametr """
        @app.route('/GetRobotReady', methods=['POST'])
        @access.check_robot
        def GetRobotReady():
            info = request.json
            robots = URMSystem().get_robots()
            return jsonify({"status": True, "info": f"Curent robot '{info.get('robot')}' RobotReady parameter", "data": robots[info.get("robot")]["RobotReady"]}), 200
        
        ''' Get emergency stop '''
        @app.route('/GetRobotEmergency', methods=['POST'])
        @access.check_robot_or_user(user_role="user")
        def GetRobotEmergency():
            info = request.json
            robots = URMSystem().get_robots()
            return jsonify({"status": True, "info": f"Curent robot '{info.get('robot')}' Emergency parameter", "data": robots[info.get("robot")]["Emergency"]}), 200
            
        """ Set robot ready parametr """
        @app.route('/SetRobotReady', methods=['POST'])
        @access.check_robot
        def SetRobotReady():
            info = request.json
            robots = URMSystem().get_robots()
            if info.get('state') == False:
                globals()["is_robot_ready_setted_false"][info.get("robot")] = True
                robots[info.get("robot")]["RobotReady"] = info.get('state')
                
            if info.get('state') == True:
                if not globals()["is_robot_ready_setted_false"][info.get("robot")]: 
                    return jsonify({"status": False, "info": "The RobotReady parameter was not been seted"}), 400
                else:
                    if not isinstance(robots[info.get("robot")]["Position"], list):
                        robots[info.get("robot")]["RobotReady"] = info.get('state')
                    else:
                        return jsonify({"status": False, "info": "The RobotReady parameter was not been seted"}), 400

            System().SaveToCache(robots=robots)
            User().update_token()
            return jsonify({"status": True, "info": "The RobotReady parameter was been seted"}), 200
            
        ''' Activate and deativate emergency stop '''
        @app.route('/SetRobotEmergency', methods=['POST'])
        @access.check_robot_user(user_role="user", loger_module=self.loger_module)
        def SetRobotEmergency():
            info = request.json
            robots = URMSystem().get_robots()
            kinematics:dict = KinematicsManager().get_kinematics()
            robots[info.get("robot")]["Emergency"] = True if info.get("state") == True else False
            if robots[info.get("robot")]["Emergency"] == True:
                robots[info.get("robot")]["Position"] = robots[info.get("robot")]["MotorsPosition"].copy()
                robots[info.get("robot")]["MotorsSpeed"] = robots[info.get("robot")]["StandartSpeed"].copy()
                robots[info.get("robot")]["RobotReady"] = False
                robots[info.get("robot")]["Program"] = ""
                
            if robots[info.get("robot")]["Kinematic"] != "None":
                modul = kinematics[info.get("robot")]
                pos = robots[info.get("robot")]["Position"]
                result_forward:dict = modul.Forward(pos["J1"], pos["J2"], pos["J3"], pos["J4"])
                robots[info.get("robot")]["XYZposition"]["x"] = result_forward.get("x")
                robots[info.get("robot")]["XYZposition"]["y"] = result_forward.get("y")
                robots[info.get("robot")]["XYZposition"]["z"] = result_forward.get("z")   
            
            System().SaveToCache(robots=robots)
            User().update_token()
            Robot_loger(info.get("robot")).info(f"Emergency stop button activated")
            return jsonify({"status": True, "info": "The Emergency parameter was been seted"}), 200

        """ Curent robot position"""
        @app.route('/CurentPosition', methods=['POST'])
        @access.check_robot_user_prog_token(user_role="user")
        def CurentPosition():
            info = request.json
            print(info)
            robots = URMSystem().get_robots()
            if robots[info.get("robot")]["RobotReady"] == True:
                globals()["is_robot_ready_setted_false"][info.get("robot")] = False
            kinematics:dict = KinematicsManager().get_kinematics()
            while True:
                if robots[info.get("robot")]["Emergency"] == True:
                    log_message = f"The robot '{info.get('robot')}' is currently in emergency stop"
                    Robot_loger(info.get("robot")).error(log_message)
                    return jsonify({"status": False, "info": log_message}), 400
                else:
                    if not globals()["is_robot_ready_setted_false"][info.get("robot")] or bool(robots[info.get("robot")]["RobotReady"]) == False:
                        continue
                    elif robots[info.get("robot")]["RobotReady"] == True and globals()["is_robot_ready_setted_false"][info.get("robot")] and\
                        not isinstance(robots[info.get("robot")]["Position"], list):
                            if info.get("angles_data") is None:
                                if Robot.check_angles(info, robots) == False:
                                    log_message = "Angles values ​​are not correct"
                                    Robot_loger(info.get("robot")).error(log_message)
                                    return jsonify({"status": False, "info": log_message}), 400
                                else:
                                    for i in range(1, int(robots[info.get("robot")]["AngleCount"])+1):
                                        robots[info.get("robot")]["Position"][f"J{i}"] = info.get("angles").get(f'J{i}')
                                    
                                    if robots[info.get("robot")]["Kinematic"] != "None":
                                        modul = kinematics[info.get("robot")]
                                        result_forward:dict = modul.Forward(info.get("angles").get("J1"), info.get("angles").get("J2"), info.get("angles").get("J3"), info.get("angles").get("J4"))
                                        robots[info.get("robot")]["XYZposition"]["x"] = result_forward.get("x")
                                        robots[info.get("robot")]["XYZposition"]["y"] = result_forward.get("y")
                                        robots[info.get("robot")]["XYZposition"]["z"] = result_forward.get("z")
                                        
                                    Robot_loger(info.get("robot")).info(f"""Was setted robot current position: {
                                        info.get("angles").get('J1')},{info.get("angles").get('J2')},{info.get("angles").get('J3')},{info.get("angles").get('J4')}""")
                            else:
                                # If getted not one point
                                new_pos = ast.literal_eval(info.get("angles_data"))
                                if isinstance(new_pos, list):
                                    robots[info.get("robot")]["Position"] = new_pos
                                else:
                                    return jsonify({"status": False, "info": "Multi points data is not valid"}), 400
                                
                            robots[info.get("robot")]["RobotReady"] = False
                            System().SaveToCache(robots=robots)
                            globals()["is_robot_ready_setted_false"][info.get("robot")] = False
                            User().update_token()
                            return jsonify({"status": True, "info": f"Curent robot '{info.get('robot')}' position was been seted"}), 200
                            
        """ Remove curent robot point position """
        @app.route('/RemoveCurentPointPosition', methods=['POST'])
        @access.check_robot_user_prog_token(user_role="user")
        def RemoveCurentPointPosition():
            info = request.json
            robots = URMSystem().get_robots()
            if isinstance(robots[info.get("robot")]["Position"], list):
                if len(robots[info.get("robot")]["Position"]) > 2:
                    robots[info.get("robot")]["Position"] = robots[info.get("robot")]["Position"][1::]
                else:
                    robots[info.get("robot")]["Position"] = robots[info.get("robot")]["Position"][-1]
                System().SaveToCache(robots=robots)
                User().update_token()
                return jsonify({"status": True, "info": "Curent robot point position was been removed"}), 200
            elif isinstance(robots[info.get("robot")]["Position"], dict):
                return jsonify({"status": False, "info": "Curent robot point position is not multi point"}), 400
            
        """ Remove all robot point positions """
        @app.route('/RemoveAllPointPosition', methods=['POST'])
        @access.check_robot_user_prog_token(user_role="user")
        def RemoveAllPointPosition():
            info = request.json
            robots = URMSystem().get_robots()
            if isinstance(robots[info.get("robot")]["Position"], list):
                robots[info.get("robot")]["Position"] = robots[info.get("robot")]["Position"][-1]
                System().SaveToCache(robots=robots)
                User().update_token()
                return jsonify({"status": True, "info": "All robot points from multi point position was been removed"}), 200
            elif isinstance(robots[info.get("robot")]["Position"], dict):
                return jsonify({"status": False, "info": "Curent robot point position is not multi point"}), 400

        """ Curent home position"""
        @app.route('/HomePosition', methods=['POST'])
        @access.check_robot_user_prog(user_role="user", loger_module=self.loger_module)
        def HomePosition():
            info = request.json
            robots = URMSystem().get_robots()
            if Robot.check_angles(info, robots) == False:
                log_message = "Angles values ​​are not correct"
                Robot_loger(info.get("robot")).error(log_message)
                return jsonify({"status": False, "info": log_message}), 400
            else:
                for i in range(1, int(robots[info.get("robot")]["AngleCount"])+1):
                    robots[info.get("robot")]["HomePosition"][f"J{i}"] = float(info.get("angles").get(f'J{i}'))
                System().SaveToCache(robots=robots)
                User().update_token()
                
                Robot_loger(info.get("robot")).info(f"""Was setted robot home position: {
                    info.get("angles").get('J1')},{info.get("angles").get('J2')},{info.get("angles").get('J3')},{info.get("angles").get('J4')}""")
                return jsonify({"status": True, "info": f"Was setted robot '{info.get('robot')}' home position"}), 200

        """ Curent robot speed """
        @app.route('/CurentSpeed', methods=['POST'])
        @access.check_robot_user_prog_token(user_role="user")
        def CurentSpeed():
            info = request.json
            print(info)
            robots = URMSystem().get_robots()
            if robots[info.get("robot")]["Emergency"] == True:
                log_message = f"The robot is currently in emergency stop"
                Robot_loger(info.get("robot")).error(log_message)
                return jsonify({"status": False, "info": log_message}), 400
            else:
                if info.get("angles_data") is None:
                    for i in range(1, int(robots[info.get("robot")]["AngleCount"])+1):
                        robots[info.get("robot")]["MotorsSpeed"][f"J{i}"] = float(info.get("angles").get(f'J{i}'))
                    
                    Robot_loger(info.get("robot")).info(f"""Was setted robot current speed: {
                        info.get("angles").get('J1')},{info.get("angles").get('J2')},{info.get("angles").get('J3')},{info.get("angles").get('J4')}""")
                else:
                    # If getted not one point
                    new_pos = ast.literal_eval(info.get("angles_data"))
                    if isinstance(new_pos, list):
                        robots[info.get("robot")]["MotorsSpeed"] = new_pos
                    else:
                        return jsonify({"status": False, "info": "Multi points agle speed data is not valid"}), 400
                    
                System().SaveToCache(robots=robots)
                User().update_token()
                return jsonify({"status": True, "info": "The robot speed parameter was been seted"}), 200
                    
        """ Remove curent robot point speed """
        @app.route('/RemoveCurentPointSpeed', methods=['POST'])
        @access.check_robot_user_prog_token(user_role="user")
        def RemoveCurentPointSpeed():
            info = request.json
            robots = URMSystem().get_robots()
            if isinstance(robots[info.get("robot")]["MotorsSpeed"], list):
                if len(robots[info.get("robot")]["MotorsSpeed"]) > 2:
                    robots[info.get("robot")]["MotorsSpeed"] = robots[info.get("robot")]["MotorsSpeed"][1::]
                else:
                    robots[info.get("robot")]["MotorsSpeed"] = robots[info.get("robot")]["MotorsSpeed"][-1]
                System().SaveToCache(robots=robots)
                User().update_token()
                return jsonify({"status": True, "info": "Curent robot point speed was been removed"}), 200
            elif isinstance(robots[info.get("robot")]["MotorsSpeed"], dict):
                return jsonify({"status": False, "info": "Curent robot point speed is not multi point"}), 400
            
        """ Remove all robot point speeds """
        @app.route('/RemoveAllPointSpeed', methods=['POST'])
        @access.check_robot_user_prog_token(user_role="user")
        def RemoveAllPointSpeed():
            info = request.json
            robots = URMSystem().get_robots()
            if isinstance(robots[info.get("robot")]["MotorsSpeed"], list):
                robots[info.get("robot")]["MotorsSpeed"] = robots[info.get("robot")]["MotorsSpeed"][-1]
                System().SaveToCache(robots=robots)
                User().update_token()
                return jsonify({"status": True, "info": "All robot points from multi point speed was been removed"}), 200
            elif isinstance(robots[info.get("robot")]["Position"], dict):
                return jsonify({"status": False, "info": "Curent robot point speed is not multi point"}), 400

        """ Standart robot speed"""
        @app.route('/StandartSpeed', methods=['POST'])
        @access.check_robot_user_prog(user_role="user", loger_module=self.loger_module)
        def StandartSpeed():
            info = request.json
            robots = URMSystem().get_robots()
            for i in range(1, int(robots[info.get("robot")]["AngleCount"])+1):
                robots["First"]["StandartSpeed"][f"J{i}"] = float(info.get("angles").get(f'J{i}'))
            System().SaveToCache(robots=robots)
            User().update_token()
            Robot_loger(info.get("robot")).info(f"""Was setted robot standart speed: {
                    info.get("angles").get('J1')},{info.get("angles").get('J2')},{info.get("angles").get('J3')},{info.get("angles").get('J4')}""")
            return jsonify({"status": True, "info": "The robot default speed parameter was been seted"}), 200
            
        """ Set program """
        @app.route('/SetProgram', methods=['POST'])
        @access.check_robot_user(user_role="user", loger_module=self.loger_module)
        def Program():
            info = request.json
            robots = URMSystem().get_robots()
            if robots[info.get("robot")]["Emergency"] == True:
                log_message = f"The robot '{info.get('robot')}' is currently in emergency stop"
                Robot_loger(info.get("robot")).error(log_message)
                return jsonify({"status": False, "info": log_message}), 400
            else:
                robots[info.get("robot")]["Program"] = info.get('program')
                robots[info.get("robot")]["ProgramToken"] = secrets.token_hex(16)
                System().SaveToCache(robots=robots)
                User().update_token()
                log_message = "Was setted robot programm"
                Robot_loger(info.get("robot")).info(log_message)
                return jsonify({"status": True, "info": log_message}), 200

        """ Delete program """
        @app.route('/DeleteProgram', methods=['POST'])
        @access.check_robot_user(user_role="user", loger_module=self.loger_module)
        def DeleteProgram():
            info = request.json
            robots = URMSystem().get_robots()
            robots[info.get("robot")]["Program"] = ""
            robots[info.get("robot")]["ProgramToken"] = ""
            System().SaveToCache(robots=robots)
            User().update_token()
            log_message = "Was deleted robot programm"
            Robot_loger(info.get("robot")).info(log_message)
            return jsonify({"status": True, "info": log_message}), 200


        """ Get XYZ from angle robot position """
        @app.route('/angle_to_xyz', methods=['POST'])
        @access.check_robot_user(user_role="user", loger_module=self.loger_module)
        def angle_to_xyz():
            info = request.json
            kinematics:dict = KinematicsManager().get_kinematics()
            if kinematics[info.get("robot")] != "None":
                try:
                    if info.get("positions_data") is None:
                        new_coord = {}
                        modul = kinematics[info.get("robot")]
                        result_forward:dict = modul.Forward(info.get("angles").get("J1"), info.get("angles").get("J2"), info.get("angles").get("J3"), info.get("angles").get("J4"))
                        new_coord["x"] = result_forward.get("x")
                        new_coord["y"] = result_forward.get("y")
                        new_coord["z"] = result_forward.get("z")
                        return jsonify({"status": True, "info": "Angles to cartesian point converter", "data": new_coord}), 200
                    else:
                        angles = ast.literal_eval(info.get("angles_data"))
                        if isinstance(angles, list):
                            points = []
                            for pos in angles:
                                point_coords = {}
                                modul = kinematics[info.get("robot")]
                                # set coords
                                result_forward:dict = modul.Forward(pos[0], pos[1], pos[2], pos[3])
                                new_coord["x"] = result_forward.get("x")
                                new_coord["y"] = result_forward.get("y")
                                new_coord["z"] = result_forward.get("z")
                                points.append(point_coords)
                            return jsonify({"status": True, "info": "(multi) angles to cartesian points converter", "data": points}), 200
                        else:
                            return jsonify({"status": False, "info": "Multi points data is not valid"}), 400
                except:
                    return jsonify({"status": False, "info": "An error has occurred"}), 400
            else:
                return jsonify({"status": False, "info": "This command does not work if you are not using kinematics"}), 400

        """ Get angle from XYZ robot position """
        @app.route('/XYZ_to_angle', methods=['POST'])
        @access.check_robot_user(user_role="user", loger_module=self.loger_module)
        def XYZ_to_angle():
            info = request.json
            robots = URMSystem().get_robots()
            kinematics:dict = KinematicsManager().get_kinematics()
            if kinematics[info.get("robot")] != "None":
                try:
                    if info.get("positions_data") is None:
                        point_angles = {}
                        modul = kinematics[info.get("robot")]
                        result_inverse:dict = modul.Inverse(info.get("position").get("x"), info.get("position").get("y"), info.get("position").get("z"))
                        for j in range(1, int(robots[info.get("robot")]["AngleCount"]) + 1):
                            point_angles[f"J{j}"] = result_inverse.get(f"J{j}")
                        return jsonify({"status": True, "info": "Cartesian point to angles converter", "data": point_angles}), 200
                    else:
                        positions = ast.literal_eval(info.get("positions_data"))
                        if isinstance(positions, list):
                            angles = []
                            for pos in positions:
                                point_angles = {}
                                modul = kinematics[info.get("robot")]
                                result_inverse:dict = modul.Inverse(pos["x"], pos["y"], pos["z"])
                                for j in range(1, int(robots[info.get("robot")]["AngleCount"]) + 1):
                                    point_angles[f"J{j}"] = result_inverse.get(f"J{j}")
                                angles.append(point_angles)
                            return jsonify({"status": True, "info": "(multi) cartesian point to angles converter", "data": angles}), 200
                        else:
                            return jsonify({"status": False, "info": "Multi points data is not valid"}), 400
                except:
                    return jsonify({"status": False, "info": "An error has occurred"}), 400
            else:
                return jsonify({"status": False, "info": "This command does not work if you are not using kinematics"}), 400
            
        """ Set curent robot XYZ position """
        @app.route('/Move_XYZ', methods=['POST'])
        @access.check_robot_user_prog_token(user_role="user")
        def Move_XYZ():
            info = request.json
            robots = URMSystem().get_robots()
            if robots[info.get("robot")]["RobotReady"] == True:
                globals()["is_robot_ready_setted_false"][info.get("robot")] = False
            kinematics:dict = KinematicsManager().get_kinematics()
            if kinematics[info.get("robot")] != "None":
                while True:
                    if robots[info.get("robot")]["Emergency"] == True:
                        log_message = f"The robot '{info.get('robot')}' is currently in emergency stop"
                        Robot_loger(info.get("robot")).error(log_message)
                        return jsonify({"status": False, "info": log_message}), 400
                    else:
                        if not globals()["is_robot_ready_setted_false"][info.get("robot")] or bool(robots[info.get("robot")]["RobotReady"]) == False:
                            continue
                        elif bool(robots[info.get("robot")]["RobotReady"]) == True and globals()["is_robot_ready_setted_false"][info.get("robot")] and\
                        not isinstance(robots[info.get("robot")]["Position"], list):
                            try:
                                if info.get("positions_data") is None:
                                    modul = kinematics[info.get("robot")]
                                    result_inverse:dict = modul.Inverse(info.get("position").get("x"), info.get("position").get("y"), info.get("position").get("z"))
                                    for j in range(1, int(robots[info.get("robot")]["AngleCount"]) + 1):
                                        robots[info.get("robot")]["Position"][f"J{j}"] = result_inverse.get(f"J{j}")
                                        
                                    robots[info.get("robot")]["XYZposition"]["x"] = info.get("position").get("x")
                                    robots[info.get("robot")]["XYZposition"]["y"] = info.get("position").get("y")
                                    robots[info.get("robot")]["XYZposition"]["z"] = info.get("position").get("z")
                                    
                                    Robot_loger(info.get("robot")).info(f"""The robot has been moved to coordinates: X-{
                                        info.get("X")},Y-{info.get("Y")},Z-{info.get("Z")}""")
                                else:
                                    # If getted not one point
                                    new_positions = ast.literal_eval(info.get("positions_data"))
                                    if isinstance(new_positions, list):
                                        angles = []
                                        for pos in new_positions:
                                            modul = kinematics[info.get("robot")]
                                            result_inverse:dict = modul.Inverse(pos.get("x"), pos.get("y"), pos.get("z"))
                                            angles.append(result_inverse)
                                        robots[info.get("robot")]["Position"] = angles
                                    else:
                                        return jsonify({"status": False, "info": "Multi points data is not valid"}), 400
                                    
                                robots[info.get("robot")]["RobotReady"] = False
                                System().SaveToCache(robots=robots)
                                globals()["is_robot_ready_setted_false"][info.get("robot")] = False
                                User().update_token()
                                return jsonify({"status": True, "info": f"Curent robot '{info.get('robot')}' cartesian position was been seted"}), 200
                            except:
                                return jsonify({"status": False, "info": "An error has occurred"}), 400    
            else:
                return jsonify({"status": False, "info": "This command does not work if you are not using kinematics"}), 400

        ''' Set minimal angle of rotation '''
        @app.route('/MinAngles', methods=['POST'])
        @access.check_robot_user_prog(user_role="administrator", loger_module=self.loger_module)
        def MinAngles():
            info = request.json
            robots = URMSystem().get_robots()
            if robots[info.get("robot")]["Emergency"] == True:
                log_message = f"The robot '{info.get('robot')}' is currently in emergency stop"
                Robot_loger(info.get("robot")).error(log_message)
                return jsonify({"status": False, "info": log_message}), 400
            else:
                for i in range(1, int(robots[info.get("robot")]["AngleCount"])+1):
                    robots[info.get("robot")]["MinAngles"][f"J{i}"] = float(info.get("angles").get(f'J{i}'))
                System().SaveToCache(robots=robots)
                User().update_token()
                Robot_loger(info.get("robot")).info(f"""Was setted robot minimal angles: {
                    info.get("angles").get('J1')},{info.get("angles").get('J2')},{info.get("angles").get('J3')},{info.get("angles").get('J4')}""")
                return jsonify({"status": True, "info": f"Robot '{info.get('robot')}' minimal angles data was been seted"}), 200
                

        ''' Set maximum angle of rotation '''
        @app.route('/MaxAngles', methods=['POST'])
        @access.check_robot_user_prog(user_role="administrator", loger_module=self.loger_module)
        def MaxAngles():
            info = request.json
            robots = URMSystem().get_robots()
            if robots[info.get("robot")]["Emergency"] == True:
                log_message = f"The robot '{info.get('robot')}' is currently in emergency stop"
                Robot_loger(info.get("robot")).error(log_message)
                return jsonify({"status": False, "info": log_message}), 400
            else:
                for i in range(1, int(robots[info.get("robot")]["AngleCount"])+1):
                    robots[info.get("robot")]["MaxAngles"][f"J{i}"] = float(info.get("angles").get(f'J{i}'))
                System().SaveToCache(robots=robots)
                User().update_token()
                Robot_loger(info.get("robot")).info(f"""Was setted robot maximal angles: {
                    info.get("angles").get('J1')},{info.get("angles").get('J2')},{info.get("angles").get('J3')},{info.get("angles").get('J4')}""")
                return jsonify({"status": True, "info": f"Robot '{info.get('robot')}' maximal angles data was been seted"}), 200

        ''' Set program is running '''
        @app.route('/SetProgramRun', methods=['POST'])
        @access.check_user(user_role="System", loger_module=self.loger_module)
        def SetProgramRun():
            info = request.json
            robots = URMSystem().get_robots()
            robots[info.get("robot")]["ProgramRunning"] = info.get("state")
            System().SaveToCache(robots=robots)
            User().update_token()
            return jsonify({"status": True, "info": f"Robot '{info.get('robot')}' ProgramRun parameter was been seted"}), 200
        
        return app