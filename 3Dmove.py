""" Module for connection 3D mouse """

import hid
import time
import requests


J1Angle = 0
J2Angle = 0
J3Angle = 0
J4Angle = 0
J5Angle = 0
J6Angle = 0

angle = 2

devices = hid.enumerate()
for device in devices:
    pass


vendor_id = 9583
product_id = 50741
device_info = next((d for d in devices if d['vendor_id'] == vendor_id and d['product_id'] == product_id), None)
print(device_info)
while True:
    if device_info:

        angle = int(requests.get("http://127.0.0.1:5000/CurentAngle").text)


        device = hid.Device(vid=vendor_id, pid=product_id, path=device_info['path'])
        data = device.read(64)
        data = str(data)
        data = data.replace("b'", "")
        data = data.replace("'", "")
        data = data.replace('\\', "", 1)
        data = data.split("\\")
        try:
            Angle1 = int.from_bytes(bytes.fromhex((data[1]).replace("x","")), byteorder='big', signed=False)
        except:
            pass
        try:
            Angle2 = int.from_bytes(bytes.fromhex((data[2]).replace("x","")), byteorder='big', signed=False)
        except:
            pass
        try:
            Angle3 = int.from_bytes(bytes.fromhex((data[3]).replace("x","")), byteorder='big', signed=False)
        except:
            pass
        try:
            Angle4 = int.from_bytes(bytes.fromhex((data[4]).replace("x","")), byteorder='big', signed=False)
        except:
            pass
        try:
            Angle5 = int.from_bytes(bytes.fromhex((data[5]).replace("x","")), byteorder='big', signed=False)
        except:
            pass
        try:
            Angle6 = int.from_bytes(bytes.fromhex((data[6]).replace("x","")), byteorder='big', signed=False)
        except:
            pass

        responce = requests.get("http://127.0.0.1:5000/CurentPosition").text
        print(responce)
        if responce == "":
            pass
        else:
            responce = responce.replace("<br>", "", 1)
            responce = responce.replace("<br>", "/")
            Commands = responce.split('/')
            for line in Commands:
                line = line.replace(",", "/")
                line = line.replace("'", "")
                line = line.replace(" ", "")
                line = line.replace("[", "")
                line = line.replace("]", "")
                line = line.replace("\n", "")
                line = line.split("/")
                J1Angle = int(line[1])
                J2Angle = int(line[2])
                J3Angle = int(line[3])
                J4Angle = int(line[4])
                J5Angle = int(line[5])
                J6Angle = int(line[6])

        
        
        if (int(Angle1) > 5 and int(Angle2) > 5):
            if (angle == 1):
                J1Angle = int(J1Angle) + 1
                requests.get(f"http://127.0.0.1:5000/CurentPosition?J1={J1Angle}&J2={J2Angle}&J3={J3Angle}&J4={J4Angle}&J5={J5Angle}&J6={J6Angle}")
                

            elif (angle == 3):
                J2Angle = int(J2Angle) + 1
                requests.get(f"http://127.0.0.1:5000/CurentPosition?J1={J1Angle}&J2={J2Angle}&J3={J3Angle}&J4={J4Angle}&J5={J5Angle}&J6={J6Angle}")


            elif (angle == 2):
                J3Angle = int(J3Angle) + 1
                requests.get(f"http://127.0.0.1:5000/CurentPosition?J1={J1Angle}&J2={J2Angle}&J3={J3Angle}&J4={J4Angle}&J5={J5Angle}&J6={J6Angle}")

            elif (angle == 4):
                J4Angle = int(J4Angle) + 1
                requests.get(f"http://127.0.0.1:5000/CurentPosition?J1={J1Angle}&J2={J2Angle}&J3={J3Angle}&J4={J4Angle}&J5={J5Angle}&J6={J6Angle}")


            elif (angle == 5):
                J5Angle = int(J5Angle) + 1
                requests.get(f"http://127.0.0.1:5000/CurentPosition?J1={J1Angle}&J2={J2Angle}&J3={J3Angle}&J4={J4Angle}&J5={J5Angle}&J6={J6Angle}")


            elif (angle == 6):
                J6Angle = int(J6Angle) + 1
                requests.get(f"http://127.0.0.1:5000/CurentPosition?J1={J1Angle}&J2={J2Angle}&J3={J3Angle}&J4={J4Angle}&J5={J5Angle}&J6={J6Angle}")


        elif (int(Angle3) > 5 and int(Angle4) > 5):
            if (angle == 1):
                J1Angle = int(J1Angle) - 1
                requests.get(f"http://127.0.0.1:5000/CurentPosition?J1={J1Angle}&J2={J2Angle}&J3={J3Angle}&J4={J4Angle}&J5={J5Angle}&J6={J6Angle}")
            elif (angle == 3):
                J2Angle = int(J2Angle) - 1
                requests.get(f"http://127.0.0.1:5000/CurentPosition?J1={J1Angle}&J2={J2Angle}&J3={J3Angle}&J4={J4Angle}&J5={J5Angle}&J6={J6Angle}")

            elif (angle == 2):
                J3Angle = int(J3Angle) - 1
                requests.get(f"http://127.0.0.1:5000/CurentPosition?J1={J1Angle}&J2={J2Angle}&J3={J3Angle}&J4={J4Angle}&J5={J5Angle}&J6={J6Angle}")

            elif (angle == 4):
                J4Angle = int(J4Angle) - 1
                requests.get(f"http://127.0.0.1:5000/CurentPosition?J1={J1Angle}&J2={J2Angle}&J3={J3Angle}&J4={J4Angle}&J5={J5Angle}&J6={J6Angle}")

            elif (angle == 5):
                J5Angle = int(J5Angle) - 1
                requests.get(f"http://127.0.0.1:5000/CurentPosition?J1={J1Angle}&J2={J2Angle}&J3={J3Angle}&J4={J4Angle}&J5={J5Angle}&J6={J6Angle}")

            elif (angle == 6):
                J6Angle = int(J6Angle) - 1
                requests.get(f"http://127.0.0.1:5000/CurentPosition?J1={J1Angle}&J2={J2Angle}&J3={J3Angle}&J4={J4Angle}&J5={J5Angle}&J6={J6Angle}")



        time.sleep(0.1)

    else:
        print('Устройство не найдено')

        
