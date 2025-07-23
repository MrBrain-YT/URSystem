import time
import os

logger_is_started = False

class Logger():
    
    def __init__(self, robot_name:str=None) -> None:
        current_time = time.localtime()
        self.robot_name = robot_name
        file_name = f"{current_time[2]}_{current_time[1]}_{current_time[0]}"
        if robot_name is None:
            file_path = f'logs/{file_name}.log'
        else:
            try:
                os.mkdir(f'logs/{robot_name}')
            except:
                pass
            file_path = f'logs/{robot_name}/{file_name}.log'
            
        if not logger_is_started:
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    text = file.read()
                if text == "":
                    with open(file_path, "a") as file:
                        file.write(f"[{self.__get_time()}] [INFO] [logger] System logging module started")
                else:
                    with open(file_path, "a") as file:
                        file.write(f"\n[{self.__get_time()}] [INFO] [logger] System logging module started")
        
            else:
                with open(f'logs/{file_name}.log', "a") as file:
                    file.write(f"[{self.__get_time()}] [INFO] [logger] System logging module started")
            globals()["logger_is_started"] = True
    
    @staticmethod
    def __get_time() -> str:
        current_time = time.localtime()
        return f"{current_time[3]}:{current_time[4]}:{current_time[5]}"
    
    def create_message(self, type:str, msg:str, module:str=None):
        current_time = time.localtime()
        file_name = f"{str(current_time[2]).zfill(2)}_{str(current_time[1]).zfill(2)}_{str(current_time[0]).zfill(2)}"
        if self.robot_name is None:
            with open(f'logs/{file_name}.log', 'a', encoding='utf-8') as file:
                file.write(f"\n[{self.__get_time()}] [{type}] [{module}] {msg}")
        else:
            with open(f'logs/{self.robot_name}/{file_name}.log', 'a', encoding='utf-8') as file:
                file.write(f"\n[{self.__get_time()}] [{type}] {msg}")
    
    def debug(self, msg:str, module:str=None) -> None:
        self.create_message("DEBUG", msg, module)
        
    def info(self, msg:str, module:str=None) -> None:
        self.create_message("INFO", msg, module)
    
    def warning(self, msg:str, module:str=None) -> None:
        self.create_message("WARNING", msg, module)
    
    def error(self, msg:str, module:str=None) -> None:
        self.create_message("ERROR", msg, module)
            
    def get_logs(self, timestamp:int=None) -> list:
        if timestamp is None:
            current_time = time.localtime()
        else:
            current_time = time.localtime(timestamp)
        file_name = f"{current_time[2]}_{current_time[1]}_{current_time[0]}"
        if self.robot_name is None:
            with open(f'logs/{file_name}.log', 'r') as file:
                return file.readlines()
        else:
            if os.path.exists(f'logs/{self.robot_name}/{file_name}.log'):
                with open(f'logs/{self.robot_name}/{file_name}.log', 'r') as file:
                    return file.readlines()
            return ""