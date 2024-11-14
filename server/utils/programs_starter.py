import json
import subprocess
import os
import time

import requests

def UPS():
    process_program = {}
        
    def Prog():
        p = subprocess.Popen("python program.py", shell=False)
        process_program[i] = p


    while True:
        try:
            url = "https://localhost:5000/GetRobots"
            data = {"token":os.environ.get("SYSTEM_API_TOKEN")}
            resp = requests.post(url, data=json.loads(json.dumps(data, ensure_ascii=False))).text
            for i in json.loads(resp.replace("'", '"')).keys():
                url = "https://localhost:5000/GetRobot"
                data = {'Robot':i, "token":os.environ.get("SYSTEM_API_TOKEN")}
                resp = requests.post(url, data=json.loads(json.dumps(data, ensure_ascii=False))).text
                if json.loads(resp.replace("'", '"'))["ProgramRunning"] != "True":
                    if json.loads(resp.replace("'", '"'))["Program"] == "":
                        pass
                    else:
                        program = bytes.fromhex(json.loads(resp.replace("'", '"'))["Program"])
                        with open("program.py", "w") as file:
                            file.write(program.decode("utf-8"))
                            file.close()

                        if program != "":
                            Prog()


                        time.sleep(1)
                        os.remove("program.py")
                        
                        url = "https://localhost:5000/SetProgramRun"
                        data = {'Robot':i, "State":"True", "token":os.environ.get("SYSTEM_API_TOKEN")}
                        requests.post(url, data=json.loads(json.dumps(data, ensure_ascii=False))).text
                else:
                    if json.loads(resp.replace("'", '"'))["Program"] == "":
                        process_program.get(f"{i}").kill()
                        url = "https://localhost:5000/SetProgramRun"
                        data = {'Robot':i, "State":"False", "token":os.environ.get("SYSTEM_API_TOKEN")}
                        requests.post(url, data=json.loads(json.dumps(data, ensure_ascii=False))).text
        except:
            pass

        time.sleep(3)

