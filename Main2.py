import dearpygui.dearpygui as dpg
import time
from dearpygui.demo import *
import subprocess
import win32gui
import win32con
from dearpygui_ext import logger
import variable
import random
import requests
import kinematic
import pyperclip
import os

# # Путь к EXE-файлу
# exe_path = '3dVisualization/RobotA.exe'
# # # Запуск EXE-файла
# subprocess.Popen(exe_path)
# time.sleep(3)

# # Получение дескриптора окна
# window_title = "RobotA"
# window_handle = win32gui.FindWindow(None, window_title)
# print(window_handle)

# # Установка окна поверх всех окон
# win32gui.SetWindowPos(window_handle, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
# win32gui.MoveWindow(window_handle, 0,827,980,440,True)
# window_style = win32gui.GetWindowLong(window_handle, win32con.GWL_STYLE)
# # Удаление стилей, отвечающих за перемещение окна
# window_style &= ~win32con.WS_THICKFRAME  # Убираем возможность изменения размера окна
# window_style &= ~win32con.WS_SYSMENU  # Убираем системное меню
# window_style &= ~win32con.WS_CAPTION
# # Установка нового стиля окна
# win32gui.SetWindowLong(window_handle, win32con.GWL_STYLE, window_style)

x_data = [4.0, 4.0, 4.0, 3.0, 1.0, 0.0]
y_data = [0.0, 10.0, 40.0, 40.0, 40.0, 40.0]
oldHeight = 750

X = 0
Y = 0
Z = 0

oldJ1angle = float(variable.oldJ1angle)
oldJ2angle = float(variable.oldJ2angle)
oldJ3angle = float(variable.oldJ3angle)
oldJ4angle = float(variable.oldJ4angle)
oldJ5angle = float(variable.oldJ5angle)
oldJ6angle = float(variable.oldJ6angle)

old_log = ""
log_panel = None

TextImage = '''                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                              
                                             SSi;                                                             
                                            rSii5Xrs                  ,ss           ,;Shh5                    
                                      iSS5S2ssss5sSSsiiiSi2Siii;rr###B###M#BBB#2ssir#@           
                                     ;HGS552iSiiXi22SSii5i25SiSSS&HM##A;B2ri#M#525Si##r          
                                     Hh3X55X555SX223XXXX353XXX2iSSM#MMM@#M##MM#3X22S#@           
                                     MSXXXX32253X5SG,.                559,   .S5M#B; s235X            
                                   ,5MX2h&X2225SX5                                                            
                                ,ii99#G3hS5G5XX2X                                                             
                                Xs922B3222252352i                                                             
                                 X255Ah2223s&225                                                              
                                 S932GG2XX9ih25                                                               
                                 sh339&XX2253S                                                                
                                 .h&hhMGh&s5.                                                                 
                                  iAGGMh&5S.                                                                  
                                  is2AB5S5S                                                                   
                                  iSiSSSSi5                                                                   
                                  siiiiSSS5                                                                   
                                  rSSSSSSS5                                                                   
                                  ;iiiiSSS5                                                                   
                                  ;S5iiSSS5                                                                   
                                  ;i2Xii5SS                                                                   
                                  ;23325XSS                                                                   
                                  ;555SXXSS                                                                   
                                  r;   i555                                                                   
                                  sGA&h2X55                                                                   
                                  ShAAGX22S                                                                   
                                  ShAAh222S                                                                   
                                  ShAAh252S:                                                                                                                                    
                                  ;555SXXSS                                                                   
                                  r;   i555                                                                   
                                  sGA&h2X55                                                                   
                                  ShAAGX22S                                                                   
                                  ShAAh222S                                                                   
                                  ShAAh252S:
                                 :XHAHhHMhS5                                                                  
                                 SHHA&h&HA35                                                                  
                                 5A&HAh3X9ASS                                                                 
                                ,h3hHA9h3XX5X5                                                                
                             ,52ih22A&XXXX23s35                                                               
                           r55XX5X25HH2X2223Sh5                                                               
                        s5525552i33BGA222393s35.                                                              
                       55S55552X23h&HA9XX9955Xi.                                                              
                       5S55255225H&3AH22322GiXr                                                               
                       552X55GH23BH2235X&HH5iS                                                                
                       252X2HMBBX#.iSXSSSSSS25                                                                
                      .5SSSSSS52X2SS:,5255Si5                                                                 
                     ,5iiiiiSS55522iX3X2Sis5;                                                                 
                     ,SiiiSiSSS555XXis22                                                                      
                      5SSSSSSS555552ssiS                                                                      
                      :&GGGhhhhhhhhX2hG #                                                                     
               @@##@.@#AHS2X####52#BAHh                                                                       
              .MMM@###H##M#MMMM#HXGGMM@Mh                                                                     
              .#MM@#@##MMMMMMMMMH2XMM#A@B#;                                                                   
                r;;;;;;;;;;;;;;::;:::::;,:;:::                                                                
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                             '''

speedImage = "Controll speed robot angles"

def minimize_window(window_handle):
    win32gui.ShowWindow(window_handle, win32con.SW_MINIMIZE)

def maximize_window(window_handle):
    win32gui.ShowWindow(window_handle, win32con.SW_MAXIMIZE)
    win32gui.SetWindowPos(window_handle, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    win32gui.MoveWindow(window_handle, 0,827,980,440,True)
    window_style = win32gui.GetWindowLong(window_handle, win32con.GWL_STYLE)
    window_style &= ~win32con.WS_THICKFRAME  # Убираем возможность изменения размера окна
    window_style &= ~win32con.WS_SYSMENU  # Убираем системное меню
    window_style &= ~win32con.WS_CAPTION
    win32gui.SetWindowLong(window_handle, win32con.GWL_STYLE, window_style)

def Font():
    with dpg.font_registry():
        dpg.add_font("123.ttf", 13)
        dpg.show_font_manager()

# def OpenNotification():
#     dpg.show_item("_Notification")
#     dpg.hide_item("Logs")
#     dpg.hide_item("Phisic panel")

def OpenAccount():
    # dpg.hide_item("_Notification")
    dpg.hide_item("Logs")
    dpg.show_item("Phisic panel")

def OpenLogs():
    dpg.show_item("Logs")
    dpg.hide_item("Phisic panel")
    # dpg.hide_item("_Notification")

def DebugColor():
    dpg.show_style_editor()
    
def DebugMetrics():
    dpg.show_metrics()

def StartProgrammEditor():
    dpg.show_item("NoProgramm")
    dpg.hide_item("Programm")

def OpenProgrammInEditor():
    dpg.show_item("Programm")
    dpg.hide_item("NoProgramm")

def CloseProgrammInEditor():
    if len(dpg.get_item_children("ProgrammTabs")[1]) == 1:
        dpg.show_item("NoProgramm")
        dpg.hide_item("Programm")
    for child in range(0, len(dpg.get_item_children("ProgrammTabs")[1])):
        if child == 0:
            pass
        else:
            Prog =  (dpg.get_item_children(dpg.get_item_children("ProgrammTabs")[1][child])[1][1])
            if dpg.is_item_visible(Prog):
                dpg.delete_item(dpg.get_item_children("ProgrammTabs")[1][child])



def OpenAngleControll():
    for i in dpg.get_item_children("Controll")[1]:
        dpg.hide_item(i)
    dpg.show_item("AngleControl")

def OpenXYZControll():
    for i in dpg.get_item_children("Controll")[1]:
        dpg.hide_item(i)
    dpg.show_item("XYZControl")

def OpenCalibrationControll():
    for i in dpg.get_item_children("Controll")[1]:
        dpg.hide_item(i)
    dpg.show_item("Calibration")

def OpenHomePosition():
    for i in dpg.get_item_children("Controll")[1]:
        dpg.hide_item(i)
    dpg.show_item("HomePosition")

def OpenSpeedControll():
    for i in dpg.get_item_children("Controll")[1]:
        dpg.hide_item(i)
    dpg.show_item("SpeedControll")






def count_lines():
    global oldHeight
    for child in range(0, len(dpg.get_item_children("ProgrammTabs")[1])):
        if child == 0:
            pass
        else:
            Prog =  (dpg.get_item_children(dpg.get_item_children("ProgrammTabs")[1][child])[1][1])
            if dpg.is_item_visible(Prog):
                text = dpg.get_value(Prog)
                lines = text.split("\n")
                line_count = len(lines)
                for i in dpg.get_item_children(dpg.get_item_children(dpg.get_item_children("ProgrammTabs")[1][child])[1][0])[1]:
                    dpg.delete_item(i)
                x = 0
                y = 0
                for i in range(1, line_count+1):
                    text_id = dpg.add_text(f"{i}", parent=dpg.get_item_children(dpg.get_item_children("ProgrammTabs")[1][child])[1][0])
                    dpg.set_item_pos(text_id, pos=[x,y])
                    y += 20
                    dpg.bind_item_font(text_id, font)
                    # print(text_id)

                    if line_count <= 37:
                        pass
                    else:
                        if (750) + ((line_count - 37) * 20) == oldHeight:
                            pass
                        else:
                            newHeight = (750) + ((line_count - 37) * 20)
                            dpg.set_item_height(dpg.get_item_children(dpg.get_item_children("ProgrammTabs")[1][child])[1][1], newHeight)
                            dpg.set_item_height(dpg.get_item_children(dpg.get_item_children("ProgrammTabs")[1][child])[1][0], newHeight)
                            oldHeight = newHeight



def AnglePlot(sender, app_data):
    _helper_data = app_data[0]
    transformed_x = app_data[1]
    transformed_y = app_data[2]
    mouse_x_pixel_space = _helper_data["MouseX_PixelSpace"]
    mouse_y_pixel_space = _helper_data["MouseY_PixelSpace"]
    dpg.delete_item(sender, children_only=True, slot=2)
    dpg.push_container_stack(sender)
    dpg.configure_item("demo_custom_series", tooltip=False)
    for i in range(0, len(transformed_x)):
        if i <= len(transformed_x)-2:
            dpg.draw_line((transformed_x[i], transformed_y[i]), (transformed_x[i+1], transformed_y[i+1]), color=(255, 0, 0, 255), thickness=1)
        else:
            pass
        
        dpg.draw_circle((transformed_x[i], transformed_y[i]), 15, fill=(0, 150, 0, 255))
        dpg.draw_text((transformed_x[i]-5, transformed_y[i]-9), str(i+1), size=20)
        if mouse_x_pixel_space < transformed_x[i]+15 and mouse_x_pixel_space > transformed_x[i]-15 and mouse_y_pixel_space > transformed_y[i]-15 and mouse_y_pixel_space < transformed_y[i]+15:
            dpg.draw_circle((transformed_x[i], transformed_y[i]), 30)
            dpg.configure_item("demo_custom_series", tooltip=True)
            dpg.set_value("custom_series_text", "Current angle: " + str(i+1))
            dpg.set_value("CentralPlot", dpg.get_value(f"load_{str(i+1)}"))
            dpg.set_value("CurAngForPlot", f"J{str(i+1)}")
    dpg.pop_container_stack()
    
def hep(sender):
    if sender == "<":
        angle = dpg.get_value("CurAngForPlot")
        if angle == "J1":
            dpg.set_value("CurAngForPlot", "J6")
            dpg.set_value("CentralPlot", dpg.get_value("load_6"))
        if angle == "J6":
            dpg.set_value("CurAngForPlot", "J5")
            dpg.set_value("CentralPlot", dpg.get_value("load_5"))
        if angle == "J5":
            dpg.set_value("CurAngForPlot", "J4")
            dpg.set_value("CentralPlot", dpg.get_value("load_4"))
        if angle == "J4":
            dpg.set_value("CurAngForPlot", "J3")
            dpg.set_value("CentralPlot", dpg.get_value("load_3"))
        if angle == "J3":
            dpg.set_value("CurAngForPlot", "J2")
            dpg.set_value("CentralPlot", dpg.get_value("load_2"))
        if angle == "J2":
            dpg.set_value("CurAngForPlot", "J1")
            dpg.set_value("CentralPlot", dpg.get_value("load_1"))
    else:
        angle = dpg.get_value("CurAngForPlot")
        if angle == "J1":
            dpg.set_value("CurAngForPlot", "J2")
            dpg.set_value("CentralPlot", dpg.get_value("load_2"))
        if angle == "J2":
            dpg.set_value("CurAngForPlot", "J3")
            dpg.set_value("CentralPlot", dpg.get_value("load_3"))
        if angle == "J3":
            dpg.set_value("CurAngForPlot", "J4")
            dpg.set_value("CentralPlot", dpg.get_value("load_4"))
        if angle == "J4":
            dpg.set_value("CurAngForPlot", "J5")
            dpg.set_value("CentralPlot", dpg.get_value("load_5"))
        if angle == "J5":
            dpg.set_value("CurAngForPlot", "J6")
            dpg.set_value("CentralPlot", dpg.get_value("load_6"))
        if angle == "J6":
            dpg.set_value("CurAngForPlot", "J1")
            dpg.set_value("CentralPlot", dpg.get_value("load_1"))

def changeSendData(sender):
    value = dpg.get_value(sender)
    if value == True:
        AnglesControll()
        dpg.hide_item("send_Button")
    else:
        dpg.show_item("send_Button")

def GetXYZ_Point(sender):
    dpg.set_value("X_input", dpg.get_value(sender)[0])
    dpg.set_value("Y_input", dpg.get_value(sender)[2])
    dpg.set_value("Z_input", dpg.get_value(sender)[1])

def SetXYZ_Point():
    global X, Y, Z
    dpg.set_value("StatePatron", dpg.get_value("StatePatron_2"))
    dpg.set_value("XYZ_slider", [dpg.get_value("X_input"), dpg.get_value("Y_input"), dpg.get_value("Z_input")])
    if dpg.get_value("AutoSendXYZ") == True:
        if dpg.get_value("StatePatron_2"):
            responce = requests.get("http://127.0.0.1:5000/Tool?id=PhisicPanel_1").text.split("|")
            requests.get(f"http://127.0.0.1:5000/Tool?id=PhisicPanel_1&conf=1|{responce[1]}")
        else:
            responce = requests.get("http://127.0.0.1:5000/Tool?id=PhisicPanel_1").text.split("|")
            requests.get(f"http://127.0.0.1:5000/Tool?id=PhisicPanel_1&conf=0|{responce[1]}")
        X = dpg.get_value("X_input")
        Y = dpg.get_value("Y_input")
        Z = dpg.get_value("Z_input")
        J1, J2, J3, J4, J5, J6, = kinematic.CalcRevKin(float(x), float(y), float(Z),-90,90,-90,"N", 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0)
        requests.get((f"http://127.0.0.1:5000/CurentPosition?J1={J1}&J2={J2}&J3={J3}&J4={J4}&J5={J5}&J6={J6}"))
        dpg.set_value("J1input", J1)
        dpg.set_value("J2input", J2)
        dpg.set_value("J3input", J3)
        dpg.set_value("J4input", J4)
        dpg.set_value("J5input", J5)
        dpg.set_value("J6input", J6)

    
def changeSendDataXYZ(sender):
    value = dpg.get_value(sender)
    if value == True:
        SendXYZ()
        dpg.hide_item("XYZ_send_Button")
    else:
        dpg.show_item("XYZ_send_Button")


def AnglesControll():
    global oldJ1angle, oldJ2angle, oldJ3angle, oldJ4angle, oldJ5angle, oldJ6angle
    dpg.set_value("StatePatron_2", dpg.get_value("StatePatron"))
    if dpg.get_value("AutoSendAngels") == True:
        oldJ1angle = dpg.get_value("J1input")
        oldJ2angle = dpg.get_value("J2input")
        oldJ3angle = dpg.get_value("J3input")
        oldJ4angle = dpg.get_value("J4input")
        oldJ5angle = dpg.get_value("J5input")
        oldJ6angle = dpg.get_value("J6input")
        dpg.set_value("HomeAngle_1", dpg.get_value("J1input"))
        dpg.set_value("HomeAngle_2", dpg.get_value("J2input"))
        dpg.set_value("HomeAngle_3", dpg.get_value("J3input"))
        dpg.set_value("HomeAngle_4", dpg.get_value("J4input"))
        dpg.set_value("HomeAngle_5", dpg.get_value("J5input"))
        dpg.set_value("HomeAngle_6", dpg.get_value("J6input"))
        if dpg.get_value("StatePatron"):
            responce = requests.get("http://127.0.0.1:5000/Tool?id=PhisicPanel_1").text.split("|")
            requests.get(f"http://127.0.0.1:5000/Tool?id=PhisicPanel_1&conf=1|{responce[1]}")
        else:
            responce = requests.get("http://127.0.0.1:5000/Tool?id=PhisicPanel_1").text.split("|")
            requests.get(f"http://127.0.0.1:5000/Tool?id=PhisicPanel_1&conf=0|{responce[1]}")
        for j in range(1, 7):
            dpg.set_value(f"TabelAngle_{j}", eval(f"oldJ{j}angle"))
            requests.get((f"http://127.0.0.1:5000/CurentPosition?J1={oldJ1angle}&J2={oldJ2angle}&J3={oldJ3angle}&J4={oldJ4angle}&J5={oldJ5angle}&J6={oldJ6angle}"))

def AnglesControllSend():
    global oldJ1angle, oldJ2angle, oldJ3angle, oldJ4angle, oldJ5angle, oldJ6angle
    oldJ1angle = dpg.get_value("J1input")
    oldJ2angle = dpg.get_value("J2input")
    oldJ3angle = dpg.get_value("J3input")
    oldJ4angle = dpg.get_value("J4input")
    oldJ5angle = dpg.get_value("J5input")
    oldJ6angle = dpg.get_value("J6input")
    dpg.set_value("HomeAngle_1", dpg.get_value("J1input"))
    dpg.set_value("HomeAngle_2", dpg.get_value("J2input"))
    dpg.set_value("HomeAngle_3", dpg.get_value("J3input"))
    dpg.set_value("HomeAngle_4", dpg.get_value("J4input"))
    dpg.set_value("HomeAngle_5", dpg.get_value("J5input"))
    dpg.set_value("HomeAngle_6", dpg.get_value("J6input"))
    if dpg.get_value("StatePatron"):
        responce = requests.get("http://127.0.0.1:5000/Tool?id=PhisicPanel_1").text.split("|")
        requests.get(f"http://127.0.0.1:5000/Tool?id=PhisicPanel_1&conf=1|{responce[1]}")
    else:
        responce = requests.get("http://127.0.0.1:5000/Tool?id=PhisicPanel_1").text.split("|")
        requests.get(f"http://127.0.0.1:5000/Tool?id=PhisicPanel_1&conf=0|{responce[1]}")
    for j in range(1, 7):
        dpg.set_value(f"TabelAngle_{j}", eval(f"oldJ{j}angle"))
        requests.get((f"http://127.0.0.1:5000/CurentPosition?J1={oldJ1angle}&J2={oldJ2angle}&J3={oldJ3angle}&J4={oldJ4angle}&J5={oldJ5angle}&J6={oldJ6angle}"))


def UpdateAngleControll():
    newJ1angle = dpg.get_value("J1input")
    if newJ1angle > dpg.get_value("PosAngLim_1"):
        dpg.set_value("J1input", dpg.get_value("PosAngLim_1"))
    elif newJ1angle < dpg.get_value("NegAngLim_1"):
        dpg.set_value("J1input", dpg.get_value("NegAngLim_1"))
    newJ2angle = dpg.get_value("J2input")
    if newJ2angle > dpg.get_value("PosAngLim_2"):
        dpg.set_value("J2input", dpg.get_value("PosAngLim_2"))
    elif newJ2angle < dpg.get_value("NegAngLim_2"):
        dpg.set_value("J2input", dpg.get_value("NegAngLim_2"))
    newJ3angle = dpg.get_value("J3input")
    if newJ3angle > dpg.get_value("PosAngLim_3"):
        dpg.set_value("J3input", dpg.get_value("PosAngLim_3"))
    elif newJ3angle < dpg.get_value("NegAngLim_3"):
        dpg.set_value("J3input", dpg.get_value("NegAngLim_3"))
    newJ4angle = dpg.get_value("J4input")
    if newJ4angle > dpg.get_value("PosAngLim_4"):
        dpg.set_value("J4input", dpg.get_value("PosAngLim_4"))
    elif newJ4angle < dpg.get_value("NegAngLim_4"):
        dpg.set_value("J4input", dpg.get_value("NegAngLim_4"))
    newJ5angle = dpg.get_value("J5input")
    if newJ5angle > dpg.get_value("PosAngLim_5"):
        dpg.set_value("J5input", dpg.get_value("PosAngLim_5"))
    elif newJ5angle < dpg.get_value("NegAngLim_5"):
        dpg.set_value("J5input", dpg.get_value("NegAngLim_5"))
    newJ6angle = dpg.get_value("J6input")
    if newJ6angle > dpg.get_value("PosAngLim_6"):
        dpg.set_value("J6input", dpg.get_value("PosAngLim_6"))
    elif newJ6angle < dpg.get_value("NegAngLim_6"):
        dpg.set_value("J6input", dpg.get_value("NegAngLim_6"))

def UpdateAngleHome():
    newJ1angle = dpg.get_value("HomeAngle_1")
    if newJ1angle > dpg.get_value("PosAngLim_1"):
        dpg.set_value("HomeAngle_1", dpg.get_value("PosAngLim_1"))
    elif newJ1angle < dpg.get_value("NegAngLim_1"):
        dpg.set_value("HomeAngle_1", dpg.get_value("NegAngLim_1"))
    newJ2angle = dpg.get_value("HomeAngle_2")
    if newJ2angle > dpg.get_value("PosAngLim_2"):
        dpg.set_value("HomeAngle_2", dpg.get_value("PosAngLim_2"))
    elif newJ2angle < dpg.get_value("NegAngLim_2"):
        dpg.set_value("HomeAngle_2", dpg.get_value("NegAngLim_2"))
    newJ3angle = dpg.get_value("HomeAngle_3")
    if newJ3angle > dpg.get_value("PosAngLim_3"):
        dpg.set_value("HomeAngle_3", dpg.get_value("PosAngLim_3"))
    elif newJ3angle < dpg.get_value("NegAngLim_3"):
        dpg.set_value("HomeAngle_3", dpg.get_value("NegAngLim_3"))
    newJ4angle = dpg.get_value("HomeAngle_4")
    if newJ4angle > dpg.get_value("PosAngLim_4"):
        dpg.set_value("HomeAngle_4", dpg.get_value("PosAngLim_4"))
    elif newJ4angle < dpg.get_value("NegAngLim_4"):
        dpg.set_value("HomeAngle_4", dpg.get_value("NegAngLim_4"))
    newJ5angle = dpg.get_value("HomeAngle_5")
    if newJ5angle > dpg.get_value("PosAngLim_5"):
        dpg.set_value("HomeAngle_5", dpg.get_value("PosAngLim_5"))
    elif newJ5angle < dpg.get_value("NegAngLim_5"):
        dpg.set_value("HomeAngle_5", dpg.get_value("NegAngLim_5"))
    newJ6angle = dpg.get_value("HomeAngle_6")
    if newJ6angle > dpg.get_value("PosAngLim_6"):
        dpg.set_value("HomeAngle_6", dpg.get_value("PosAngLim_6"))
    elif newJ6angle < dpg.get_value("NegAngLim_6"):
        dpg.set_value("HomeAngle_6", dpg.get_value("NegAngLim_6"))

def GetStepAngle(sender):
    if sender == "StepAngle_1":
        dpg.configure_item("J1input", step= dpg.get_value(sender))
    elif sender == "StepAngle_2":
        dpg.configure_item("J2input", step= dpg.get_value(sender))
    elif sender == "StepAngle_3":
        dpg.configure_item("J3input", step= dpg.get_value(sender))
    elif sender == "StepAngle_4":
        dpg.configure_item("J4input", step= dpg.get_value(sender))
    elif sender == "StepAngle_5":
        dpg.configure_item("J5input", step= dpg.get_value(sender))
    elif sender == "StepAngle_6":
        dpg.configure_item("J6input", step= dpg.get_value(sender))

def GetStepAnglePos(sender):
    if sender == "StepPosAngLim_1":
        dpg.configure_item("PosAngLim_1", step= dpg.get_value(sender))
    elif sender == "StepPosAngLim_2":
        dpg.configure_item("PosAngLim_2", step= dpg.get_value(sender))
    elif sender == "StepPosAngLim_3":
        dpg.configure_item("PosAngLim_3", step= dpg.get_value(sender))
    elif sender == "StepPosAngLim_4":
        dpg.configure_item("PosAngLim_4", step= dpg.get_value(sender))
    elif sender == "StepPosAngLim_5":
        dpg.configure_item("PosAngLim_5", step= dpg.get_value(sender))
    elif sender == "StepPosAngLim_6":
        dpg.configure_item("PosAngLim_6", step= dpg.get_value(sender))

def GetStepAngleNeg(sender):
    if sender == "StepNegAngLim_1":
        dpg.configure_item("NegAngLim_1", step= dpg.get_value(sender))
    elif sender == "StepNegAngLim_2":
        dpg.configure_item("NegAngLim_2", step= dpg.get_value(sender))
    elif sender == "StepNegAngLim_3":
        dpg.configure_item("NegAngLim_3", step= dpg.get_value(sender))
    elif sender == "StepNegAngLim_4":
        dpg.configure_item("NegAngLim_4", step= dpg.get_value(sender))
    elif sender == "StepNegAngLim_5":
        dpg.configure_item("NegAngLim_5", step= dpg.get_value(sender))
    elif sender == "StepNegAngLim_6":
        dpg.configure_item("NegAngLim_6", step= dpg.get_value(sender))

def GetStepXYZ(sender):
    if sender == "Step_X":
        dpg.configure_item("X_input", step= dpg.get_value(sender))
    elif sender == "Step_Y":
        dpg.configure_item("Y_input", step= dpg.get_value(sender))
    elif sender == "Step_Z":
        dpg.configure_item("Z_input", step= dpg.get_value(sender))


def GetStepHome(sender):
    if sender == "StepHomeAngle_1":
        dpg.configure_item("HomeAngle_1", step= dpg.get_value(sender))
    elif sender == "StepHomeAngle_2":
        dpg.configure_item("HomeAngle_2", step= dpg.get_value(sender))
    elif sender == "StepHomeAngle_3":
        dpg.configure_item("HomeAngle_3", step= dpg.get_value(sender))
    elif sender == "StepHomeAngle_4":
        dpg.configure_item("HomeAngle_4", step= dpg.get_value(sender))
    elif sender == "StepHomeAngle_5":
        dpg.configure_item("HomeAngle_5", step= dpg.get_value(sender))
    elif sender == "StepHomeAngle_6":
        dpg.configure_item("HomeAngle_6", step= dpg.get_value(sender))

def GetStepSpeed(sender):
    if sender == "StepSpeedAngle_1":
        dpg.configure_item("SpeedAngle_1", step= dpg.get_value(sender))
    elif sender == "StepSpeedAngle_2":
        dpg.configure_item("SpeedAngle_2", step= dpg.get_value(sender))
    elif sender == "StepSpeedAngle_3":
        dpg.configure_item("SpeedAngle_3", step= dpg.get_value(sender))
    elif sender == "StepSpeedAngle_4":
        dpg.configure_item("SpeedAngle_4", step= dpg.get_value(sender))
    elif sender == "StepSpeedAngle_5":
        dpg.configure_item("HomeAngle_5", step= dpg.get_value(sender))
    elif sender == "StepSpeedAngle_6":
        dpg.configure_item("SpeedAngle_6", step= dpg.get_value(sender))

def SendXYZ():
    global X, Y, Z
    if dpg.get_value("StatePatron_2"):
        responce = requests.get("http://127.0.0.1:5000/Tool?id=PhisicPanel_1").text.split("|")
        requests.get(f"http://127.0.0.1:5000/Tool?id=PhisicPanel_1&conf=1|{responce[1]}")
    else:
        responce = requests.get("http://127.0.0.1:5000/Tool?id=PhisicPanel_1").text.split("|")
        requests.get(f"http://127.0.0.1:5000/Tool?id=PhisicPanel_1&conf=0|{responce[1]}")
    X = dpg.get_value("X_input")
    Y = dpg.get_value("Y_input")
    Z = dpg.get_value("Z_input")
    J1, J2, J3, J4, J5, J6, = kinematic.CalcRevKin(float(x), float(y), float(Z),-90,90,-90,"N", 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0)
    requests.get((f"http://127.0.0.1:5000/CurentPosition?J1={J1}&J2={J2}&J3={J3}&J4={J4}&J5={J5}&J6={J6}"))
    dpg.set_value("J1input", J1)
    dpg.set_value("J2input", J2)
    dpg.set_value("J3input", J3)
    dpg.set_value("J4input", J4)
    dpg.set_value("J5input", J5)
    dpg.set_value("J6input", J6)

def MoveHomeRobot():
    global oldJ1angle, oldJ2angle, oldJ3angle, oldJ4angle, oldJ5angle, oldJ6angle
    oldJ1angle = dpg.get_value("HomeAngle_1")
    oldJ2angle = dpg.get_value("HomeAngle_2")
    oldJ3angle = dpg.get_value("HomeAngle_3")
    oldJ4angle = dpg.get_value("HomeAngle_4")
    oldJ5angle = dpg.get_value("HomeAngle_5")
    oldJ6angle = dpg.get_value("HomeAngle_6")

    dpg.set_value("J1input", oldJ1angle)
    dpg.set_value("J2input", oldJ2angle)
    dpg.set_value("J3input", oldJ3angle)
    dpg.set_value("J4input", oldJ4angle)
    dpg.set_value("J5input", oldJ5angle)
    dpg.set_value("J6input", oldJ6angle)

    for j in range(1, 7):
        dpg.set_value(f"TabelAngle_{j}", eval(f"oldJ{j}angle"))
        requests.get((f"http://127.0.0.1:5000/CurentPosition?J1={oldJ1angle}&J2={oldJ2angle}&J3={oldJ3angle}&J4={oldJ4angle}&J5={oldJ5angle}&J6={oldJ6angle}"))

def ProgrammFromFile(sender, app_data):
    filePath = str(app_data["selections"][app_data["file_name"]])
    AddNewProgramm(label=str(app_data["file_name"]).replace(".url", ""))
    with open(filePath, "r") as file:
        allText = file.read()
        Prog =  (dpg.get_item_children(dpg.get_item_children("ProgrammTabs")[1][-1])[1][1])
        dpg.set_value(Prog, allText)

def AddNewProgramm(label):
    OpenProgrammInEditor()
    if len(dpg.get_item_children("ProgrammTabs")[1]) == 1:
        dpg.set_value("fileName", "untitle")
    with dpg.tab(label=label,closable=True, parent="ProgrammTabs"):
        with dpg.child_window(pos=[3,50], width=47, height=750, border=False):
            pass
        Text = dpg.add_input_text(multiline=True, on_enter=True, pos=[40,50], width=425, height=770, tab_input=True, tracked=True)
        dpg.bind_item_font(Text, font)
        

def StartProgramm():
    All_Programm = ""
    for child in range(0, len(dpg.get_item_children("ProgrammTabs")[1])):
        if child == 0:
            pass
        else:
            Prog =  (dpg.get_item_children(dpg.get_item_children("ProgrammTabs")[1][child])[1][1])
            if dpg.is_item_visible(Prog):
                Programm = str(dpg.get_value(Prog)).split("\n")
                c = 1
                for line in Programm:
                    if c == 1:
                        All_Programm += line
                        c = 0
                    else:
                        All_Programm += ("<br>" + line)
                    
                requests.get(f"http://127.0.0.1:5000/ProgrammPosition?Programm={All_Programm.replace('#', '^').replace('/', '$').replace('&', '!')}")

def SaveProgramm(sender, app_data):
    filePath = str(app_data['current_path'])
    fileName = dpg.get_item_label(int(dpg.get_item_children("ProgrammTabs")[1][1]))
    file = filePath + "\\" + fileName + ".url"
    with open(file, "w+") as file:
        for child in range(0, len(dpg.get_item_children("ProgrammTabs")[1])):
            if child == 0:
                pass
            else:
                Prog =  (dpg.get_item_children(dpg.get_item_children("ProgrammTabs")[1][child])[1][1])
                if dpg.is_item_visible(Prog):
                    text = dpg.get_value(Prog)
                    file.write(text)


def OpenFileSave():
    dpg.show_item("Directory_dialog")

def AddCommandToText(command):
    for child in range(0, len(dpg.get_item_children("ProgrammTabs")[1])):
        if child == 0:
            pass
        else:
            Prog = (dpg.get_item_children(dpg.get_item_children("ProgrammTabs")[1][child])[1][1])
            if dpg.is_item_visible(Prog):
                val = dpg.get_value(Prog)
                if val == "":
                    text = val + command
                    dpg.set_value(Prog, text)
                else:
                    text = val + "\n" + command
                    dpg.set_value(Prog, text)

def AddPTP():
    command = f"[{oldJ1angle}, {oldJ2angle}, {oldJ3angle}, {oldJ4angle}, {oldJ5angle}, {oldJ6angle}]"
    AddCommandToText(command)

def SetTimeOut():
    time = str(dpg.get_value("AddTime"))
    if dpg.get_value("AddTime") != 0:
        AddCommandToText("Time " + time)

def SetFileName(sender):
    name = dpg.get_value(sender)
    for child in range(0, len(dpg.get_item_children("ProgrammTabs")[1])):
        if child == 0:
            pass
        else:
            Prog = (dpg.get_item_children(dpg.get_item_children("ProgrammTabs")[1][child])[1][1])
            if dpg.is_item_visible(Prog):
                dpg.set_item_label(dpg.get_item_children("ProgrammTabs")[1][child], name)

def ChangeCommandEdit(sender):
    CurCommand = dpg.get_value(sender)
    for i in dpg.get_item_children("All_commands")[1]:
        if i == dpg.get_item_children("All_commands")[1][0] or i == dpg.get_item_children("All_commands")[1][1]:
            pass
        else:
            dpg.hide_item(i)
    dpg.show_item(CurCommand)

def SetLineCommand():
    LJ1 = dpg.get_value("Lin_J0")
    LJ2 = dpg.get_value("Lin_J1")
    LJ3 = dpg.get_value("Lin_J2")
    LJ4 = dpg.get_value("Lin_J3")
    LJ5 = dpg.get_value("Lin_J4")
    LJ6 = dpg.get_value("Lin_J5")
    dpg.set_value("Line_com", f"LIN[{LJ1}, {LJ2}, {LJ3}, {LJ4}, {LJ5}, {LJ6}]")

def SetPtpCommand():
    LJ1 = dpg.get_value("Ptp_J0")
    LJ2 = dpg.get_value("Ptp_J1")
    LJ3 = dpg.get_value("Ptp_J2")
    LJ4 = dpg.get_value("Ptp_J3")
    LJ5 = dpg.get_value("Ptp_J4")
    LJ6 = dpg.get_value("Ptp_J5")
    dpg.set_value("Ptp_com", f"[{LJ1}, {LJ2}, {LJ3}, {LJ4}, {LJ5}, {LJ6}]")

def SetSpeedCommand():
    LJ1 = dpg.get_value("Speed_J0")
    LJ2 = dpg.get_value("Speed_J1")
    LJ3 = dpg.get_value("Speed_J2")
    LJ4 = dpg.get_value("Speed_J3")
    LJ5 = dpg.get_value("Speed_J4")
    LJ6 = dpg.get_value("Speed_J5")
    dpg.set_value("Speed_com", f"SPEED[{LJ1}, {LJ2}, {LJ3}, {LJ4}, {LJ5}, {LJ6}]")

def SetCircCommand():
    x = dpg.get_value("Circ_J0")
    y = dpg.get_value("Circ_J1")
    z = dpg.get_value("Circ_J2")
    dpg.set_value("XYZ_com", f"CIRC[{x}, {y}, {z}]")

def GetLogs():
    global old_log
    responce = requests.get("http://127.0.0.1:5000/Logs").text
    if old_log != responce:
        type = responce.split()[1]
        Message = responce.split()[2:]
        if type == "[DEBUG]":
            log_panel.log_debug(" ".join(Message))
        elif type == "[ERROR]":
            log_panel.log_error(" ".join(Message))
        elif type == "[INFO]":
            log_panel.log_info(" ".join(Message))
        old_log = responce

def GetStartLog():
    global old_log
    responce = requests.get(f"http://127.0.0.1:5000/Logs?M=true").text.split("<br>")
    for i in responce:
        type = i.split()[1]
        Message = i.split()[2:]
        if type == "[DEBUG]":
            log_panel.log_debug(" ".join(Message))
        elif type == "[ERROR]":
            log_panel.log_error(" ".join(Message))
        elif type == "[INFO]":
            log_panel.log_info(" ".join(Message))

    old_log = requests.get("http://127.0.0.1:5000/Logs").text

def GetConfigPanel():
    responce = requests.get("http://127.0.0.1:5000/Tool?id=PhisicPanel_1").text.split("|")
    try:
        if responce[0] == "1":
            dpg.hide_item("Image_1")
            dpg.show_item("Image_4")
        else:
            dpg.hide_item("Image_4")
            dpg.show_item("Image_1")

        if responce[1] == "1":
            dpg.hide_item("Image_2")
            dpg.show_item("Image_5")
        else:
            dpg.hide_item("Image_5")
            dpg.show_item("Image_2")

        responce = requests.get("http://127.0.0.1:5000/Tool?id=EmButton").text
        if responce == "1":
            dpg.hide_item("Image_0")
            dpg.show_item("Image_3")
        else:
            dpg.hide_item("Image_3")
            dpg.show_item("Image_0")

    except:pass

def ReplaicePTPhome():
    global oldJ1angle,oldJ2angle,oldJ3angle,oldJ4angle,oldJ5angle,oldJ6angle

    J1NaL = variable.J1Min
    J2NaL = variable.J2Min
    J3NaL = variable.J3Min
    J4NaL = variable.J4Min
    J5NaL = variable.J5Min
    J6NaL = variable.J6Min
    J1PaL = variable.J1Max
    J2PaL = variable.J2Max
    J3PaL = variable.J3Max
    J4PaL = variable.J4Max
    J5PaL = variable.J5Max
    J6PaL = variable.J6Max


    filename = "variable.py"
    with open(filename, "w") as f:
        f.write(f'oldJ1angle = {dpg.get_value("HomeAngle_1")}\n')
        f.write(f'oldJ2angle = {dpg.get_value("HomeAngle_2")}\n')
        f.write(f'oldJ3angle = {dpg.get_value("HomeAngle_3")}\n')
        f.write(f'oldJ4angle = {dpg.get_value("HomeAngle_4")}\n')
        f.write(f'oldJ5angle = {dpg.get_value("HomeAngle_5")}\n')
        f.write(f'oldJ6angle = {dpg.get_value("HomeAngle_6")}\n')
        f.write(f'\n')
        f.write(f'J1Max = "{J1PaL}"\n')
        f.write(f'J2Max = "{J2PaL}"\n')
        f.write(f'J3Max = "{J3PaL}"\n')
        f.write(f'J4Max = "{J4PaL}"\n')
        f.write(f'J5Max = "{J5PaL}"\n')
        f.write(f'J6Max = "{J6PaL}"\n')
        f.write(f'J1Min = "{J1NaL}"\n')
        f.write(f'J2Min = "{J2NaL}"\n')
        f.write(f'J3Min = "{J3NaL}"\n')
        f.write(f'J4Min = "{J4NaL}"\n')
        f.write(f'J5Min = "{J5NaL}"\n')
        f.write(f'J6Min = "{J6NaL}"\n')
        f.write(f'\n')

def SetSpeed():
    j1 = dpg.get_value("SpeedAngle_1")
    j2 = dpg.get_value("SpeedAngle_2")
    j3 = dpg.get_value("SpeedAngle_3")
    j4 = dpg.get_value("SpeedAngle_4")
    j5 = dpg.get_value("SpeedAngle_5")
    j6 = dpg.get_value("SpeedAngle_6")
    requests.get(f"http://127.0.0.1:5000/StandartSpeed?J1={j1}&J3={j2}&J2={j3}&J4={j4}&J5={j5}&J6={j6}")

def AddDataSimplePlot():
    for j in range(0, 6):
        LIST = dpg.get_value(f"load_{j+1}")
        resp = requests.get("http://127.0.0.1:5000/Tool?id=MotorLoads").text.split("|")
        LIST.append(int(resp[j]))
        dpg.set_value(f"load_{j+1}", LIST)
        angle = dpg.get_value("CurAngForPlot")
        if angle == f"J{j+1}":
            dpg.set_value("CurAngForPlot", "J6")
            dpg.set_value("CentralPlot", dpg.get_value("load_6"))
        if angle == f"J{j+1}":
            dpg.set_value("CurAngForPlot", "J5")
            dpg.set_value("CentralPlot", dpg.get_value("load_5"))
        if angle == f"J{j+1}":
            dpg.set_value("CurAngForPlot", "J4")
            dpg.set_value("CentralPlot", dpg.get_value("load_4"))
        if angle == f"J{j+1}":
            dpg.set_value("CurAngForPlot", "J3")
            dpg.set_value("CentralPlot", dpg.get_value("load_3"))
        if angle == f"J{j+1}":
            dpg.set_value("CurAngForPlot", "J2")
            dpg.set_value("CentralPlot", dpg.get_value("load_2"))
        if angle == f"J{j+1}":
            dpg.set_value("CurAngForPlot", "J1")
            dpg.set_value("CentralPlot", dpg.get_value("load_1"))

dpg.create_context()
dpg.create_viewport(title='Custom Title',width=1100, height=2000,x_pos=0,y_pos=0, resizable=False)
dpg.setup_dearpygui()

requests.get("http://127.0.0.1:5000/CreateTool?id=PhisicPanel_1")
requests.get("http://127.0.0.1:5000/Tool?id=PhisicPanel_1&conf=0|0")

big_let_start = 0x00C0  # Capital "A" in cyrillic alphabet
big_let_end = 0x00DF  # Capital "Я" in cyrillic alphabet
small_let_end = 0x00FF  # small "я" in cyrillic alphabet
remap_big_let = 0x0410  # Starting number for remapped cyrillic alphabet
alph_len = big_let_end - big_let_start + 1  # adds the shift from big letters to small
alph_shift = remap_big_let - big_let_start  # adds the shift from remapped to non-remapped
with dpg.font_registry():
    font = dpg.add_font("123.ttf", 20)
    fontImage = dpg.add_font("8.ttf", 9)
    with dpg.font("Museo.otf", 13) as default_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        biglet = remap_big_let  # Starting number for remapped cyrillic alphabet
        for i1 in range(big_let_start, big_let_end + 1):  # Cycle through big letters in cyrillic alphabet
            dpg.add_char_remap(i1, biglet)  # Remap the big cyrillic letter
            dpg.add_char_remap(i1 + alph_len, biglet + alph_len)  # Remap the small cyrillic letter
            biglet += 1  # choose next letter
        dpg.bind_font(default_font)

Images = ["EmStop.png", "Lazer.png", "start.png","EmStopPressed.png", "LazerPressed.png", "startPressed.png"]
for i in Images:
    with dpg.texture_registry():
        width, height, channels, data = dpg.load_image(f'Images/{i}') # 0: width, 1: height, 2: channels, 3: data
        dpg.add_static_texture(width, height, data, tag=f"image_{Images.index(i)}")

with dpg.file_dialog(directory_selector=False, show=False, id="file_dialog_id", width=700 ,height=400, callback=ProgrammFromFile):
    dpg.add_file_extension(".url", color=(0, 255, 0, 255), custom_text="[URL]")

dpg.add_file_dialog(directory_selector=True, show=False, tag="Directory_dialog", width=700 ,height=400, callback=SaveProgramm)

with dpg.window(label="Программный редактор",width= 610,height=430,no_collapse=True, no_move=True, no_close=True, no_resize=True):
    with dpg.menu_bar():
        dpg.add_button(label="Создать", callback=lambda: AddNewProgramm(label="untitle"))
        dpg.add_button(label="Открыть", callback=lambda: dpg.show_item("file_dialog_id"))
        dpg.add_button(label="Сохранить", callback=OpenFileSave)
        # dpg.add_button(label="Save as", callback=dpg.show_item_registry)
        
    with dpg.child_window(border=False, tag="NoProgramm"):
        dpg.add_text("Ни одна программа не открыта", pos=[199, 150])

    with dpg.child_window(border=False, tag="Programm"):
        dpg.add_button(label="Запуск программы",pos=[5, 10],height=35, width=200, tag="Start", callback=StartProgramm)
        dpg.add_button(label="Остановить программу",pos=[390, 10],height=35, width=200, tag="Close", callback=lambda: requests.get("http://127.0.0.1:5000/DeleteProgramm"))
        dpg.add_button(label="Добавить точку PTP",pos=[5, 55],height=35, width=200, tag="AddPTP",callback=AddPTP)
        dpg.add_text(default_value="Название файла", pos=[253, 5])
        dpg.add_input_text(tag="fileName", pos=[215, 25], hint="untitle", width=165, callback=SetFileName)
        dpg.add_input_int(pos=[215, 71], width=165, tag="AddTime", min_value=0, max_value=9999, min_clamped=True, max_clamped=True)
        dpg.add_button(label="Установить паузу",pos=[390, 55],height=35, width=200, tag="ConfirmTime", callback=SetTimeOut)
        with dpg.child_window(width= 586,height=279, pos=[5, 97], border=False, tag="All_commands"):
            dpg.add_text(pos=[35, 15],default_value="Выберите действие:")
            dpg.add_listbox(items=['LIN','CIRC','SPEED', 'PTP', 'Init block', 'Call block', 'While', 'Debug', 'Time-out', 'Get'], pos=[0, 40], width=175, num_items=13, tag="Editor_commands", callback=ChangeCommandEdit)
            with dpg.child_window(pos=[185,40], height=232, width=401, tag="LIN", show=True, border=False):
                x, y = 25,10
                for i in range(3):
                    dpg.add_text(default_value=f"J{i+1}", pos=[x,y])
                    x+= 120
                x, y = 25,50
                for i in range(3):
                    dpg.add_text(default_value=f"J{3+i+1}", pos=[x,y])
                    x+= 120
                x, y = 25,30
                for i in range(3):
                    dpg.add_input_float(pos=[x,y], width=110, tag=f"Lin_J{i}", callback=SetLineCommand)
                    x+= 120
                x, y = 25,70
                for i in range(3):
                    dpg.add_input_float(pos=[x,y], width=110,tag=f"Lin_J{3+i}", callback=SetLineCommand)
                    x+= 120
                dpg.add_input_text(default_value="LIN[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]", pos=[25, 100], width=350, tag="Line_com", readonly=True)
                dpg.add_button(label="Копировать", pos=[265,130], width=110, callback=lambda: pyperclip.copy(dpg.get_value("Line_com")))
                dpg.add_button(label="Переместить в программу", pos=[100,130], width=155, callback=lambda: AddCommandToText(dpg.get_value("Line_com")))

            with dpg.child_window(pos=[185,40], height=232, width=401, tag="CIRC", show=False, border=False):
                x, y = 25,10
                for i in range(3):
                    if i == 0:
                        dpg.add_text(default_value="X", pos=[x,y])
                    if i == 1:
                        dpg.add_text(default_value="Y", pos=[x,y])
                    if i == 2:
                        dpg.add_text(default_value="Z", pos=[x,y])
                    x+= 120
                x, y = 25,30
                for i in range(3):
                    dpg.add_input_float(pos=[x,y], width=110, tag=f"Circ_J{i}", callback=SetCircCommand)
                    x+= 120
                dpg.add_input_text(default_value="CIRC[0.0, 0.0, 0.0]", pos=[25, 60], width=350, tag="XYZ_com", readonly=True)
                dpg.add_button(label="Копировать", pos=[265,90], width=110, callback=lambda: pyperclip.copy(dpg.get_value("XYZ_com")))
                dpg.add_button(label="Переместить в программу", pos=[100,90], width=155, callback=lambda: AddCommandToText(dpg.get_value("XYZ_com")))

            with dpg.child_window(pos=[185,40], height=232, width=401, tag="SPEED", show=False, border=False):
                x, y = 25,10
                for i in range(3):
                    dpg.add_text(default_value=f"J{i+1}", pos=[x,y])
                    x+= 120
                x, y = 25,50
                for i in range(3):
                    dpg.add_text(default_value=f"J{3+i+1}", pos=[x,y])
                    x+= 120
                x, y = 25,30
                for i in range(3):
                    dpg.add_input_float(pos=[x,y], width=110, tag=f"Speed_J{i}", callback=SetSpeedCommand)
                    x+= 120
                x, y = 25,70
                for i in range(3):
                    dpg.add_input_float(pos=[x,y], width=110,tag=f"Speed_J{3+i}", callback=SetSpeedCommand)
                    x+= 120
                dpg.add_input_text(default_value="SPEED[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]", pos=[25, 100], width=350, tag="Speed_com", readonly=True)
                dpg.add_button(label="Копировать", pos=[265,130], width=110, callback=lambda: pyperclip.copy(dpg.get_value("Speed_com")))
                dpg.add_button(label="Переместить в программу", pos=[100,130], width=155, callback=lambda: AddCommandToText(dpg.get_value("Speed_com")))

            with dpg.child_window(pos=[185,40], height=232, width=401, tag="PTP", show=False, border=False):
                x, y = 25,10
                for i in range(3):
                    dpg.add_text(default_value=f"J{i+1}", pos=[x,y])
                    x+= 120
                x, y = 25,50
                for i in range(3):
                    dpg.add_text(default_value=f"J{3+i+1}", pos=[x,y])
                    x+= 120
                x, y = 25,30
                for i in range(3):
                    dpg.add_input_float(pos=[x,y], width=110, tag=f"Ptp_J{i}", callback=SetPtpCommand)
                    x+= 120
                x, y = 25,70
                for i in range(3):
                    dpg.add_input_float(pos=[x,y], width=110,tag=f"Ptp_J{3+i}", callback=SetPtpCommand)
                    x+= 120
                dpg.add_input_text(default_value="[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]", pos=[25, 100], width=350, tag="Ptp_com", readonly=True)
                dpg.add_button(label="Копировать", pos=[265,130], width=110, callback=lambda: pyperclip.copy(dpg.get_value("Ptp_com")))
                dpg.add_button(label="Переместить в программу", pos=[100,130], width=155, callback=lambda: AddCommandToText(dpg.get_value("Ptp_com")))

            with dpg.child_window(pos=[185,40], height=232, width=401, tag="Init block", show=False, border=False):
                dpg.add_input_text(tag="Init", default_value="1", pos=[25, 20], width=350,height=100, multiline=True, callback=lambda: dpg.set_value("Init_com", "=" + dpg.get_value("Init") + "="))
                dpg.add_input_text(default_value="=1=", pos=[25, 130], width=350, readonly=True, tag="Init_com")
                dpg.add_button(label="Копировать", pos=[265,160], width=110, callback=lambda: pyperclip.copy(dpg.get_value("Init_com")))
                dpg.add_button(label="Переместить в программу", pos=[100,160], width=155, callback=lambda: AddCommandToText(dpg.get_value("Init_com")))

            with dpg.child_window(pos=[185,40], height=232, width=401, tag="Call block", show=False, border=False):
                dpg.add_input_text(tag="Call", default_value="1", pos=[25, 20], width=350,height=100, multiline=True, callback=lambda: dpg.set_value("Call_com", "@_" + dpg.get_value("Call")))
                dpg.add_input_text(default_value="@_1", pos=[25, 130], width=350, readonly=True, tag="Call_com")
                dpg.add_button(label="Копировать", pos=[265,160], width=110, callback=lambda: pyperclip.copy(dpg.get_value("Call_com")))
                dpg.add_button(label="Переместить в программу", pos=[100,160], width=155, callback=lambda: AddCommandToText(dpg.get_value("Call_com")))

            with dpg.child_window(pos=[185,40], height=232, width=401, tag="While", show=False, border=False):
                dpg.add_input_text(tag="WhileI", default_value="1", pos=[25, 20], width=350,height=100, multiline=True, no_spaces=True, decimal=True, callback=lambda: dpg.set_value("While_com", "While(" + dpg.get_value("WhileI") + ")" if dpg.get_value("WhileI") != "" and dpg.get_value("WhileI") != "0" else "While(1)"))
                dpg.add_input_text(default_value="While(1)", pos=[25, 130], width=350, readonly=True, tag="While_com")
                dpg.add_button(label="Копировать", pos=[265,160], width=110, callback=lambda: pyperclip.copy(dpg.get_value("While_com")))
                dpg.add_button(label="Переместить в программу", pos=[100,160], width=155, callback=lambda: AddCommandToText(dpg.get_value("While_com")))

            with dpg.child_window(pos=[185,40], height=232, width=401, tag="Debug", show=False, border=False):
                dpg.add_input_text(tag="Debug_mes",default_value="Test debug message", pos=[25, 20], width=350,height=100, multiline=True, callback=lambda: dpg.set_value("Debug_com", "Debug(" + dpg.get_value("Debug_mes") + ")"))
                dpg.add_input_text(default_value="Debug(Test debug message)", pos=[25, 130], width=350, readonly=True, tag="Debug_com")
                dpg.add_button(label="Копировать", pos=[265,160], width=110, callback=lambda: pyperclip.copy(dpg.get_value("Debug_com")))
                dpg.add_button(label="Переместить в программу", pos=[100,160], width=155, callback=lambda: AddCommandToText(dpg.get_value("Debug_com")))

            with dpg.child_window(pos=[185,40], height=232, width=401, tag="Time-out", show=False, border=False):
                dpg.add_input_text(tag="TimeS",default_value="1", pos=[25, 20], width=350,height=100, multiline=True, no_spaces=True, decimal=True, callback=lambda: dpg.set_value("Time_com", "Time " + dpg.get_value("TimeS") if dpg.get_value("TimeS") != "" and dpg.get_value("TimeS") != "0" else "Time 1"))
                dpg.add_input_text(default_value="Time 1", pos=[25, 130], width=350, readonly=True, tag="Time_com")
                dpg.add_button(label="Копировать", pos=[265,160], width=110, callback=lambda: pyperclip.copy(dpg.get_value("Time_com")))
                dpg.add_button(label="Переместить в программу", pos=[100,160], width=155, callback=lambda: AddCommandToText(dpg.get_value("Time_com")))

            with dpg.child_window(pos=[185,40], height=232, width=401, tag="Get", show=False, border=False):
                dpg.add_input_text(tag="GetCom",default_value="http://127.0.0.1:5000/Tool?id=PhisicPanel_1&conf=0|0", pos=[25, 20], width=350,height=100, multiline=True, callback=lambda: dpg.set_value("Get_com", "get(" + dpg.get_value("GetCom") + ")"))
                dpg.add_input_text(default_value="get(http://127.0.0.1:5000/Tool?id=PhisicPanel_1&conf=0|0)", pos=[25, 130], width=350, readonly=True, tag="Get_com")
                dpg.add_button(label="Копировать", pos=[265,160], width=110, callback=lambda: pyperclip.copy(dpg.get_value("Get_com")))
                dpg.add_button(label="Переместить в программу", pos=[100,160], width=155, callback=lambda: AddCommandToText(dpg.get_value("Get_com")))

    StartProgrammEditor()
        
        
    
with dpg.window(label="Программа",width= 470,height=828, pos=[610,0],no_collapse=True, no_move=True, no_close=True, no_resize=True):
    with dpg.tab_bar(label="tabs", tag="ProgrammTabs", reorderable=True):
        dpg.add_tab_button(label="+", trailing=True, callback=lambda:AddNewProgramm(label="untitle"))
        

with dpg.window(label="Визуализация",width= 1080,height=440, pos=[0,827],no_collapse=True, no_move=True, no_close=True, no_resize=True, no_title_bar=True):
    dpg.add_text(default_value="3D", pos=[1020, 10])
    dpg.add_button(label="Убрать", width=80, pos=[990, 30],callback=lambda: minimize_window(window_handle))
    dpg.add_button(label="Показать", width=80, pos=[990, 55],callback=lambda: maximize_window(window_handle))

    dpg.add_text(default_value="Клавиатура", pos=[999, 80])
    dpg.add_button(label="Убрать", width=80, pos=[990, 100],callback=lambda: os.system("taskkill /im osk.exe"))
    dpg.add_button(label="Показать", width=80, pos=[990, 125],callback=lambda: subprocess.Popen("osk.exe", shell=True))
# 1267
with dpg.window(label="Управление",width= 1080,height=653, pos=[0,1267],no_collapse=True, tag="Controll", no_move=True, no_close=True, no_resize=True):
    with dpg.menu_bar():
        dpg.add_button(label="Управление углами", callback=OpenAngleControll)
        dpg.add_button(label="Управление по XYZ", callback=OpenXYZControll)
        dpg.add_button(label="Управление скоростью", callback=OpenSpeedControll)
        dpg.add_button(label="Калибровка", callback=OpenCalibrationControll)
        dpg.add_button(label="Домашняя позиция", callback=OpenHomePosition)
        

    with dpg.child_window(border=False, tag="AngleControl", pos=[0,32], width=1310, height=610):
        dpg.add_text(pos=[155,20], default_value="J1")
        dpg.add_input_float(width=160, pos=[75, 40], default_value=oldJ1angle, tag="J1input", callback=AnglesControll, step=1)
        dpg.add_drag_float(width=160, pos=[75, 65],speed=0.001,min_value=0, tag="StepAngle_1", callback=GetStepAngle,default_value=1)
        dpg.add_text(pos=[335,20], default_value="J2")
        dpg.add_input_float(width=160, pos=[255, 40], default_value=oldJ2angle, tag="J2input", callback=AnglesControll, step=1)
        dpg.add_drag_float(width=160, pos=[255, 65],speed=0.001,min_value=0, tag="StepAngle_2", callback=GetStepAngle,default_value=1)
        dpg.add_text(pos=[515,20], default_value="J3")
        dpg.add_input_float(width=160, pos=[435, 40], default_value=oldJ3angle, tag="J3input", callback=AnglesControll, step=1)
        dpg.add_drag_float(width=160, pos=[435, 65],speed=0.001,min_value=0, tag="StepAngle_3", callback=GetStepAngle,default_value=1)

        dpg.add_text(pos=[155,120], default_value="J4")
        dpg.add_input_float(width=160, pos=[75, 140], default_value=oldJ4angle, tag="J4input", callback=AnglesControll, step=1)
        dpg.add_drag_float(width=160, pos=[75, 165],speed=0.001,min_value=0, tag="StepAngle_4", callback=GetStepAngle,default_value=1)
        dpg.add_text(pos=[335,120], default_value="J5")
        dpg.add_input_float(width=160, pos=[255, 140], default_value=oldJ5angle, tag="J5input", callback=AnglesControll, step=1)
        dpg.add_drag_float(width=160, pos=[255, 165],speed=0.001,min_value=0, tag="StepAngle_5", callback=GetStepAngle,default_value=1)
        dpg.add_text(pos=[515,120], default_value="J6")
        dpg.add_input_float(width=160, pos=[435, 140], default_value=oldJ6angle, tag="J6input", callback=AnglesControll, step=1)
        dpg.add_drag_float(width=160, pos=[435, 165],speed=0.001,min_value=0, tag="StepAngle_6", callback=GetStepAngle, default_value=1)
        dpg.add_checkbox(label="Авто отправка", pos=[435,205], callback=changeSendData, tag="AutoSendAngels")
        dpg.add_checkbox(label="Patron", callback=AnglesControll, pos=[255,205], tag="StatePatron")
        dpg.add_button(label="Отправить данные", pos=[435, 230], width=160, height=30, tag="send_Button", callback=AnglesControllSend)
        with dpg.child_window(pos=[5,300], width=660, border=False):
            with dpg.table(header_row=True, width=660, pos=[0,0]):
                dpg.add_table_column(label="Информация")
                dpg.add_table_column(label="J1")
                dpg.add_table_column(label="J2")
                dpg.add_table_column(label="J3")
                dpg.add_table_column(label="J4")
                dpg.add_table_column(label="J5")
                dpg.add_table_column(label="J6")
                dpg.add_table_row()
                with dpg.table_row():
                    dpg.add_text(f"Позиция")
                    for j in range(1, 7):
                            dpg.add_text(eval(f"float(variable.oldJ{j}angle)"), tag=f"TabelAngle_{j}")
                with dpg.table_row():            
                    dpg.add_text("Нагрузка")
                    for j in range(0, 6):
                        resp = requests.get("http://127.0.0.1:5000/Tool?id=MotorLoads").text.split("|")
                        dpg.add_simple_plot(default_value=[int(resp[j])], height=30, width=96, tracked=True, tag=f"load_{j+1}")
            with dpg.child_window(pos=[10,115], width=655, border=False):
                dpg.add_button(label="<", callback=hep, tag="<")
                dpg.add_text(default_value="J1", pos=[25,0], tag="CurAngForPlot")
                dpg.add_button(label=">", pos=[50, 0], callback=hep, tag=">")
                dpg.add_simple_plot(width=645, height=166, default_value=dpg.get_value("load_1"), tag="CentralPlot")


        with dpg.plot(label="Сервомоторы робота", height=594, width=642 - 240, pos=[670,10], no_mouse_pos=True):
                dpg.add_plot_legend(location=50)
                dpg.add_plot_axis(dpg.mvXAxis)
                with dpg.plot_axis(dpg.mvYAxis, log_scale=False):
                    with dpg.custom_series(x_data, y_data, 2, callback=AnglePlot, tag="demo_custom_series", ):
                        dpg.add_text("Current Point: ", tag="custom_series_text")
                    dpg.fit_axis_data(dpg.top_container_stack())
    
    
    with dpg.child_window(border=False, tag="XYZControl", pos=[0,32], width=1310, height=610):
        with dpg.child_window(pos=[560, 110], height=580, width=580, border=False):
            dpg.add_3d_slider(pos=[5,35], callback=GetXYZ_Point, tag="XYZ_slider", max_x=2000, max_y=2000, max_z=2000, min_x=-2000, min_y=-2000, min_z=-2000)

        dpg.add_text(pos=[135,40], default_value="X")
        dpg.add_input_float(width=160, pos=[55, 60], tag="X_input", callback=SetXYZ_Point, step=1)
        dpg.add_drag_float(width=160, pos=[55, 85],speed=0.001,min_value=0, tag="Step_X", callback=GetStepXYZ, default_value=1)
        dpg.add_text(pos=[315,40], default_value="Y")
        dpg.add_input_float(width=160, pos=[235, 60], tag="Y_input", callback=SetXYZ_Point, step=1)
        dpg.add_drag_float(width=160, pos=[235, 85],speed=0.001,min_value=0, tag="Step_Y", callback=GetStepXYZ, default_value=1)
        dpg.add_text(pos=[495,40], default_value="Z")
        dpg.add_input_float(width=160, pos=[415, 60], tag="Z_input", callback=SetXYZ_Point, step=1)
        dpg.add_drag_float(width=160, pos=[415, 85],speed=0.001,min_value=0, tag="Step_Z", callback=GetStepXYZ, default_value=1)
        dpg.add_checkbox(label="Авто отправка", pos=[55,110], callback=changeSendDataXYZ, tag="AutoSendXYZ")
        dpg.add_checkbox(label="Patron", callback=SetXYZ_Point, pos=[235,110], tag="StatePatron_2")
        dpg.add_button(label="Отправить данные", pos=[55, 135], width=160, height=30, tag="XYZ_send_Button", callback=SendXYZ)

    with dpg.child_window(border=False, tag="Calibration", pos=[0,32], width=1310, height=610):
        x=15;y=15
        for i in range(1,7):
            dpg.add_text(f"PosAngLim_{i}", pos=[x, y])
            dpg.add_text(f"NegAngLim_{i}", pos=[x, y + 25])
            y+=65
        
        x=100;y=15
        for i in range(1,7):
            dpg.add_input_float(pos=[x, y], width=200, tag=f"PosAngLim_{i}", step=1, default_value=int(eval(f"variable.J{i}Max")))
            dpg.add_input_float(pos=[x, y + 25], width=200, tag=f"NegAngLim_{i}", step=1, default_value=int(eval(f"variable.J{i}Min")))
            y+=65
        
        x=310;y=15
        for i in range(1,7):
            dpg.add_drag_float(pos=[x, y], width=200, tag=f"StepPosAngLim_{i}", speed=0.001, callback=GetStepAnglePos, default_value=1)
            dpg.add_drag_float(pos=[x, y + 25], width=200, tag=f"StepNegAngLim_{i}", speed=0.001, callback=GetStepAngleNeg, default_value=1)
            with dpg.tooltip(parent=f"StepPosAngLim_{i}"):
                dpg.add_text(f"Step PosAngLim_{i} input")
            with dpg.tooltip(parent=f"StepNegAngLim_{i}"):
                dpg.add_text(f"Step NegAngLim_{i} input")
            y+=65
        
        x=130;y=430
        for i in range(1,7):
            if i == 1:
                dpg.add_text("X", pos=[x+45, y - 25])
            elif i == 2:
                dpg.add_text("Y", pos=[x+45, y - 25])
            elif i == 3:
                dpg.add_text("Z", pos=[x+45, y - 25])
            elif i == 4:
                dpg.add_text("Rx", pos=[x+45, y - 25])
            elif i == 5:
                dpg.add_text("Ry", pos=[x+45, y - 25])
            elif i == 6:
                dpg.add_text("Rz", pos=[x+45, y - 25])

            dpg.add_input_int(pos=[x, y], width= 100, tag=f"Work_frame_{i}")
            dpg.add_input_int(pos=[x, y+25], width= 100, tag=f"Tool_frame_{i}")
            dpg.add_input_int(pos=[x, y+50], width= 100, tag=f"Curent_Position_{i}")
            x+=110
        
        dpg.add_text("Work frame", pos=[50, 430])
        dpg.add_text("Tool frame", pos=[50, 430+25])
        dpg.add_text("Curent position", pos=[15, 430+50])
        
    
    
    with dpg.child_window(border=False, tag="SpeedControll", pos=[0,32], width=1310, height=610):
        Image = dpg.add_text(speedImage, pos= [100, 30])
        dpg.bind_item_font(Image, fontImage)
        with dpg.child_window(border=False, pos=[380,200], width=650, height=300):
            dpg.add_text(pos=[155,20], default_value="J1")
            dpg.add_input_float(width=160, pos=[75, 40], tag="SpeedAngle_1", default_value=1, step=1)
            dpg.add_drag_float(width=160, pos=[75, 65],speed=0.001, min_value=0, default_value=1, callback=GetStepSpeed, tag="StepSpeedAngle_1")
            dpg.add_text(pos=[335,20], default_value="J2")
            dpg.add_input_float(width=160, pos=[255, 40], tag="SpeedAngle_2", default_value=1, step=1)
            dpg.add_drag_float(width=160, pos=[255, 65],speed=0.001, min_value=0, default_value=1, callback=GetStepSpeed, tag="StepSpeedAngle_2")
            dpg.add_text(pos=[515,20], default_value="J3")
            dpg.add_input_float(width=160, pos=[435, 40], tag="SpeedAngle_3", default_value=1, step=1)
            dpg.add_drag_float(width=160, pos=[435, 65],speed=0.001, min_value=0, default_value=1, callback=GetStepSpeed, tag="StepSpeedAngle_3")

            dpg.add_text(pos=[155,120], default_value="J4")
            dpg.add_input_float(width=160, pos=[75, 140], tag="SpeedAngle_4", default_value=1, step=1)
            dpg.add_drag_float(width=160, pos=[75, 165],speed=0.001, min_value=0, default_value=1, callback=GetStepSpeed, tag="StepSpeedAngle_4")
            dpg.add_text(pos=[335,120], default_value="J5")
            dpg.add_input_float(width=160, pos=[255, 140], tag="SpeedAngle_5", default_value=1, step=1)
            dpg.add_drag_float(width=160, pos=[255, 165],speed=0.001, min_value=0, default_value=1, callback=GetStepSpeed, tag="StepSpeedAngle_5")
            dpg.add_text(pos=[515,120], default_value="J6")
            dpg.add_input_float(width=160, pos=[435, 140], tag="SpeedAngle_6", default_value=1, step=1)
            dpg.add_drag_float(width=160, pos=[435, 165],speed=0.001, min_value=0, default_value=1, callback=GetStepSpeed, tag="StepSpeedAngle_6")

            dpg.add_button(label="Сохранить", height=40, width=160, pos=[435,195], callback=SetSpeed)
    

    with dpg.child_window(border=False, tag="HomePosition", pos=[0,32], width=1310, height=610):
        Image = dpg.add_text(TextImage, pos= [-100, -40])
        dpg.bind_item_font(Image, fontImage)
        with dpg.child_window(border=False, pos=[450,200], width=650, height=300):
            dpg.add_text(pos=[155,20], default_value="J1")
            dpg.add_input_float(width=160, pos=[75, 40], tag="HomeAngle_1", default_value=oldJ1angle)
            dpg.add_drag_float(width=160, pos=[75, 65],speed=0.001, min_value=0, default_value=1, callback=GetStepHome, tag="StepHomeAngle_1")
            dpg.add_text(pos=[335,20], default_value="J2")
            dpg.add_input_float(width=160, pos=[255, 40], tag="HomeAngle_2", default_value=oldJ2angle)
            dpg.add_drag_float(width=160, pos=[255, 65],speed=0.001, min_value=0, default_value=1, callback=GetStepHome, tag="StepHomeAngle_2")
            dpg.add_text(pos=[515,20], default_value="J3")
            dpg.add_input_float(width=160, pos=[435, 40], tag="HomeAngle_3", default_value=oldJ3angle)
            dpg.add_drag_float(width=160, pos=[435, 65],speed=0.001, min_value=0, default_value=1, callback=GetStepHome, tag="StepHomeAngle_3")

            dpg.add_text(pos=[155,120], default_value="J4")
            dpg.add_input_float(width=160, pos=[75, 140], tag="HomeAngle_4", default_value=oldJ4angle)
            dpg.add_drag_float(width=160, pos=[75, 165],speed=0.001, min_value=0, default_value=1, callback=GetStepHome, tag="StepHomeAngle_4")
            dpg.add_text(pos=[335,120], default_value="J5")
            dpg.add_input_float(width=160, pos=[255, 140], tag="HomeAngle_5", default_value=oldJ5angle)
            dpg.add_drag_float(width=160, pos=[255, 165],speed=0.001, min_value=0, default_value=1, callback=GetStepHome, tag="StepHomeAngle_5")
            dpg.add_text(pos=[515,120], default_value="J6")
            dpg.add_input_float(width=160, pos=[435, 140], tag="HomeAngle_6", default_value=oldJ6angle)
            dpg.add_drag_float(width=160, pos=[435, 165],speed=0.001, min_value=0, default_value=1, callback=GetStepHome, tag="StepHomeAngle_6")

            dpg.add_button(label="Переместить робота", height=40, width=160, pos=[255,195], callback=MoveHomeRobot)
            dpg.add_button(label="Сохранить", height=40, width=160, pos=[435,195], callback=ReplaicePTPhome)


    dpg.hide_item("Calibration")
    dpg.hide_item("SpeedControll")
    dpg.hide_item("HomePosition")
    dpg.hide_item("XYZControl")

with dpg.window(label="Настройки",width= 610,height=397, pos=[0,430], tag="Notification",no_collapse=True, no_move=True, no_close=True, no_resize=True):
    with dpg.menu_bar():
        dpg.add_button(label="Физическая панель", callback=OpenAccount)
        # dpg.add_button(label="Notification", callback=OpenNotification)
        dpg.add_button(label="Логи", callback=OpenLogs)

    with dpg.child_window(width=579+ 17, height=343, tag="Phisic panel"):
        dpg.add_image("image_0", tag="Image_0", pos=[8,8])
        dpg.add_image("image_1", tag="Image_1", pos=[8,106])
        dpg.add_image("image_2", tag="Image_2", pos=[8,186])
        dpg.add_image("image_3", show=False, pos=[8,8], tag="Image_3")
        dpg.add_image("image_4", show=False, pos=[8,106], tag="Image_4")
        dpg.add_image("image_5", show=False, pos=[8, 186], tag="Image_5")
        dpg.add_text(default_value="Emergency stop", pos=[120, 45])
        dpg.add_text(default_value="Patron", pos=[120, 130])
        dpg.add_text(default_value="Cycle start", pos=[120, 220])

    # with dpg.child_window(width=579+ 17, height=343, tag="_Notification"):
    #     dpg.add_button(label="Debug fonts", callback=Font)
    #     dpg.add_button(label="Debug style", callback=DebugColor)
    #     dpg.add_button(label="Debug metrics", callback=DebugMetrics)
    #     dpg.add_button(label="Debug fonts", callback=Font)
    #     dpg.add_checkbox(label="full", default_value=False, callback=dpg.toggle_viewport_fullscreen, tag="Full")

    with dpg.child_window(width=579+ 17, height=343, tag="Logs"):
        log_panel = logger.mvLogger(parent="Logs")
    OpenAccount()

    


GetStartLog()
dpg.show_viewport()
# dpg.start_dearpygui()
dpg.toggle_viewport_fullscreen()
b = 60
while dpg.is_dearpygui_running():
    count_lines()
    UpdateAngleControll()
    UpdateAngleHome()
    dpg.render_dearpygui_frame()
    GetLogs()
    GetConfigPanel()
    if b == 60:
        AddDataSimplePlot()
        b = 0
    else:
        b+=1

    for child in range(0, len(dpg.get_item_children("ProgrammTabs")[1])):
        if child == 0:
            pass
        else:
            Prog = dpg.get_item_children("ProgrammTabs")[1][child]
            if dpg.is_item_clicked(Prog):
                dpg.set_value("fileName", dpg.get_item_label(dpg.get_item_children("ProgrammTabs")[1][child]))

    for tab in dpg.get_item_children("ProgrammTabs")[1]:
        if dpg.get_item_configuration(tab)["show"] == False:
            dpg.delete_item(tab)
    if len(dpg.get_item_children("ProgrammTabs")[1]) == 1:
        CloseProgrammInEditor()

dpg.destroy_context()