import json
import ast

import requests
import numpy as np
from scipy.interpolate import CubicSpline

import tools

external_token = ""
robot_name = ""
class tokenizer():

    def __init__(self, token) -> None:
        self.token = token

    def set_token(self) -> None:
        global external_token
        external_token = self.token

class Robot(tools.Tools):
    
    def __init__(self, host:str, port:int, code:str, *token:str) -> None:
        self.__host = host
        self.__name = robot_name
        self.__port = port
        self.__code = code
        self.__token = token if external_token == "" else external_token
        super().__init__(host=self.__host, port=self.__port, token=self.__token)
    
    def check_emergency(self) -> bool:
        url = f"https://{self.__host}:{str(self.__port)}/GetRobotEmergency"
        data = {
            "Robot": self.__name,
            "token": self.__token
        }
        response = requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
        if  bool(response):
            return True
        else:
            return False

    def ptp(self, angles:list) -> str:
        # Set position
        if self.check_emergency():
            url = f"https://{self.__host}:{str(self.__port)}/CurentPosition"
            data = {
                "Robot": self.__name,
                "token": self.__token,
                "Code" : self.__code
                }
            for i in range(1, len(angles)+1):
                data[f"J{i}"] = angles[i-1]
            responce = requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
            # Set motor speed
            url = f"https://{self.__host}:{str(self.__port)}/CurentSpeed"
            data = {
                "Robot": self.__name,
                "token": self.__token,
                "Code" : self.__code
                }
            for i in range(1, len(angles)+1):
                data[f"J{i}"] = 1
            requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False)))
            return responce
        else:
            return "The robot is currently in emergency stop"
    
    
    def move_xyz(self, position:list) -> str:
        if self.check_emergency():
            url = f"https://{self.__host}:{str(self.__port)}/Move_XYZ"
            data = {
                "Robot": self.__name,
                "X": position[0],
                "Y": position[1],
                "Z": position[2],
                "token": self.__token,
                "Code" : self.__code
                }
            return requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
        else:
            return "The robot is currently in emergency stop"

    def xyz_to_angle(self, position:list) -> str:
        url = f"https://{self.__host}:{str(self.__port)}/XYZ_to_angle"
        data = {
            "Robot": self.__name,
            "X": position[0],
            "Y": position[1],
            "Z": position[2],
            "token": self.__token,
            "Code" : self.__code
            }
        responce = requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
        angles_dict = ast.literal_eval(responce)
        return [
            angles_dict["J1"],
            angles_dict["J2"],
            angles_dict["J3"],
            angles_dict["J4"]
        ]
        
    def angle_to_xyz(self, angles:list) -> list:
        url = f"https://{self.__host}:{str(self.__port)}/angle_to_xyz"
        data = {
            "Robot": self.__name,
            "J1": angles[0],
            "J2": angles[1],
            "J3": angles[2],
            "J4": angles[3],
            "token": self.__token,
            "Code" : self.__code
            }
        responce = requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
        coord_dict = ast.literal_eval(responce)
        return [
            coord_dict["X"],
            coord_dict["Y"],
            coord_dict["Z"]
        ]
        
    @staticmethod
    def calculate_speed(start_angles, end_angles, steps):
    # Проверка на совпадение размеров списков
        if len(start_angles) != len(end_angles):
            raise ValueError("Списки начальных и конечных углов должны иметь одинаковую длину")
        
        # Инициализация списка скоростей
        speeds = []
        
        # Цикл по элементам списков углов
        for i in range(len(start_angles)):
            # Вычисление разницы между начальным и конечным углом для каждого сервомотора
            angle_diff = end_angles[i] - start_angles[i]
            
            # Вычисление скорости вращения для каждого сервомотора
            speed = angle_diff / steps  # steps - количество шагов
            
            # Добавление скорости вращения в список
            speeds.append(abs(speed))
        
        return speeds
    
    def lin(self, angles:list, step_count:int=100) -> None:
        if self.check_emergency():
        # Lin robot moving
            url = f"https://{self.__host}:{str(self.__port)}/GetCurentPosition"
            data = {
                "Robot": self.__name,
                "token": self.__token
                }
            resp = requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
            speed_angles = json.loads(resp.replace("'", '"'))
            start_angles = [speed_angles["J1"],
                            speed_angles["J2"],
                            speed_angles["J3"],
                            speed_angles["J4"],]
            
            end_angles = angles
            steps = step_count
            # Вычисление скоростей вращения для перемещения от начальной позиции к конечной
            speeds = self.calculate_speed(start_angles, end_angles, steps)

            # send current position
            url = f"https://{self.__host}:{str(self.__port)}/CurentPosition"
            data = {
                "Robot": self.__name,
                "token": self.__token,
                "Code" : self.__code
                }
            for i in range(1, len(angles)+1):
                data[f"J{i}"] = angles[i-1]
            requests.post(url,  verify=True ,data=json.loads(json.dumps(data, ensure_ascii=False)))
            
            # send current speed
            url = f"https://{self.__host}:{str(self.__port)}/CurentSpeed"
            data = {
                "Robot": self.__name,
                "token": self.__token,
                "Code" : self.__code
                }
            for i in range(1, len(angles)+1):
                data[f"J{i}"] = speeds[i-1]
            requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False)))
            return "True"
        else:
            return "The robot is currently in emergency stop"

    @staticmethod
    def __interpolate_points(start_point, intermediate_point, end_point, num_points):
        # Создание массивов x, y и z координат для начальной, конечной и вспомогательной точек
        x = np.array([start_point[0], intermediate_point[0], end_point[0]])
        y = np.array([start_point[1], intermediate_point[1], end_point[1]])
        z = np.array([start_point[2], intermediate_point[2], end_point[2]])

        # Интерполяция координат по кубическим сплайнам
        t = [0, 0.5, 1]  # Параметры времени для начальной, вспомогательной и конечной точек
        cs = CubicSpline(t, np.vstack([x, y, z]).T)
        # Генерация равномерных значений параметра времени от 0 до 1
        t_interp = np.linspace(0, 1, num=num_points)

        # Вычисление интерполированных координат x, y и z
        x_interp, y_interp, z_interp = cs(t_interp).T

        # Возвращение массива интерполированных точек
        interpolated_points = np.column_stack((x_interp, y_interp, z_interp))
        return interpolated_points

    def circ(self, points:list[list[float]], count_points:int, lin_step_count:int=100) -> bool:
        if self.check_emergency():
            coords = self.__interpolate_points(
                points[0],
                points[1],
                points[2],
                count_points)
            points = []
            for line in coords:
                points.append(self.xyz_to_angle(line))
            for point in points:
                self.lin(point, lin_step_count)
            return True
        else:
            return "The robot is currently in emergency stop"

    def get_log(self) -> str:
        url = f"https://{self.__host}:{str(self.__port)}/URLog"
        data = {
            "Robot": self.__name,
            "token": self.__token
            }
        return requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text

    def get_last_log(self) -> str:
        url = f"https://{self.__host}:{str(self.__port)}/URLog"
        data = {
            "Robot": self.__name,
            "token": self.__token
            }
        return requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text.split("\n")[-1]
    
    def debug(self, text:str) -> str:
        url = f"https://{self.__host}:{str(self.__port)}/URLogs"
        data = {
            "Robot": self.__name,
            "Type": "DEBUG",
            "Text": text
            }
        return requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text

    def set_program(self , program:str) -> str:
        if self.check_emergency():
            url = f"https://{self.__host}:{str(self.__port)}/SetProgram"
            data = {
                "Robot": self.__name,
                "Program": program.encode().hex(),
                "token": self.__token,
                "Code" : self.__code
                }
            return requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
        else:
            return "The robot is currently in emergency stop"
        
    def delete_program(self) -> str:
        url = f"https://{self.__host}:{str(self.__port)}/DeleteProgram"
        data = {
            "Robot": self.__name,
            "token": self.__token,
            "Code" : self.__code
            }
        return requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text

    def set_robot_ready(self) -> str:
        if self.check_emergency():
            url = f"https://{self.__host}:{str(self.__port)}/SetRobotReady"
            data = {
                "Robot": self.__name,
                "token": self.__token
                }
            return requests.post(url, verify=True, data=json.loads(json.dumps(data, ensure_ascii=False))).text
        else:
            return "The robot is currently in emergency stop"