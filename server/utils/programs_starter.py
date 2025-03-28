import json
import subprocess
import os
import time

import requests

def UPS():
    process_program = {}
        
    def Prog(robot_name:str, token:str):
        p = subprocess.Popen(f"python program.py {token}", shell=False)
        process_program[robot_name] = p


    while True:
        try:
            url = "https://localhost:5000/GetRobots"
            data = {"token":os.environ.get("SYSTEM_API_TOKEN")}
            resp = requests.post(url, json=json.loads(json.dumps(data, ensure_ascii=False))).text
            for robot_name in json.loads(resp)["data"].keys():
                url = "https://localhost:5000/GetRobot"
                data = {'Robot':robot_name, "token":os.environ.get("SYSTEM_API_TOKEN")}
                resp = requests.post(url, json=json.loads(json.dumps(data, ensure_ascii=False))).text
                if json.loads(resp.replace("'", '"'))["ProgramRunning"] == "True" and json.loads(resp.replace("'", '"'))["Program"] != "":
                    if process_program[robot_name].poll() is not None:
                        # Set program not running
                        process_program[robot_name] = ""
                        url = "https://localhost:5000/SetProgramRun"
                        data = {'Robot':robot_name, "State":"False", "token":os.environ.get("SYSTEM_API_TOKEN")}
                        requests.post(url, json=json.loads(json.dumps(data, ensure_ascii=False))).text
                        # Delete program
                        url = "https://localhost:5000/DeleteProgram"
                        robot_code = json.loads(resp.replace("'", '"'))["SecureCode"]
                        data = {'Robot':robot_name, "Code":robot_code, "token":os.environ.get("SYSTEM_API_TOKEN")}
                        requests.post(url, json=json.loads(json.dumps(data, ensure_ascii=False))).text
                elif json.loads(resp.replace("'", '"'))["ProgramRunning"] != "True":
                    if json.loads(resp.replace("'", '"'))["Program"] == "":
                        pass
                    else:
                        program = bytes.fromhex(json.loads(resp.replace("'", '"'))["Program"])
                        with open("program.py", "w") as file:
                            file.write(program.decode("utf-8"))
                            file.close()

                        if program != "":
                            program_token = json.loads(resp.replace("'", '"'))["ProgramToken"]
                            Prog(robot_name, program_token)


                        time.sleep(1)
                        os.remove("program.py")
                        
                        url = "https://localhost:5000/SetProgramRun"
                        data = {'Robot':robot_name, "State":"True", "token":os.environ.get("SYSTEM_API_TOKEN")}
                        requests.post(url, json=json.loads(json.dumps(data, ensure_ascii=False))).text
                else:
                    if json.loads(resp.replace("'", '"'))["Program"] == "":
                        process_program.get(f"{robot_name}").kill()
                        process_program[robot_name] = ""
                        url = "https://localhost:5000/SetProgramRun"
                        data = {'Robot':robot_name, "State":"False", "token":os.environ.get("SYSTEM_API_TOKEN")}
                        requests.post(url, json=json.loads(json.dumps(data, ensure_ascii=False))).text
        
        except:
            pass

        time.sleep(3)

