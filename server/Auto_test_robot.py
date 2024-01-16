import robot_modules.auth  as auth

robot = auth.Auth("localhost", 5000, "15244dfbf0c9bd8378127e990c48e5a68b8c5a5786f34704bc528c9d91dbc84a")\
    .robot("First", "12345").Robot("localhost", 5000, "654123")
    
""" PTP test """
robot.ptp([300,10,0,100])
# robot.ptp([10,0,0,-10])
# robot.ptp([200,60,30,20])
# print(robot.ptp([0,-100,-20,100]))

""" Drawing cube """
# robot.move_xyz([100, 0, 67.117]) # рисуем квадрат
# robot.move_xyz([200, 0, 67.117])
# robot.move_xyz([200, 100, 67.117])
# robot.move_xyz([100, 100, 67.117])
# robot.move_xyz([100, 0, 67.117])

""" XYZ test """
# robot.move_xyz([300, 0, 67.117])
# robot.move_xyz([300, 0, 67.117+200])
# robot.move_xyz([300, 0, 67.117-200])
# ang = robot.angle_to_xyz([180,60,30, 20])
# print(ang)
# one = [200,100,67.117]
# two = [250,0,67.117]
# three = [200,-100,67.117]
# robot.circ([one, two, three], 10)
# print(robot.xyz_to_angle([300, 0, 67.117+200]))
# print(robot.xyz_to_angle([300, 0, 67.117-200]))
# robot.move_xyz([300, 0, 67.117])
# robot.move_xyz([-200, -200, 67.117])

""" LIN test """
# robot.lin([180,60,30,20], 100)
# robot.lin([180,-30,-30,40], 100)
# robot.lin([200,60,30,20])
# robot.lin([0,-100,-20,100])