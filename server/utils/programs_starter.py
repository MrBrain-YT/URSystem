import json
import subprocess
import os
import time

import requests

host = "localhost"
port = 5000

def UPS():
    process_program = {}
        
    def Prog(robot_name:str, token:str):
        p = subprocess.Popen(f"python program.py {token}", shell=False)
        process_program[robot_name] = p

    while True:
        try:
            url = f"https://{host}:{port}/api/get-robots"
            data = {"token":os.environ.get("SYSTEM_API_TOKEN")}
            resp = requests.post(url, json=data, verify=True).json()['data']
            for robot_name in resp.keys():
                url = f"https://{host}:{port}/api/get-robot"
                data = {'robot':robot_name, "token":os.environ.get("SYSTEM_API_TOKEN")}
                resp = requests.post(url, json=data, verify=True).json()['data']
                if resp["ProgramRunning"] == "True" and resp["Program"] != "":
                    if process_program[robot_name].poll() is not None:
                        # Set program not running
                        process_program[robot_name] = ""
                        url = f"https://{host}:{port}/api/set-program-run"
                        data = {'robot':robot_name, "state": False, "token":os.environ.get("SYSTEM_API_TOKEN")}
                        requests.post(url, json=data, verify=True).json()['data']
                        # Delete program
                        url = f"https://{host}:{port}/api/delete-program"
                        robot_code = json.loads(resp.replace("'", '"'))["SecureCode"]
                        data = {'robot':robot_name, "Code":robot_code, "token":os.environ.get("SYSTEM_API_TOKEN")}
                        requests.post(url, json=data, verify=True).json()['data']
                elif resp["ProgramRunning"] != "True":
                    if resp["Program"] == "":
                        pass
                    else:
                        program = bytes.fromhex(resp["Program"])
                        with open("program.py", "w") as file:
                            file.write(program.decode("utf-8"))
                            file.close()

                        if program != "":
                            program_token = resp["ProgramToken"]
                            Prog(robot_name, program_token)

                        time.sleep(1)
                        os.remove("program.py")
                        
                        url = f"https://{host}:{port}/api/set-program-run"
                        data = {'robot':robot_name, "state": True, "token":os.environ.get("SYSTEM_API_TOKEN")}
                        requests.post(url, json=data, verify=True).json()['data']
                else:
                    if json.loads(resp.replace("'", '"'))["Program"] == "":
                        process_program.get(f"{robot_name}").kill()
                        process_program[robot_name] = ""
                        url = f"https://{host}:{port}/api/set-program-run"
                        data = {'robot':robot_name, "state": False, "token":os.environ.get("SYSTEM_API_TOKEN")}
                        requests.post(url, json=data, verify=True).json()['data']
        
        except:
            pass

        time.sleep(3)

