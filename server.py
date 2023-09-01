from flask import Flask, request
import variable
import time

J1MotorAngle = 0
J2MotorAngle = 0
J3MotorAngle = 0
J4MotorAngle = 0
J5MotorAngle = 0
J6MotorAngle = 0

J1AngleSpeed = 0
J2AngleSpeed = 0
J3AngleSpeed = 0
J4AngleSpeed = 0
J5AngleSpeed = 0
J6AngleSpeed = 0

StandartJ1AngleSpeed = 0
StandartJ2AngleSpeed = 0
StandartJ3AngleSpeed = 0
StandartJ4AngleSpeed = 0
StandartJ5AngleSpeed = 0
StandartJ6AngleSpeed = 0

X = 0
Y = 0
Z = 0

CurX = 0
CurY = 0
CurZ = 0

angle = 2

programm = ""

Full = str([str(variable.oldJ1angle), str(variable.oldJ2angle), str(variable.oldJ3angle), str(variable.oldJ4angle), str(variable.oldJ5angle), str(variable.oldJ6angle)])
FullSpeed = "['1.0', '1.0', '1.0', '1.0', '1.0', '1.0']"
FullStandartSpeed = "['1.0', '1.0', '1.0', '1.0', '1.0', '1.0']"

RobotWork = 0

tools_id = {"EmButton":"0", "MotorLoads":"0|0|0|0|0|0"}

logs = f'{time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]} [DEBUG] URL server started'

app = Flask(__name__)
""" URLogs """
@app.route("/Logs")
def ShowLogs():
    global logs
    write = request.args.get('W')
    NewLine = request.args.get('New')
    multi_line = request.args.get('M')
    type_mess = request.args.get('T')
    if write is None:
        if multi_line is None:
            return logs.split("<br>")[-1]
        elif multi_line == "True" or multi_line == "true":
            return logs
        else:
            return "Multi_line is not recognized"
        
    elif write == "True" or write == "true":
        if NewLine is None:
            return "The line was not added to the logs"
        else:
            if type_mess == "D" or type_mess is None:
                type_mess = "DEBUG"
            elif type_mess == "E":
                type_mess = "ERROR"
            elif type_mess == "I":
                type_mess = "INFO"
            else:
                return "Type not recognized"
            time_mess = f'{time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]}'
            logs += f"{'<br>'}{time_mess} [{type_mess}] {NewLine}"
            return "The line was added to the logs"
    else:
        return "Write is not recognized"

""" URS tool system """
@app.route("/ShowTools")
def ShowAlltool():
    return str(list(tools_id.keys()))

@app.route("/Tool")
def tool():
    global Full
    id = request.args.get('id')
    tool_conf = request.args.get('conf')
    if id != None:
        if tools_id.get(id) is None:
            return "Tool not created"
        elif tool_conf == None:
            return str(tools_id.get(id))
        else:
            tools_id[id] = tool_conf
            return str(tools_id.get(id))
    else:
        return "Tool does not exist"
        
@app.route("/CreateTool")
def CreatTool():
    tool_id = request.args.get('id')
    if tool_id == None:
        return "Tool not created"
    else:
        tools_id[tool_id] = ""
        return("Tool was created")

""" hello message """
@app.route("/")
def hello():
    return 'This URL server'

""" Curent robot position"""
@app.route('/CurentPosition')
def CurentPosition():
    global Full
    if tools_id.get("EmButton") == "1":
        J1AngleNew,J2AngleNew,J3AngleNew,J4AngleNew,J5AngleNew,J6AngleNew = J1MotorAngle,J2MotorAngle,J3MotorAngle,J4MotorAngle,J5MotorAngle,J6MotorAngle
        Full = str([str(J1AngleNew), str(J2AngleNew), str(J3AngleNew), str(J4AngleNew), str(J5AngleNew), str(J6AngleNew)])
        return Full
    else:
        J1Angle = request.args.get('J1')
        J2Angle = request.args.get('J2')
        J3Angle = request.args.get('J3')
        J4Angle = request.args.get('J4')
        J5Angle = request.args.get('J5')
        J6Angle = request.args.get('J6')
        if (J1Angle == None and J2Angle == None and J3Angle == None and J4Angle == None and J5Angle == None and J6Angle == None):
            return Full
        else:
            J1AngleNew,J2AngleNew,J3AngleNew,J4AngleNew,J5AngleNew,J6AngleNew = J1Angle,J2Angle,J3Angle,J4Angle,J5Angle,J6Angle
            Full = str([str(J1AngleNew), str(J2AngleNew), str(J3AngleNew), str(J4AngleNew), str(J5AngleNew), str(J6AngleNew)])
            return Full
    
""" Curent motors position"""
@app.route('/CurentMotorsPosition')
def CurentMotorsPosition():
    global J1MotorAngle
    global J2MotorAngle
    global J3MotorAngle
    global J4MotorAngle
    global J5MotorAngle
    global J6MotorAngle

    J1Angle = request.args.get('J1')
    J2Angle = request.args.get('J2')
    J3Angle = request.args.get('J3')
    J4Angle = request.args.get('J4')
    J5Angle = request.args.get('J5')
    J6Angle = request.args.get('J6')
    if (J1Angle == None and J2Angle == None and J3Angle == None and J4Angle == None and J5Angle == None and J6Angle == None):
        Full = str([str(J1MotorAngle), str(J2MotorAngle), str(J3MotorAngle), str(J4MotorAngle), str(J5MotorAngle), str(J6MotorAngle)])
        return Full
    else:
        J1MotorAngle = J1Angle
        J2MotorAngle = J2Angle
        J3MotorAngle = J3Angle
        J4MotorAngle = J4Angle
        J5MotorAngle = J5Angle
        J6MotorAngle = J6Angle
        Full = str([str(J1MotorAngle), str(J2MotorAngle), str(J3MotorAngle), str(J4MotorAngle), str(J5MotorAngle), str(J6MotorAngle)])
        return Full
    
""" Curent robot speed """
@app.route('/CurentSpeed')
def CurentSpeed():
    global J1AngleSpeed
    global J2AngleSpeed
    global J3AngleSpeed
    global J4AngleSpeed
    global J5AngleSpeed
    global J6AngleSpeed
    global FullSpeed

    J1Angle = request.args.get('J1')
    J2Angle = request.args.get('J2')
    J3Angle = request.args.get('J3')
    J4Angle = request.args.get('J4')
    J5Angle = request.args.get('J5')
    J6Angle = request.args.get('J6')
    if (J1Angle == None and J2Angle == None and J3Angle == None and J4Angle == None and J5Angle == None and J6Angle == None):
        return FullSpeed
    else:
        J1AngleSpeed = J1Angle
        J2AngleSpeed = J2Angle
        J3AngleSpeed = J3Angle
        J4AngleSpeed = J4Angle
        J5AngleSpeed = J5Angle
        J6AngleSpeed = J6Angle
        FullSpeed = str([str(J1AngleSpeed), str(J2AngleSpeed), str(J3AngleSpeed), str(J4AngleSpeed), str(J5AngleSpeed), str(J6AngleSpeed)])
        return FullSpeed
    
""" Standart robot speed"""
@app.route('/StandartSpeed')
def StandartSpeed():
    global StandartJ1AngleSpeed
    global StandartJ2AngleSpeed
    global StandartJ3AngleSpeed
    global StandartJ4AngleSpeed
    global StandartJ5AngleSpeed
    global StandartJ6AngleSpeed
    global FullStandartSpeed

    J1Angle = request.args.get('J1')
    J2Angle = request.args.get('J2')
    J3Angle = request.args.get('J3')
    J4Angle = request.args.get('J4')
    J5Angle = request.args.get('J5')
    J6Angle = request.args.get('J6')
    if (J1Angle == None and J2Angle == None and J3Angle == None and J4Angle == None and J5Angle == None and J6Angle == None):
        return FullStandartSpeed
    else:
        J1AngleSpeed = J1Angle
        J2AngleSpeed = J2Angle
        J3AngleSpeed = J3Angle
        J4AngleSpeed = J4Angle
        J5AngleSpeed = J5Angle
        J6AngleSpeed = J6Angle
        FullStandartSpeed = str([str(J1AngleSpeed), str(J2AngleSpeed), str(J3AngleSpeed), str(J4AngleSpeed), str(J5AngleSpeed), str(J6AngleSpeed)])
        return FullStandartSpeed

""" Started programm """
@app.route('/ProgrammPosition')
def Programm():
    global programm

    NewProgramm = request.args.get('Programm')
    if (NewProgramm == None):
        return programm
    else:
        programm = NewProgramm
        return programm
    
""" Delete programm """
@app.route('/DeleteProgramm')
def DeleteProgramm():
    global programm
    programm = ""
    return programm

""" Does the robot accept commands """
@app.route('/RobotWork')
def Robot_Work():
    global RobotWork
    work = request.args.get('Work')
    if work is None:
        return str(RobotWork)
    else:
        RobotWork = work
        return str(RobotWork)
    

# @app.route('/CurentAngle')
# def CurentAngle():
#     global angle
#     angle2 = request.args.get('Angle')
#     if angle2 is None:
#         return str(angle)
#     else:
#         angle = angle2
#         return str(angle)

""" Curent robot XYZ position """
@app.route('/XYZ')
def XYZposition():
    global X,Y,Z
    X2 = request.args.get('X')
    Y2 = request.args.get('Y')
    Z2 = request.args.get('Z')
    if (X2 == None and Y2 == None and Z2 == None):
        return (f'{X}\{Y}\{Z}')
    else:
        X = X2
        Y = Y2
        Z = Z2
        return (f'{X}\{Y}\{Z}')


if __name__ == "__main__":
    # app.run(host="192.168.0.103")
    app.run()
    