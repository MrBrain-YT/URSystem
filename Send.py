import requests
import time
import numpy as np
from scipy.interpolate import CubicSpline
import variable

RspeedJ1 = 0
RspeedJ2 = 0
RspeedJ3 = 0
RspeedJ4 = 0
RspeedJ5 = 0
RspeedJ6 = 0

lineP = ""
lineC = ""

# blocks variables
programm_blocks = {}
startblock = None

def interpolate_points(start_point, intermediate_point, end_point, num_points):
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

def interpretator(line):
    while True:
        responce2 = requests.get("http://127.0.0.1:5000/RobotWork").text
        if responce2 == "0":
            pass
        else:
            """ Comment command """
            if "#" in line:
                pass

            elif "While" in line:
                """ While command """
                try:
                    LIndex = Commands.index(line)
                    TabCount = line.count("    ")
                    line = line.replace("While(", "")
                    line = line.replace(")", "")
                    line2 = line.replace("    "*TabCount, "")
                    if line2 == "":
                        """ Infinity while """
                        while True:
                            responce = requests.get("http://127.0.0.1:5000/ProgrammPosition").text
                            if responce == "":
                                break
                            else:
                                for lines in range(LIndex+1, len(Commands)):
                                    responce = requests.get("http://127.0.0.1:5000/ProgrammPosition").text
                                    if responce == "":
                                        break
                                    else:
                                        if "    "*(TabCount+1) in Commands[lines] or "" == Commands[lines]:
                                            interpretator(Commands[lines])
                                            time.sleep(1)
                                        else:
                                            break
                    else:
                        """ Counter while """
                        for i in range(int(line2)-1):
                            responce = requests.get("http://127.0.0.1:5000/ProgrammPosition").text
                            if responce == "":
                                break
                            else:
                                for lines in range(LIndex+1, len(Commands)):
                                    responce = requests.get("http://127.0.0.1:5000/ProgrammPosition").text
                                    if responce == "":
                                        break
                                    else:
                                        if TabCount+1 == Commands[lines].count("    ") or "" == Commands[lines]:
                                            interpretator(Commands[lines])
                                            time.sleep(1)
                                        else:
                                            break
                except:
                    error_line = f"Line /|{line}|\ have error. Type: While"
                    requests.get(f"http://127.0.0.1:5000/Logs?W=true&T=E&New={error_line}")

            elif "Debug" in line:
                    """ CIRC command """
                    line = line.replace("Debug(", "", 1)
                    line = line.replace(")", "").replace("    ", "")
                    requests.get(f"http://127.0.0.1:5000/Logs?W=true&New={line}")
                    print(f"[DEBUG] {line}")
                    time.sleep(0.5)

            elif "Time" in line:
                """ Time command """
                print(line ,"sleep")
                try:
                    time.sleep(int(line.replace("Time ", "").replace("    ", "")))
                except:
                    error_line = f"Line /|{line}|\ have error. Type: Time"
                    requests.get(f"http://127.0.0.1:5000/Logs?W=true&T=E&New={error_line}")

            elif "get" in line:
                """ Request get command """
                try:
                    line = line.replace("get(", "", 1).replace(")","").replace("$","/").replace("    ", "")
                    requests.get(line)
                except:
                    error_line = f"Line /|{line}|\ have error. Type: get"
                    requests.get(f"http://127.0.0.1:5000/Logs?W=true&T=E&New={error_line}")

            elif "@_" in line:
                """ Call block command """
                try:
                    name = line.replace("@_", "", 1).replace("    ", "")
                    start, stop = str(programm_blocks.get(name)).split(",")
                    for i in range(int(start), int(stop)+1):
                        interpretator(Commands[i].replace("    ", "", 1))
                except:
                    error_line = f"Line /|{line}|\ have error. Type: Call block"
                    requests.get(f"http://127.0.0.1:5000/Logs?W=true&T=E&New={error_line}")

            elif "CIRC" in line:
                """ CIRC command """
                try:
                    line = line.replace("CIRC", "").replace("    ", "")
                    line = line.replace("[", "")
                    line = line.replace("]", "")
                    XYZpoint = line.split("|")
                    StartPoint = XYZpoint[0].replace(",",".").split("\\")
                    DopPoint = XYZpoint[1].replace(",",".").split("\\")
                    EndPoint = XYZpoint[2].replace(",",".").split('\\')
                    interpolated_points = interpolate_points(list(map(float, StartPoint)), list(map(float, DopPoint)), list(map(float, EndPoint)), 100)
                    for point in interpolated_points:
                        while True:
                            responce = requests.get("http://127.0.0.1:5000/RobotWork").text
                            if responce == "0":
                                pass
                            else:
                                requests.get(f"http://127.0.0.1:5000/XYZposition?X={point[0]}&Y={point[1]}&Z={point[2]}")
                                break
                except:
                    error_line = f"Line /|{line}|\ have error. Type: CIRC"
                    requests.get(f"http://127.0.0.1:5000/Logs?W=true&T=E&New={error_line}")

            elif "SPEED" in line:
                """ SPEED command """
                line = line.replace(",", "/").replace("    ", "")
                line = line.replace("'", "")
                line = line.replace(" ", "")
                line = line.replace("SPEED[", "")
                line = line.replace("]", "")
                line = line.replace("\n", "")
                line = line.split("/")
                try:
                    requests.get(f"http://127.0.0.1:5000/CurentSpeed?J1={line[0]}&J3={line[2]}&J2={line[1]}&J4={line[3]}&J5={line[4]}&J6={line[5]}")
                except:
                    error_line = f"Line /|{line}|\ have error. Type: SPEED"
                    requests.get(f"http://127.0.0.1:5000/Logs?W=true&T=E&New={error_line}")
                break
                        
            elif "LIN" in line:
                """ LIN command """
                try:
                    responce = requests.get("http://127.0.0.1:5000/CurentPosition").text
                    responce = responce.replace("<br>", "", 1)
                    responce = responce.replace("<br>", "/")
                    line2 = responce.replace(",", "/")
                    line2 = line2.replace("'", "").replace("    ", "")
                    line2 = line2.replace(" ", "")
                    line2 = line2.replace("[", "")
                    line2 = line2.replace("LIN", "")
                    line2 = line2.replace("]", "")
                    line2 = line2.replace("\n", "")
                    line2 = line2.replace("'", "")
                    lineC = line2.split("/")
                    if "Home" in line:
                        RspeedJ1 = abs(float(lineC[0])- float(variable.oldJ1angle))
                        RspeedJ2 = abs(float(lineC[1])- float(variable.oldJ2angle))
                        RspeedJ3 = abs(float(lineC[2])- float(variable.oldJ3angle))
                        RspeedJ4 = abs(float(lineC[3])- float(variable.oldJ4angle))
                        RspeedJ5 = abs(float(lineC[4])- float(variable.oldJ5angle))
                        RspeedJ6 = abs(float(lineC[5])- float(variable.oldJ6angle))
                    
                        MaxSpeed = max([RspeedJ1, RspeedJ2, RspeedJ3, RspeedJ4, RspeedJ5, RspeedJ6])
                        if MaxSpeed == RspeedJ1:
                            OfficialAngle = RspeedJ1
                        elif MaxSpeed == RspeedJ2:
                            OfficialAngle = RspeedJ2
                        elif MaxSpeed == RspeedJ3:
                            OfficialAngle = RspeedJ3
                        elif MaxSpeed == RspeedJ4:
                            OfficialAngle = RspeedJ4
                        elif MaxSpeed == RspeedJ5:
                            OfficialAngle = RspeedJ5
                        elif MaxSpeed == RspeedJ6:
                            OfficialAngle = RspeedJ6
                        
                        SpeedJ1 = RspeedJ1 / OfficialAngle
                        SpeedJ2 = RspeedJ2 / OfficialAngle
                        SpeedJ3 = RspeedJ3 / OfficialAngle
                        SpeedJ4 = RspeedJ4 / OfficialAngle
                        SpeedJ5 = RspeedJ5 / OfficialAngle
                        SpeedJ6 = RspeedJ6 / OfficialAngle
                        requests.get(f"http://127.0.0.1:5000/CurentSpeed?J1={SpeedJ1}&J2={SpeedJ2}&J3={SpeedJ3}&J4={SpeedJ4}&J5={SpeedJ5}&J6={SpeedJ6}")
                        requests.get(f"http://127.0.0.1:5000/CurentPosition?J1={float(variable.oldJ1angle)}&J2={float(variable.oldJ2angle)}&J3={float(variable.oldJ3angle)}&J4={float(variable.oldJ4angle)}&J5={float(variable.oldJ5angle)}&J6={float(variable.oldJ6angle)}")
                    else:
                        line = line.replace(",", "/").replace("    ", "")
                        line = line.replace("'", "")
                        line = line.replace(" ", "")
                        line = line.replace("[", "")
                        line = line.replace("]", "")
                        line = line.replace("LIN", "")
                        line = line.replace("\n", "")
                        line = line.split("/")

                        lineP = line
                        
                        RspeedJ1 = abs(float(lineC[0])- float(lineP[0]))
                        RspeedJ2 = abs(float(lineC[1])- float(lineP[1]))
                        RspeedJ3 = abs(float(lineC[2])- float(lineP[2]))
                        RspeedJ4 = abs(float(lineC[3])- float(lineP[3]))
                        RspeedJ5 = abs(float(lineC[4])- float(lineP[4]))
                        RspeedJ6 = abs(float(lineC[5])- float(lineP[5]))
                    
                        MaxSpeed = max([RspeedJ1, RspeedJ2, RspeedJ3, RspeedJ4, RspeedJ5, RspeedJ6])
                        if MaxSpeed == RspeedJ1:
                            OfficialAngle = RspeedJ1
                        elif MaxSpeed == RspeedJ2:
                            OfficialAngle = RspeedJ2
                        elif MaxSpeed == RspeedJ3:
                            OfficialAngle = RspeedJ3
                        elif MaxSpeed == RspeedJ4:
                            OfficialAngle = RspeedJ4
                        elif MaxSpeed == RspeedJ5:
                            OfficialAngle = RspeedJ5
                        elif MaxSpeed == RspeedJ6:
                            OfficialAngle = RspeedJ6
                        
                        SpeedJ1 = RspeedJ1 / OfficialAngle
                        SpeedJ2 = RspeedJ2 / OfficialAngle
                        SpeedJ3 = RspeedJ3 / OfficialAngle
                        SpeedJ4 = RspeedJ4 / OfficialAngle
                        SpeedJ5 = RspeedJ5 / OfficialAngle
                        SpeedJ6 = RspeedJ6 / OfficialAngle
                        requests.get(f"http://127.0.0.1:5000/CurentSpeed?J1={SpeedJ1}&J2={SpeedJ2}&J3={SpeedJ3}&J4={SpeedJ4}&J5={SpeedJ5}&J6={SpeedJ6}")
                        requests.get(f"http://127.0.0.1:5000/CurentPosition?J1={float(lineP[0])}&J2={float(lineP[1])}&J3={float(lineP[2])}&J4={float(lineP[3])}&J5={float(lineP[4])}&J6={float(lineP[5])}")
                except:
                    error_line = f"Line /|{line}|\ have error. Type: LIN"
                    requests.get(f"http://127.0.0.1:5000/Logs?W=true&T=E&New={error_line}")
            

            elif "[" in line and "]" in line:
                """ PTP command """
                if "Home" in line:
                    try:
                        requests.get(f"http://127.0.0.1:5000/CurentPosition?J1={variable.oldJ1angle}&J3={variable.oldJ2angle}&J2={variable.oldJ3angle}&J4={variable.oldJ4angle}&J5={variable.oldJ5angle}&J6={variable.oldJ6angle}")
                    except:
                        error_line = f"Line /|{line}|\ have error. Type: PTP"
                        requests.get(f"http://127.0.0.1:5000/Logs?W=true&T=E&New={error_line}")
                else:
                    line = line.replace(",", "/").replace("    ", "")
                    line = line.replace("'", "")
                    line = line.replace(" ", "")
                    line = line.replace("[", "")
                    line = line.replace("]", "")
                    line = line.replace("\n", "")
                    line = line.split("/")
                    try:
                        requests.get(f"http://127.0.0.1:5000/CurentPosition?J1={line[0]}&J3={line[2]}&J2={line[1]}&J4={line[3]}&J5={line[4]}&J6={line[5]}")
                    except:
                        error_line = f"Line /|{line}|\ have error. Type: PTP"
                        requests.get(f"http://127.0.0.1:5000/Logs?W=true&T=E&New={error_line}")

            else:
                """ No command """
                if line == "" or "\n":
                    pass
                else:
                    error_line = f"Line /|{line}|\ is not a command"
                    print(error_line)
                    requests.get(f"http://127.0.0.1:5000/Logs?W=true&T=E&New={error_line}")
            break

curent_while = 0
line_index = 0

while True:
    responce = requests.get("http://127.0.0.1:5000/ProgrammPosition").text
    if responce == "":
        time.sleep(1)
        line_index = 0
    else:
        responce = responce.replace("<br>", "*")
        Commands = responce.split('*')
        for line in Commands:
            line = line.replace("^", "#", 1).replace('$', '/').replace('!', '&')
            line_index += 1
            while True:
                if requests.get("http://127.0.0.1:5000/ProgrammPosition").text == "":
                    break
                else:
                    if "#" in line:
                        break
                    else:
                        # Init block command
                        if "=" in line and "    " not in line:
                            startblock = line_index
                            name = line.replace("=", "")
                            curent_while = 1

                            counter_line = line_index-1
                            for block_command in Commands[startblock:]:
                                if "    " in block_command and '' != block_command and "\n" != block_command:
                                    counter_line+=1
                                else:
                                    programm_blocks[name] = f"{startblock},{counter_line}"
                                    break
                            break
                        

                        # Other commands
                        else:
                            if curent_while == 1:
                                if "    " in line:
                                    break
                                else:
                                    interpretator(line)
                                    time.sleep(1)
                                    curent_while = 0
                                    break
                            else:
                                interpretator(line)
                                time.sleep(1)
                                break
            
        while True:    
            responce2 = requests.get("http://127.0.0.1:5000/RobotWork").text
            if responce2 == "0":
                continue
            else:     
                requests.get("http://127.0.0.1:5000/DeleteProgramm")
                resp = requests.get("http://127.0.0.1:5000/StandartSpeed").text.replace("[", "").replace("]", "").replace("'", "").split(",")
                requests.get(f"http://127.0.0.1:5000/CurentSpeed?J1={resp[0]}&J3={resp[1]}&J2={resp[2]}&J4={resp[3]}&J5={resp[4]}&J6={resp[5]}")
                startblock = None
                programm_blocks.clear()
                line_index = 0
                break

