import secrets
import time

from configuration.cache.file_cache import save_to_cache
from utils.logger import Logger
from utils.user_updater import update_token
from utils.validator import RobotChecker
from services.multi_robots_manager import MultiRobotsManager
from services.kinematics_manager import KinematicsManager
from services.tools_manager import ToolsManager
from services.bases_manager import BasesManager

is_robot_ready_setted_false = {}

class RobotManager:
    is_robot_ready_setted_false = is_robot_ready_setted_false
    logger = Logger()
    checker = RobotChecker()
    robots_manager = MultiRobotsManager()
    kinematic_manager = KinematicsManager()
    tools_manager = ToolsManager()
    bases_manager = BasesManager()
    
    def __init__(self, robots:dict=None) -> None:
        self.logger_module = "URManager"
        if robots is not None:
            for robot_name in robots.keys():
                self.is_robot_ready_setted_false[robot_name] = True
      
    def add_new_robot_ready(self, robot_name:str) -> None:
        self.is_robot_ready_setted_false[robot_name] = True
    
    def remove_new_robot_ready(self, robot_name:str) -> None:
        if self.is_robot_ready_setted_false.get(robot_name) is not None:
            del self.is_robot_ready_setted_false[robot_name]
    
    """ Get curent robot position """
    def get_position(self, robot_name:str) -> tuple:
        time.sleep(0.2)
        robots = self.robots_manager.get_robots()
        return {"status": True, "info": f"Curent robot '{robot_name}' angles position", "data": robots[robot_name]["Position"]}, 200
    
    """ Get robot position id """
    def get_position_id(self, robot_name:str) -> tuple:
        robots = self.robots_manager.get_robots()
        return {"status": True, "info": f"Curent robot '{robot_name}' position id", "data": robots[robot_name]["PositionID"]}, 200
    
    """ Get curent robot speed """
    def get_speed(self, robot_name:str) -> tuple:
        time.sleep(0.2)
        robots = self.robots_manager.get_robots()
        return {"status": True, "info": f"Curent robot '{robot_name}' angles speed", "data": robots[robot_name]["MotorsSpeed"]}, 200
    
    """ Get curent robot position """
    def get_catesian_position(self, robot_name:str) -> tuple:
        robots = self.robots_manager.get_robots()
        return {"status": True, "info": f"Curent robot '{robot_name}' cartesian position", "data": robots[robot_name]["XYZposition"]}, 200
    
    """ Get robot angles count """
    def get_angles_count(self, robot_name:str) -> tuple:
        robots = self.robots_manager.get_robots()
        return {"status": True, "info": f"Curent robot '{robot_name}' angles count", "data": robots[robot_name]["AngleCount"]}, 200
        
    """ Set curent robot motors position """
    def set_motors_position(self, robot_name:str, angles:dict[float]) -> tuple:
        robots = self.robots_manager.get_robots()
        kinematics:dict = self.kinematic_manager.get_kinematics()
        for i in range(1, int(robots[robot_name]["AngleCount"])+1):
            robots[robot_name]["MotorsPosition"][f"J{i}"] = angles.get(f'J{i}')
            if robots[robot_name]["Emergency"] == True:
                robots[robot_name]["Position"][f"J{i}"] = angles.get(f'J{i}')
        
        if robots[robot_name]["Kinematic"] != "None":
            modul = kinematics[robot_name]
            result_forward:dict = modul.Forward(angles)
            pos = robots[robot_name]["XYZposition"]
            pos["x"] = result_forward.get("x")
            pos["y"] = result_forward.get("y")
            pos["z"] = result_forward.get("z")      
            pos["a"] = result_forward.get("a")      
            pos["b"] = result_forward.get("b")      
            pos["c"] = result_forward.get("c")      
        
        save_to_cache(robots=robots)
        return {"status": True, "info": f"Motors position for robot '{robot_name}' has been setted"}, 200
        
    """ Get robot ready parameter """
    def get_ready_state(self, robot_name:str) -> tuple:
        robots = self.robots_manager.get_robots()
        return {"status": True, "info": f"Curent robot '{robot_name}' RobotReady parameter", "data": robots[robot_name]["RobotReady"]}, 200
    
    ''' Get emergency stop '''
    def get_emergency_state(self, robot_name:str) -> tuple:
        robots = self.robots_manager.get_robots()
        return {"status": True, "info": f"Curent robot '{robot_name}' Emergency parameter", "data": robots[robot_name]["Emergency"]}, 200
        
    """ Set robot ready parameter """
    def set_ready_state(self, robot_name:str, state:bool) -> tuple:
        robots = self.robots_manager.get_robots()
        if state == False:
            self.is_robot_ready_setted_false[robot_name] = True
            robots[robot_name]["RobotReady"] = state
            
        if state == True:
            if not self.is_robot_ready_setted_false[robot_name]: 
                return {"status": False, "info": "The RobotReady parameter was not been seted"}, 400
            else:
                if not isinstance(robots[robot_name]["Position"], list):
                    robots[robot_name]["RobotReady"] = state
                else:
                    return {"status": False, "info": "The RobotReady parameter was not been seted"}, 400
        save_to_cache(robots=robots)
        update_token()
        return {"status": True, "info": "The RobotReady parameter was been seted"}, 200
    
    """ Set robot position id """
    # TODO: determine access to the function (who has access)
    def set_position_id(self, robot_name:str, position_id:str) -> tuple:
        robots = self.robots_manager.get_robots()
        robots[robot_name]["PositionID"] = position_id
        
        save_to_cache(robots=robots)
        update_token()
        return {"status": True, "info": "The PositionID parameter was been seted"}, 200
        
    ''' Activate and deativate emergency stop '''
    def set_emergency_state(self, robot_name:str, state:bool) -> tuple:
        robots = self.robots_manager.get_robots()
        kinematics:dict = self.kinematic_manager.get_kinematics()
        robots[robot_name]["Emergency"] = True if state == True else False
        if robots[robot_name]["Emergency"] == True:
            robots[robot_name]["Position"] = robots[robot_name]["MotorsPosition"].copy()
            robots[robot_name]["MotorsSpeed"] = robots[robot_name]["StandartSpeed"].copy()
            robots[robot_name]["RobotReady"] = False
            robots[robot_name]["Program"] = ""
            
        if robots[robot_name]["Kinematic"] != "None":
            modul = kinematics[robot_name]
            pos = robots[robot_name]["Position"]
            result_forward:dict = modul.Forward(pos)
            pos = robots[robot_name]["XYZposition"]
            pos["x"] = result_forward.get("x")
            pos["y"] = result_forward.get("y")
            pos["z"] = result_forward.get("z")      
            pos["a"] = result_forward.get("a")      
            pos["b"] = result_forward.get("b")      
            pos["c"] = result_forward.get("c") 
        
        save_to_cache(robots=robots)
        update_token()
        Logger(robot_name=robot_name).info(f"Emergency stop button activated")
        return {"status": True, "info": "The Emergency parameter was been seted"}, 200

    """ Curent robot position"""
    def set_position(self, robot_name:str, angles:dict=None, angles_data:list=None) -> tuple:
        robots = self.robots_manager.get_robots()
        if robots[robot_name]["RobotReady"] == True:
            self.is_robot_ready_setted_false[robot_name] = False
        kinematics:dict = self.kinematic_manager.get_kinematics()
        while True:
            if robots[robot_name]["Emergency"] == True:
                log_message = f"The robot '{robot_name}' is currently in emergency stop"
                Logger(robot_name=robot_name).error(log_message)
                return {"status": False, "info": log_message}, 400
            else:
                if not self.is_robot_ready_setted_false[robot_name] or bool(robots[robot_name]["RobotReady"]) == False:
                    continue
                elif robots[robot_name]["RobotReady"] == True and self.is_robot_ready_setted_false[robot_name] and\
                    not isinstance(robots[robot_name]["Position"], list):
                        if angles_data is None:
                            if RobotChecker().check_angles(robot_name, angles, robots) == False:
                                log_message = "Angles values ​​are not correct"
                                Logger(robot_name=robot_name).error(log_message)
                                return {"status": False, "info": log_message}, 400
                            else:
                                for i in range(1, int(robots[robot_name]["AngleCount"])+1):
                                    robots[robot_name]["Position"][f"J{i}"] = angles.get(f'J{i}')
                                
                                if robots[robot_name]["Kinematic"] != "None":
                                    modul = kinematics[robot_name]
                                    result_forward:dict = modul.Forward(angles)
                                    pos = robots[robot_name]["XYZposition"]
                                    pos["x"] = result_forward.get("x")
                                    pos["y"] = result_forward.get("y")
                                    pos["z"] = result_forward.get("z")      
                                    pos["a"] = result_forward.get("a")      
                                    pos["b"] = result_forward.get("b")      
                                    pos["c"] = result_forward.get("c") 
                                    
                                Logger(robot_name=robot_name).info(f"Was setted robot current position: {angles}")
                        else:
                            # If getted not one point
                            if isinstance(angles_data, list):
                                robots[robot_name]["Position"] = angles_data
                            else:
                                return {"status": False, "info": "Multi points data is not valid"}, 400

                        robots[robot_name]["RobotReady"] = False
                        save_to_cache(robots=robots)
                        self.is_robot_ready_setted_false[robot_name] = False
                        update_token()
                        return {"status": True, "info": f"Curent robot '{robot_name}' position was been seted"}, 200
                        
    """ Remove curent robot point position """
    def remove_curent_point_position(self, robot_name:str) -> tuple:
        robots = self.robots_manager.get_robots()
        if isinstance(robots[robot_name]["Position"], list):
            if len(robots[robot_name]["Position"]) > 2:
                robots[robot_name]["Position"] = robots[robot_name]["Position"][1::]
            else:
                robots[robot_name]["Position"] = robots[robot_name]["Position"][-1]
            save_to_cache(robots=robots)
            update_token()
            return {"status": True, "info": "Curent robot point position was been removed"}, 200
        elif isinstance(robots[robot_name]["Position"], dict):
            return {"status": False, "info": "Curent robot point position is not multi point"}, 400
        
    """ Remove all robot point positions """
    def remove_all_point_position(self, robot_name:str) -> tuple:
        robots = self.robots_manager.get_robots()
        if isinstance(robots[robot_name]["Position"], list):
            robots[robot_name]["Position"] = robots[robot_name]["Position"][-1]
            save_to_cache(robots=robots)
            update_token()
            return {"status": True, "info": "All robot points from multi point position was been removed"}, 200
        elif isinstance(robots[robot_name]["Position"], dict):
            return {"status": False, "info": "Curent robot point position is not multi point"}, 400

    """ Curent home position"""
    def set_home_position(self, robot_name:str, angles:dict) -> tuple:
        robots = self.robots_manager.get_robots()
        if RobotChecker().check_angles(robot_name, angles, robots) == False:
            log_message = "Angles values ​​are not correct"
            Logger(robot_name=robot_name).error(log_message)
            return {"status": False, "info": log_message}, 400
        else:
            for i in range(1, int(robots[robot_name]["AngleCount"])+1):
                robots[robot_name]["HomePosition"][f"J{i}"] = float(angles.get(f'J{i}'))
            save_to_cache(robots=robots)
            update_token()
            
            Logger(robot_name=robot_name).info(f"""Was setted robot home position: {angles}""")
            return {"status": True, "info": f"Was setted robot '{robot_name}' home position"}, 200

    """ Curent robot speed """
    def set_speed(self, robot_name:str, angles:dict=None, angles_data:list=None) -> tuple:
        robots = self.robots_manager.get_robots()
        if robots[robot_name]["Emergency"] == True:
            log_message = f"The robot is currently in emergency stop"
            Logger(robot_name=robot_name).error(log_message)
            return {"status": False, "info": log_message}, 400
        else:
            if angles_data is None:
                for i in range(1, int(robots[robot_name]["AngleCount"])+1):
                    robots[robot_name]["MotorsSpeed"][f"J{i}"] = float(angles.get(f'J{i}'))
                
                Logger(robot_name=robot_name).info(f"""Was setted robot current speed: {angles}""")
            else:
                # If getted not one point
                new_pos = angles_data
                if isinstance(new_pos, list):
                    robots[robot_name]["MotorsSpeed"] = new_pos
                else:
                    return {"status": False, "info": "Multi points agle speed data is not valid"}, 400
                
            save_to_cache(robots=robots)
            update_token()
            return {"status": True, "info": "The robot speed parameter was been seted"}, 200
                
    """ Remove curent robot point speed """
    def remove_curent_point_speed(self, robot_name:str) -> tuple:
        robots = self.robots_manager.get_robots()
        if isinstance(robots[robot_name]["MotorsSpeed"], list):
            if len(robots[robot_name]["MotorsSpeed"]) > 2:
                robots[robot_name]["MotorsSpeed"] = robots[robot_name]["MotorsSpeed"][1::]
            else:
                robots[robot_name]["MotorsSpeed"] = robots[robot_name]["MotorsSpeed"][-1]
            save_to_cache(robots=robots)
            update_token()
            return {"status": True, "info": "Curent robot point speed was been removed"}, 200
        elif isinstance(robots[robot_name]["MotorsSpeed"], dict):
            return {"status": False, "info": "Curent robot point speed is not multi point"}, 400
        
    """ Remove all robot point speeds """
    def remove_all_point_speed(self, robot_name:str) -> tuple:
        robots = self.robots_manager.get_robots()
        if isinstance(robots[robot_name]["MotorsSpeed"], list):
            robots[robot_name]["MotorsSpeed"] = robots[robot_name]["MotorsSpeed"][-1]
            save_to_cache(robots=robots)
            update_token()
            return {"status": True, "info": "All robot points from multi point speed was been removed"}, 200
        elif isinstance(robots[robot_name]["Position"], dict):
            return {"status": False, "info": "Curent robot point speed is not multi point"}, 400

    """ Standart robot speed"""
    def set_standart_speed(self, robot_name:str, angles:dict[float]) -> tuple:
        robots = self.robots_manager.get_robots()
        for i in range(1, int(robots[robot_name]["AngleCount"])+1):
            robots["First"]["StandartSpeed"][f"J{i}"] = float(angles.get(f'J{i}'))
        save_to_cache(robots=robots)
        update_token()
        Logger(robot_name=robot_name).info(f"""Was setted robot standart speed: {angles}""")
        return {"status": True, "info": "The robot default speed parameter was been seted"}, 200
        
    """ Set program """
    def set_program(self, robot_name:str, program:str) -> tuple:
        robots = self.robots_manager.get_robots()
        if robots[robot_name]["Emergency"] == True:
            log_message = f"The robot '{robot_name}' is currently in emergency stop"
            Logger(robot_name=robot_name).error(log_message)
            return {"status": False, "info": log_message}, 400
        else:
            robots[robot_name]["Program"] = program
            robots[robot_name]["ProgramToken"] = secrets.token_hex(16)
            robots[robot_name]["PositionID"] = ""
            save_to_cache(robots=robots)
            update_token()
            log_message = "Was setted robot programm"
            Logger(robot_name=robot_name).info(log_message)
            return {"status": True, "info": log_message}, 200

    """ Delete program """
    def delete_program(self, robot_name:str) -> tuple:
        robots = self.robots_manager.get_robots()
        robots[robot_name]["Program"] = ""
        robots[robot_name]["ProgramToken"] = ""
        save_to_cache(robots=robots)
        update_token()
        log_message = "Was deleted robot programm"
        Logger(robot_name=robot_name).info(log_message)
        return {"status": True, "info": log_message}, 200


    """ Get XYZ from angle robot position """
    def angles_to_cartesian(self, robot_name:str, angles:dict=None, angles_data:list=None) -> tuple:
        robots:dict = self.robots_manager.get_robots()
        kinematics:dict = self.kinematic_manager.get_kinematics()
        if kinematics[robot_name] != "None":
            try:
                if angles_data is None:
                    point_coords = {}
                    modul = kinematics[robot_name]
                    result_forward:dict = modul.Forward(angles)
                    point_coords["x"] = result_forward.get("x")
                    point_coords["y"] = result_forward.get("y")
                    point_coords["z"] = result_forward.get("z")      
                    point_coords["a"] = result_forward.get("a")      
                    point_coords["b"] = result_forward.get("b")      
                    point_coords["c"] = result_forward.get("c") 
                    return {"status": True, "info": "Angles to cartesian point converter", "data": point_coords}, 200
                else:
                    if isinstance(angles_data, list):
                        points = []
                        for angles in angles_data:
                            point_coords = {}
                            modul = kinematics[robot_name]
                            # set coords
                            angles_count = robots[robot_name]["AngleCount"]
                            position_angles = {f"J{i+1}": angles[i] for i in range(angles_count)}
                            result_forward:dict = modul.Forward(position_angles)
                            point_coords["x"] = result_forward.get("x")
                            point_coords["y"] = result_forward.get("y")
                            point_coords["z"] = result_forward.get("z")
                            point_coords["a"] = result_forward.get("a")
                            point_coords["b"] = result_forward.get("b")
                            point_coords["c"] = result_forward.get("c")
                            points.append(point_coords)
                        return {"status": True, "info": "(multi) angles to cartesian points converter", "data": points}, 200
                    else:
                        return {"status": False, "info": "Multi points data is not valid"}, 400
            except:
                return {"status": False, "info": "An error has occurred"}, 400
        else:
            return {"status": False, "info": "This command does not work if you are not using kinematics"}, 400

    """ Get angle from XYZ robot position """
    def cartesian_to_angles(self, robot_name:str, coordinate_system:str, position:dict=None, positions_data:list=None) -> tuple:
        robots = self.robots_manager.get_robots()
        kinematics:dict = self.kinematic_manager.get_kinematics()
        if kinematics[robot_name] != "None":
            # try:
                if positions_data is None:
                    point_angles = {}
                    modul = kinematics[robot_name]
                    result_inverse:dict = modul.Inverse(robot_name, position, coordinate_system)
                    for j in range(1, int(robots[robot_name]["AngleCount"]) + 1):
                        point_angles[f"J{j}"] = result_inverse.get(f"J{j}")
                    return {"status": True, "info": "Cartesian point to angles converter", "data": point_angles}, 200
                else:
                    if isinstance(positions_data, list):
                        angles = []
                        for pos in positions_data:
                            point_angles = {}
                            modul = kinematics[robot_name]
                            position = {"x": pos[0], "y": pos[1], "z": pos[2],
                                        "a": pos[3], "b": pos[4], "c": pos[5]}                                
                            result_inverse:dict = modul.Inverse(robot_name, position, coordinate_system)
                            for j in range(1, int(robots[robot_name]["AngleCount"]) + 1):
                                point_angles[f"J{j}"] = result_inverse.get(f"J{j}")
                            angles.append(point_angles)
                        return {"status": True, "info": "(multi) cartesian point to angles converter", "data": angles}, 200
                    else:
                        return {"status": False, "info": "Multi points data is not valid"}, 400
            # except:
            #     return jsonify({"status": False, "info": "An error has occurred"}), 400
        else:
            return {"status": False, "info": "This command does not work if you are not using kinematics"}, 400
        
    """ Set curent robot XYZ position """
    def set_cartesian_position(self, robot_name:str, coordinate_system:str, position:dict=None, positions_data:list=None) -> tuple:
        robots = self.robots_manager.get_robots()
        if robots[robot_name]["RobotReady"] == True:
            self.is_robot_ready_setted_false[robot_name] = False
        kinematics:dict = self.kinematic_manager.get_kinematics()
        if kinematics[robot_name] != "None":
            while True:
                if robots[robot_name]["Emergency"] == True:
                    log_message = f"The robot '{robot_name}' is currently in emergency stop"
                    Logger(robot_name=robot_name).error(log_message)
                    return {"status": False, "info": log_message}, 400
                else:
                    if not self.is_robot_ready_setted_false[robot_name] or bool(robots[robot_name]["RobotReady"]) == False:
                        continue
                    elif bool(robots[robot_name]["RobotReady"]) == True and self.is_robot_ready_setted_false[robot_name] and\
                    not isinstance(robots[robot_name]["Position"], list):
                        try:
                            if positions_data is None:
                                modul = kinematics[robot_name]
                                result_inverse:dict = modul.Inverse(robot_name, position, coordinate_system)
                                for j in range(1, int(robots[robot_name]["AngleCount"]) + 1):
                                    robots[robot_name]["Position"][f"J{j}"] = result_inverse.get(f"J{j}")
                                    
                                pos = robots[robot_name]["XYZposition"]
                                pos["x"] = position.get("x")
                                pos["y"] = position.get("y")
                                pos["z"] = position.get("z")
                                pos["a"] = position.get("a")
                                pos["b"] = position.get("b")
                                pos["c"] = position.get("c")
                                
                                Logger(robot_name=robot_name).info(f"""The robot has been moved to coordinates: {position}""")
                            else:
                                # If getted not one point
                                if isinstance(positions_data, list):
                                    angles = []
                                    for position in positions_data:
                                        modul = kinematics[robot_name]
                                        result_inverse:dict = modul.Inverse(robot_name, position, coordinate_system)
                                        angles.append(result_inverse)
                                    robots[robot_name]["Position"] = angles
                                else:
                                    return {"status": False, "info": "Multi points data is not valid"}, 400
                                
                            robots[robot_name]["RobotReady"] = False
                            save_to_cache(robots=robots)
                            self.is_robot_ready_setted_false[robot_name] = False
                            update_token()
                            return {"status": True, "info": f"Curent robot '{robot_name}' cartesian position was been seted"}, 200
                        except:
                            return {"status": False, "info": "An error has occurred"}, 400    
        else:
            return {"status": False, "info": "This command does not work if you are not using kinematics"}, 400

    ''' Set minimal angle of rotation '''
    def set_min_angles(self, robot_name:str, angles:dict[float]) -> tuple:
        robots = self.robots_manager.get_robots()
        if robots[robot_name]["Emergency"] == True:
            log_message = f"The robot '{robot_name}' is currently in emergency stop"
            Logger(robot_name=robot_name).error(log_message)
            return {"status": False, "info": log_message}, 400
        else:
            for i in range(1, int(robots[robot_name]["AngleCount"])+1):
                robots[robot_name]["MinAngles"][f"J{i}"] = float(angles.get(f'J{i}'))
            save_to_cache(robots=robots)
            update_token()
            Logger(robot_name=robot_name).info(f"""Was setted robot minimal angles: {angles}""")
            return {"status": True, "info": f"Robot '{robot_name}' minimal angles data was been seted"}, 200

    ''' Set maximum angle of rotation '''
    def set_max_angles(self, robot_name:str, angles:dict[float]) -> tuple:
        robots = self.robots_manager.get_robots()
        if robots[robot_name]["Emergency"] == True:
            log_message = f"The robot '{robot_name}' is currently in emergency stop"
            Logger(robot_name=robot_name).error(log_message)
            return {"status": False, "info": log_message}, 400
        else:
            for i in range(1, int(robots[robot_name]["AngleCount"])+1):
                robots[robot_name]["MaxAngles"][f"J{i}"] = float(angles.get(f'J{i}'))
            save_to_cache(robots=robots)
            update_token()
            Logger(robot_name=robot_name).info(f"""Was setted robot maximal angles: {angles}""")
            return {"status": True, "info": f"Robot '{robot_name}' maximal angles data was been seted"}, 200

    ''' Set program is running '''
    def set_program_run_state(self, robot_name:str, state:bool) -> tuple:
        robots = self.robots_manager.get_robots()
        robots[robot_name]["ProgramRunning"] = state
        save_to_cache(robots=robots)
        update_token()
        return {"status": True, "info": f"Robot '{robot_name}' ProgramRun parameter was been seted"}, 200
    
    # set robot tool
    def set_robot_tool(self, robot_name:str, tool_id:str):
        robots:dict = self.robots_manager.get_robots()
        tools = self.tools_manager.get_tools()
        if tool_id == "":
            if robots[robot_name]["Tool"] == "":
                log_message = f"The robot '{robot_name}' the tool is no longer installed"
                self.logger.info(module=self.logger_module, msg=log_message)
                return {"status": False, "info": log_message}, 200
            else:
                robots[robot_name]["Tool"] = ""
                save_to_cache(robots=robots)
                update_token()
                log_message = f"The empty tool was been setted as tool for robot '{robot_name}'"
                self.logger.info(module=self.logger_module, msg=log_message)
                return {"status": True, "info": log_message}, 200
            
        elif tools.get(tool_id) is not None:
            if tools[tool_id].get("calibrated_vector") is not None:
                if robots.get(robot_name) is not None:
                    robots[robot_name]["Tool"] = tool_id
                    save_to_cache(robots=robots)
                    update_token()
                    log_message = f"The tool '{tool_id}' was been setted as tool for robot '{robot_name}'"
                    self.logger.info(module=self.logger_module, msg=log_message)
                    return {"status": True, "info": log_message}, 200
                else:
                    log_message = f"The robot '{robot_name} not found'"
                    self.logger.error(module=self.logger_module, msg=log_message)
                    return {"status": False, "info": log_message}, 403
            else:
                log_message = f"The tool {tool_id} does not have support for running on a robot"
                self.logger.error(module=self.logger_module, msg=log_message)
                return {"status": False, "info": log_message}, 400
        else:
            log_message = f"The tool was not found"
            self.logger.error(module=self.logger_module, msg=log_message)
            return {"status": False, "info": log_message}, 403
        
    # set robot tool
    def set_robot_base(self, robot_name:str, base_id:str) -> tuple:
        robots:dict = self.robots_manager.get_robots()
        bases = self.bases_manager.get_bases()
        
        if base_id == "":
            if robots[robot_name]["Base"] == "":
                log_message = f"The robot '{robot_name}' the empty base is no longer installed"
                Logger(robot_name=robot_name).info(msg=log_message)
                return {"status": False, "info": log_message}, 200
            else:
                robots[robot_name]["Base"] = ""
                save_to_cache(robots=robots)
                update_token()
                log_message = f"The empty base was been setted as base for robot '{robot_name}"
                self.logger.info(msg=log_message)
                return {"status": True, "info": log_message}, 200
        elif bases.get(base_id) is not None:
            if robots.get(robot_name) is not None:
                robots[robot_name]["Base"] = base_id
                save_to_cache(robots=robots)
                update_token()
                log_message = f"The base '{base_id}' was been setted as base for robot '{robot_name}'"
                self.logger.info(module=self.logger_module, msg=log_message)
                return {"status": True, "info": log_message}, 200
            else:
                log_message = f"The robot '{robot_name} not found'"
                self.logger.error(module=self.logger_module, msg=log_message)
                return {"status": False, "info": log_message}, 403
        else:
            log_message = f"The base was not found"
            self.logger.error(module=self.logger_module, msg=log_message)
            return {"status": False, "info": log_message}, 403