import time
import os

# TODO: add select date for get log

class Loger():
    
    def __init__(self) -> None:
        current_time = time.localtime()
        file_name = f"{current_time[2]} {current_time[1]} {current_time[0]}"
        file_path = f'Logs/{file_name}.log'
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                text = file.read()
            if text == "":
                with open(file_path, "a") as file:
                    file.write(f"[{self.__get_time()}] [INFO] [loger] System logging submodule started")
            else:
                with open(file_path, "a") as file:
                    file.write(f"\n[{self.__get_time()}] [INFO] [loger] System logging submodule started")
      
        else:
            with open(f'Logs/{file_name}.log', "a") as file:
                file.write(f"[{self.__get_time()}] [INFO] [loger] System logging submodule started")
            
    
    @staticmethod
    def __get_time():
        current_time = time.localtime()
        return f"{current_time[3]}:{current_time[4]}:{current_time[5]}"
    
    def debug(self, module:str, msg:str) -> None:
        current_time = time.localtime()
        file_name = f"{current_time[2]} {current_time[1]} {current_time[0]}"
        with open(f'Logs/{file_name}.log', 'a') as file:
            file.write(f"\n[{self.__get_time()}] [DEBUG] [{module}] {msg}")
        
    def info(self, module:str, msg:str) -> None:
        current_time = time.localtime()
        file_name = f"{current_time[2]} {current_time[1]} {current_time[0]}"
        with open(f'Logs/{file_name}.log', 'a') as file:
            file.write(f"\n[{self.__get_time()}] [INFO] [{module}] {msg}")
    
    def warning(self, module:str, msg:str) -> None:
        current_time = time.localtime()
        file_name = f"{current_time[2]} {current_time[1]} {current_time[0]}"
        with open(f'Logs/{file_name}.log', 'a') as file:
            file.write(f"\n[{self.__get_time()}] [WARNING] [{module}] {msg}")
    
    def error(self, module:str, msg:str) -> None:
        current_time = time.localtime()
        file_name = f"{current_time[2]} {current_time[1]} {current_time[0]}"
        with open(f'Logs/{file_name}.log', 'a') as file:
            file.write(f"\n[{self.__get_time()}] [ERROR] [{module}] {msg}")
            
    def get_logs(self) -> list:
        current_time = time.localtime()
        file_name = f"{current_time[2]} {current_time[1]} {current_time[0]}"
        with open(f'Logs/{file_name}.log', 'r') as file:
            return file.readlines()

class Robot_loger():
    def __init__(self, robot_name:str) -> None:
        self.__name = robot_name
        current_time = time.localtime()
        file_name = f"{current_time[2]} {current_time[1]} {current_time[0]}"
        try:
            os.mkdir(f'Logs/{robot_name}')
        except:
            pass
        file_path = f'Logs/{robot_name}/{file_name}.log'
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                text = file.read()
            if text == "":
                with open(file_path, "a") as file:
                    file.write(f"[{self.__get_time()}] [INFO] Robot logging submodule started")
            else:
                with open(file_path, "a") as file:
                    file.write(f"\n[{self.__get_time()}] [INFO] Robot logging submodule started")
      
        else:
            with open(file_path, "a") as file:
                file.write(f"[{self.__get_time()}] [INFO] Robot logging submodule started")
            
    
    @staticmethod
    def __get_time():
        current_time = time.localtime()
        return f"{current_time[3]}:{current_time[4]}:{current_time[5]}"
    
    def debug(self, msg:str) -> None:
        current_time = time.localtime()
        file_name = f"{current_time[2]} {current_time[1]} {current_time[0]}"
        file_path = f'Logs/{self.__name}/{file_name}.log'
        with open(file_path, 'a') as file:
            file.write(f"\n[{self.__get_time()}] [DEBUG] {msg}")
        
    def info(self, msg:str) -> None:
        current_time = time.localtime()
        file_name = f"{current_time[2]} {current_time[1]} {current_time[0]}"
        file_path = f'Logs/{self.__name}/{file_name}.log'
        with open(file_path, 'a') as file:
            file.write(f"\n[{self.__get_time()}] [INFO] {msg}")
    
    def warning(self, msg:str) -> None:
        current_time = time.localtime()
        file_name = f"{current_time[2]} {current_time[1]} {current_time[0]}"
        file_path = f'Logs/{self.__name}/{file_name}.log'
        with open(file_path, 'a') as file:
            file.write(f"\n[{self.__get_time()}] [WARNING] {msg}")
    
    def error(self, msg:str) -> None:
        current_time = time.localtime()
        file_name = f"{current_time[2]} {current_time[1]} {current_time[0]}"
        file_path = f'Logs/{self.__name}/{file_name}.log'
        with open(file_path, 'a') as file:
            file.write(f"\n[{self.__get_time()}] [ERROR] {msg}")
            
    def get_logs(self) -> list:
        current_time = time.localtime()
        file_name = f"{current_time[2]} {current_time[1]} {current_time[0]}"
        file_path = f'Logs/{self.__name}/{file_name}.log'
        with open(file_path, 'r') as file:
            return file.readlines()
