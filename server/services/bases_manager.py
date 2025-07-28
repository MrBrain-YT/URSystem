from utils.logger import Logger
from configuration.cache.file_cache import save_to_cache
from utils.validator import BasesChecker, validate_types

bases = {}

class BasesManager:
    bases = bases
    logger = Logger()
    bases_checker = BasesChecker()
    
    def __init__(self, bases:dict=None) -> None:
        self.logger_module = "URBases"
        if bases is not None:
            self.bases.update(bases)
    
    def get_bases(self) -> dict:
        return self.bases
    
    def set_bases(self, users:dict) -> None:
        self.bases.update(users)
    
    @validate_types    
    def get_bases_api(self) -> tuple:
        return {"status": True, "info": "Bases data", "data": self.bases}, 200
    
    @validate_types
    def get_base(self, base_name:str) -> tuple:
        if self.bases_checker.base_exists(base_name):
            return {"status": True, "info": "Base data", "data": self.bases}, 200
        else:
            log_message = "Base not exists"
            return {"status": False, "info": log_message}, 400
    
    @validate_types
    def create_base(self, base_name:str) -> tuple:
        if not self.bases_checker.base_exists(base_name):
                self.bases[base_name] = {}
                save_to_cache(bases=self.bases)
                log_message = f"Base '{base_name}' created"
                self.logger.info(msg=log_message, module=self.logger_module)
                return {"status": True, "info": log_message}, 200
        else:
            log_message = "Base already exists"
            return {"status": False, "info": log_message}, 400
    
    @validate_types  
    def set_base_data(self, base_name:str, base_data:dict) -> tuple:
        if self.bases_checker.base_exists(base_name):
            if self.bases_checker.data_is_valid(base_data):
                    self.bases[base_name] = base_data
                    save_to_cache(bases=self.bases)
                    log_message = f"Base data set for base '{base_name}'"
                    self.logger.info(msg=log_message, module=self.logger_module)
                    return {"status": True, "info": log_message}, 200
            else:
                log_message = "Base data not valid"
                return {"status": False, "info": log_message}, 400
        else:
            log_message = "Base not exists"
            return {"status": False, "info": log_message}, 400
    
    @validate_types 
    def delete_base(self, base_name:str) -> tuple:
        from services.multi_robots_manager import MultiRobotsManager
        if self.bases_checker.base_exists(base_name):
            robots = MultiRobotsManager().get_robots()
            del self.bases[base_name]
            for key, value in robots.items():
                if robots[key]["Base"] == base_name:
                    robots[key]["Base"] = ""
            save_to_cache(robots=robots, bases=self.bases)
            log_message = f"Base '{base_name}' deleted"
            self.logger.info(msg=log_message, module=self.logger_module)
            return {"status": True, "info": log_message}, 200
        else:
            log_message = "Base not exists"
            return {"status": False, "info": log_message}, 400
    