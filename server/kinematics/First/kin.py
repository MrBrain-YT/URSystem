import matlab.engine
import math

eng = matlab.engine.start_matlab()
eng.addpath("./kinematics/First", nargout=0)

def Forward(J1, J2, J3, J4):
    """ MATLAB forward kinematic """
    coord = eng.Main_Fwd_Kinematics(float(J1), float(J2), float(J3), float(J4), nargout=1)
    return {"x": coord[0][-1], "y": coord[1][-1], "z": coord[2][-1]}

# def Inverse(x,y,z):
#     """ MATLAB inverse kinematic """
#     J1 = math.atan2(0.0 + y, 0.0 + x) * 180.0 / math.pi
#     start = [0,0,0]
#     end = [x,y,0]
#     res = eng.main_inverse_kinematics(float(Math.sqrt(sum((end[i] - 0.0)**2 for i in range(len(start))))), float((z - 67.117)), nargout=1)
#     # print(res)
#     # if res[0][2] >= -5 and res[0][2] <= 5 and res[0][1] >= -5 and res[0][1] <= 5 and res[0][0] >= -5 and res[0][0] <= 5:
#     #     return {"J1": J1, "J2": 107.7, "J3": 138.9, "J4": -47.9}
#     if z-67.117 > 0:
#         if 195 > (0 + (90 - (res[0][0]))) > -15:
#             return {"J1": J1, "J2": -(0 + (90 - (res[0][0]))), "J3": -res[0][1], "J4": res[0][2]}
#         else:
#             if (-(0 + (90 - (res[0][0])))+270)+90 < 360:
#                 return {"J1": J1, "J2": -(-(0 + (90 - (res[0][0])))+270)+90, "J3": res[0][1], "J4": -res[0][2]}
#             else:
#                 return {"J1": J1, "J2": -((-(0 + (90 - (res[0][0])))+270)+90)-360, "J3": res[0][1], "J4": -res[0][2]}
#     else:
#         if 195 > (0 + (90 - (res[0][0]))) > -15:
#             return {"J1": J1, "J2": 0 + (90 - (res[0][0])), "J3": res[0][1], "J4": -res[0][2]}
#         else:
#             if (-(0 + (90 - (res[0][0])))+270)+90 < 360:
#                 return {"J1": J1, "J2": (-(0 + (90 - (res[0][0])))+270)+90, "J3": -res[0][1], "J4": res[0][2]}
#             else:
#                 return {"J1": J1, "J2": ((-(0 + (90 - (res[0][0])))+270)+90)-360, "J3": -res[0][1], "J4": res[0][2]}

# PICK AND PLACE

def distance_3d(point1, point2):
    """
    Вычисляет расстояние между двумя точками в 3D пространстве.

    Args:
        point1: Координаты первой точки (x1, y1, z1).
        point2: Координаты второй точки (x2, y2, z2).

    Returns:
        Расстояние между двумя точками.
    """

    x1, y1, z1 = point1
    x2, y2, z2 = point2

    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1

    return math.sqrt(dx**2 + dy**2 + dz**2)



def find_connecting_point(start1, start2, distance, length1, length2):
    """
    Находит точку соединения двух отрезков.

    Args:
        start1: Координаты первой стартовой точки (x, y).
        start2: Координаты второй стартовой точки (x, y).
        distance: Расстояние между стартовыми точками.
        length1: Длина первого отрезка.
        length2: Длина второго отрезка.

    Returns:
        Координаты точки соединения (x, y) или None, если решение не найдено.
    """

    x1, y1 = start1
    x2, y2 = start2

    # Проверяем, существует ли решение
    if length1 + length2 < distance:
        return None  # Отрезки слишком короткие

    # Вычисляем координаты точки соединения
    dx = x2 - x1
    dy = y2 - y1

    a = (length1**2 - length2**2 + distance**2) / (2 * distance**2)
    h = math.sqrt(length1**2 - a**2 * distance**2)

    x3 = x1 + a * dx + h * dy / distance
    y3 = y1 + a * dy - h * dx / distance

    return x3, y3

def calculate_angle(point1, point2, point3):
    """
    Вычисляет угол между тремя точками.
    """

    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3

    vector1 = (x1 - x2, y1 - y2)
    vector2 = (x3 - x2, y3 - y2)

    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]

    magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
    magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)

    # Добавляем проверку на нулевую длину векторов
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0  # Возвращаем 0 градусов, если точки совпадают

    cos_angle = dot_product / (magnitude1 * magnitude2)
    angle_rad = math.acos(cos_angle)
    angle_deg = math.degrees(angle_rad)

    return angle_deg


def Inverse(x,y,z):
    """ Pick and place inverse kinematic """
    point_3D = (x, y, z)
    J1 = math.atan2(0.0 + y, 0.0 + x) * 180.0 / math.pi
    # J1 += 180
    point1 = (0, 0, 0)
    point2 = (point_3D[0], point_3D[1], 0)
    x = distance_3d(point1, point2)
    y = point_3D[2] + 58.117
    
    _point1 = (0, 58.117, 0)
    _point2 = (-x, y + 65, 0)
    distance = distance_3d(_point1, _point2)
    start1 = (0, 58.117)
    start2 = (-x, y + 65)
    length1 = 195
    length2 = 235
    connecting_point = find_connecting_point(start1, start2, distance, length1, length2)
    if connecting_point:
        # Вычисляем углы
        angle1 = calculate_angle((0,0), (0, 58.117), connecting_point)
        angle2 = calculate_angle((0, 58.117), connecting_point, start2)
        third_point_y = (start2[0], start2[1]-65)
        angle3 = calculate_angle(connecting_point, start2, third_point_y)

        
        J2 = 180 - (angle1 - 90)
        J3 = 180 - angle2
        J4 = -(180 - angle3)
        return {"J1": J1, "J2": J2, "J3": J3, "J4": J4}
    else:
        print("Решение не найдено.")