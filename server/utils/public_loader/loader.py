import os

from flask import Flask

class Loader:
    _app:Flask
    
    def __init__(self) -> None:
        pass

    def init_app(self, app: Flask) -> None:
        self._app = app
        self.scan_directory("./public")
    
    @property
    def app(self):
        return self._app
        
    # TODO: find files with specific function from os module
    def scan_directory(self, dir_path:str) -> None:
        # deep scan
        directories = [name for name in os.listdir(dir_path) if os.path.isdir(f"{dir_path}/{name}")]
        for dir in directories:
            self.scan_directory(f"{dir_path}/{dir}")
        
        # activate module
        if os.path.exists(f"{dir_path}/__init__.py"):
            module_name = f"{dir_path}".replace("/", ".").replace("\\", ".").lstrip("..")
            module = __import__(module_name)
            if hasattr(module, "return_app"):
                self._app = module.return_app()
    
loader = Loader()