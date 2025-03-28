import matlab.engine
import math as Math

eng = matlab.engine.start_matlab()
eng.addpath("./kinematics/First", nargout=0)

def Forward(J1, J2, J3, J4):
    coord = eng.Main_Fwd_Kinematics(float(J1), float(J2), float(J3), float(J4), nargout=1)
    return {"x": coord[0][-1], "y": coord[1][-1], "z": coord[2][-1]}

def Inverse(x,y,z):
    J1 = Math.atan2(0.0 + y, 0.0 + x) * 180.0 / Math.pi
    start = [0,0,0]
    end = [x,y,0]
    res = eng.main_inverse_kinematics(float(Math.sqrt(sum((end[i] - 0.0)**2 for i in range(len(start))))), float((z - 67.117)), nargout=1)
    # print(res)
    # if res[0][2] >= -5 and res[0][2] <= 5 and res[0][1] >= -5 and res[0][1] <= 5 and res[0][0] >= -5 and res[0][0] <= 5:
    #     return {"J1": J1, "J2": 107.7, "J3": 138.9, "J4": -47.9}
    if z-67.117 > 0:
        if 195 > (0 + (90 - (res[0][0]))) > -15:
            return {"J1": J1, "J2": -(0 + (90 - (res[0][0]))), "J3": -res[0][1], "J4": res[0][2]}
        else:
            if (-(0 + (90 - (res[0][0])))+270)+90 < 360:
                return {"J1": J1, "J2": -(-(0 + (90 - (res[0][0])))+270)+90, "J3": res[0][1], "J4": -res[0][2]}
            else:
                return {"J1": J1, "J2": -((-(0 + (90 - (res[0][0])))+270)+90)-360, "J3": res[0][1], "J4": -res[0][2]}
    else:
        if 195 > (0 + (90 - (res[0][0]))) > -15:
            return {"J1": J1, "J2": 0 + (90 - (res[0][0])), "J3": res[0][1], "J4": -res[0][2]}
        else:
            if (-(0 + (90 - (res[0][0])))+270)+90 < 360:
                return {"J1": J1, "J2": (-(0 + (90 - (res[0][0])))+270)+90, "J3": -res[0][1], "J4": res[0][2]}
            else:
                return {"J1": J1, "J2": ((-(0 + (90 - (res[0][0])))+270)+90)-360, "J3": -res[0][1], "J4": res[0][2]}