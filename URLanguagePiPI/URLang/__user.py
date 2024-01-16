"""  module for get commands from Robot and Tools class for the user.

The tokenizer class is used to automatically send a token to the system class after registration.

"""

from . import __tools
from . import __robot

token = ""
class tokenizer():

    def __init__(self, token) -> None:
        self.__token = token

    def set_token(self) -> None:
        global token
        token = self.__token
    
# United robotics system 
class system(__robot.Robot, __tools.Tools):
    
    def __init__(self, host:str, port:int) -> None:
        super().__init__(host, port, token=token)

    