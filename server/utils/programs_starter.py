import json
import subprocess
import os
import time

import requests

host = "localhost"
port = 5000

def prepare_program(programm:str) -> str:
    new_open_function = """import builtins
import os

def restrict_open_to_directory():
    original_open = builtins.open  # сохраняем оригинальную open

    def custom_open(file, mode='r', *args, **kwargs):
        # Проверка: это попытка записи?
        is_write_mode = any(m in mode for m in ('w', 'a', 'x', '+'))

        if is_write_mode:
            # Получаем имя файла (только basename без путей)
            filename = os.path.basename(file)
            # Формируем безопасный путь в пределах "."
            safe_path = os.path.abspath(os.path.join(".", filename))

            # Проверка: файл не должен выходить за пределы "."
            if not safe_path.startswith(os.path.abspath(".")):
                raise PermissionError("Запись за пределами разрешённой директории запрещена.")

            file = safe_path

        return original_open(file, mode, *args, **kwargs)

    # Переопределяем встроенный open
    builtins.open = custom_open
    
restrict_open_to_directory()
"""
    
    return programm + "\n" + new_open_function

def UPS():
    process_program = {}
        
    def Prog(robot_name:str, token:str):
        p = subprocess.Popen(f"python programs/program.py {token}", shell=False)
        process_program[robot_name] = p

    while True:
        try:
            robots:dict = json.loads(os.environ.get("ROBOTS"))
            for robot_name, robot_data in robots.items():
                if robot_data["ProgramRunning"] == True and robot_data["Program"] != "":
                    if process_program[robot_name].poll() is not None:
                        # Set program not running
                        os.remove(f"programs/{robot_name}.py")
                        process_program[robot_name] = ""
                        url = f"https://{host}:{port}/api/set-program-run"
                        data = {'robot':robot_name, "state": False, "token":os.environ.get("SYSTEM_API_TOKEN")}
                        requests.post(url, json=data, verify=True).json()['data']
                        # Delete program
                        url = f"https://{host}:{port}/api/delete-program"
                        robot_code = robot_data["SecureCode"]
                        data = {'robot':robot_name, "code":robot_code, "token":os.environ.get("SYSTEM_API_TOKEN")}
                        requests.post(url, json=data, verify=True).json()['data']
                elif robot_data["ProgramRunning"] != "True":
                    if robot_data["Program"] == "":
                        pass
                    else:
                        program = bytes.fromhex(robot_data["Program"])
                        with open(f"programs/{robot_name}.py", "w") as file:
                            new_program = prepare_program(program.decode("utf-8"))
                            file.write(new_program)
                            file.close()

                        if program != "":
                            program_token = robot_data["ProgramToken"]
                            Prog(robot_name, program_token)

                        time.sleep(1)
                        
                        url = f"https://{host}:{port}/api/set-program-run"
                        data = {'robot':robot_name, "state": True, "token":os.environ.get("SYSTEM_API_TOKEN")}
                        requests.post(url, json=data, verify=True).json()['data']
                else:
                    if robot_data["Program"] == "":
                        os.remove(f"programs/{robot_name}.py")
                        process_program.get(f"{robot_name}").kill()
                        process_program[robot_name] = ""
                        url = f"https://{host}:{port}/api/set-program-run"
                        data = {'robot':robot_name, "state": False, "token":os.environ.get("SYSTEM_API_TOKEN")}
                        requests.post(url, json=data, verify=True).json()['data']
        
        except Exception as e:
            # print(e)
            pass

        time.sleep(3)

