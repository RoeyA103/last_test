from pydantic import BaseModel , Field
from typing import Optional
class Info(BaseModel):
    timestamp: str
    signal_id: str
    entity_id: str
    reported_lat: float
    reported_lon: float
    signal_type: str
    priority_level: int = Field(default=99)
    distance_from_last_point :int = 0 

class Attack(BaseModel):
    timestamp: str
    attack_id: str
    entity_id: str
    weapon_type: str | None = None

class Damage(BaseModel):
    timestamp: str
    attack_id: str
    entity_id: str
    result: str

class Validator():
    def __init__(self,my_logger,their_logger):
        self.logger = my_logger
        self.their_logger = their_logger

    def validate_info(self,data:dict)-> dict | str:
        try:
           return Info.model_validate(data)
            
        except Exception as e:
            return str(e)
    
    def validate_attack(self,data:dict)->dict | str:
        try:
            return Attack.model_validate(data)
        except Exception as e:
            return str(e)
        
    def validate_damage(self,data:dict)->dict | str:
        try:
           return  Damage.model_validate(data)
        except Exception as e:
            return str(e)
        
    def validate(self,data:dict,topic:str):
        if topic == "damage":
            return self.validate_damage(data)
        if topic == "intel":
            return self.validate_info(data)
        
        return self.validate_attack(data)
 

