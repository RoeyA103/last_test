from pydantic import BaseModel 

class Info(BaseModel):
    timestamp: str
    signal_id: str
    entity_id: str
    reported_lat: float
    reported_lon: float
    signal_type: str
    priority_level: int

class Attack(BaseModel):
    timestamp: str
    attack_id: str
    entity_id: str
    weapon_type: str

class Damage(BaseModel):
    timestamp: str
    attack_id: str
    entity_id: str
    result: str

class Validator():
    def __init__(self,my_logger,their_logger):
        self.logger = my_logger
        self.their_logger = their_logger

    def validate_info(data:dict)-> None | str:
        try:
            Info.model_validate(data)
            
        except Exception as e:
            return str(e)
    
    def validate_attack(data:dict)->None | str:
        try:
            Attack.model_validate(data)
        except Exception as e:
            return str(e)
        
    def validate_damage(data:dict)->None | str:
        try:
            Damage.model_validate(data)
        except Exception as e:
            return str(e)
        
    def validate(self,data:dict,topic:str):
        if topic == "damage":
            return self.validate_damage(data)
        if topic == "info":
            return self.validate_info(data)
        
        return self.validate_attack(data)
 