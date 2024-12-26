import os

from flask import Flask

class Loader:
    
    def __init__(self, app:Flask) -> None:
        globals()["app"] = app
        self.scan_directory(f"./public")
        
    def scan_directory(self, dir_path:str):
        # deep scan
        directories = [name for name in os.listdir(dir_path) if os.path.isdir(f"{dir_path}/{name}")]
        for dir in directories:
            self.scan_directory(f"{dir_path}/{dir}")
            
        # activate module
        if os.path.exists(f"{dir_path}/__init__.py"):
            module_name = f"{dir_path}/__init__".replace("/", ".").replace("\\", ".").lstrip("..")
            module = __import__(module_name)
            if hasattr(module, "get_app"):
                globals()["app"] = module.get_app()
    
    def __call__(self):
        return globals()["app"]