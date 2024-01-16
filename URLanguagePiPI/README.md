
<!-- ![plot](./images/URLanguage.png) -->
_____

# What is this? #
Module for managing and administering industrial robot systems using URSystem API. This library provides access to 3 roles in the system:
_______

### User ###
The user can only work with robots and tools:
    
    system = Auth(server_token="15244dfbf0c9bd8378127e990c48e5a68b8c5a5786f34704bc528c9d91dbc84a",
            ip="localhost", port=5000).user("user","12345").system(host="localhost", port=5000)
	system.ptp(robot_name="First", angles=[0,0,0,0,0,0], code="654123")

### Admin ###

The administrator is already given rights to work directly with the system, but they do not give much power:
    
    system = Auth(server_token="15244dfbf0c9bd8378127e990c48e5a68b8c5a5786f34704bc528c9d91dbc84a",
            ip="localhost", port=5000).admin("Admin","12345").system(host="localhost", port=5000)
	system.delete_robot(robot_name="First")


### SuperAdmin ###
The Super Administrator is given all rights to work in the system. It can delete both users and administrators, change passwords, etc.:
    
    system = Auth(server_token="15244dfbf0c9bd8378127e990c48e5a68b8c5a5786f34704bc528c9d91dbc84a",
            ip="localhost", port=5000).SuperAdmin("SuperAdmin","12345").system(host="localhost", port=5000)
	system.delete_user(name="Jon")


Each higher-level role has the ability to use the commands of the lower-level role. That is, an administrator can also be a user, and a super administrator can be both an administrator and a user, respectively.

----------
# Certificate #

To send requests, you need to install the SSL certificate that your company issued to you or the standard URSystem certificate to trusted root certification authorities.

---

# Geting started #



First, you receive user database from the server.

	database = Auth(server_token="15244dfbf0c9bd8378127e990c48e5a68b8c5a5786f34704bc528c9d91dbc84a",
            ip="localhost", port=5000)


A server token is a set of characters to confirm your affiliation with a particular company. If you were given the correct token, the server will return you a database with logins, passwords and tokens.

Now having a database, we can get a token using this command:

    account = database.user(name="user",password="12345")

Now having a database, we can get a token using this command:

    system = account.system(host="localhost", port=5000)



And then, being connected to the system, you can use commands to work. Here's a code example:

    system.ptp(robot_name="First", angles=[0,0,0,0,0,0], code="654123")

----------

# Commands #
### User ###

### Admin ###

### SuperAdmin ###
___


# Developer #

My site: [link](https://github.com/MrBrain-YT) 