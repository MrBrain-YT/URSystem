from URLanguage import auth
# from URLanguage.roles import Roles

system = auth.Auth(server_token="15244dfbf0c9bd8378127e990c48e5a68b8c5a5786f34704bc528c9d91dbc84a",
            ip="localhost", port=5000).super_admin("SuperAdmin","12345").system(host="localhost", port=5000)

# system.add_kinematics("First", "C:/Users/MrBrain/Desktop/FinKinematic", "test")

# print(system.angle_to_xyz("First", [0,0,0,90], "654123"))

# h = system.lin("First", [0, 0, 0, 0], "654123")
# print(h)
res = system.set_emergency("First", "654123", False)
print(res)

# system.change_token("user", "12345")
# print(system.get_user_accounts())
# resp = system.get_robot("First")
# print(resp)

# system.set_program("First", "while True:print(7)", "654123")
# system.delete_program("First", "654123")
# resp = system.ptp("First", [0,0,0,0,0,0],"654123")
# print(resp)