import math
import copy 
class Menager():
    def __init__(self,my_logger,their_logger,producer,consumer,validator,mongo):
        self.logger = my_logger
        self.thier_logger = their_logger
        self.producer = producer
        self.consumer = consumer
        self.validator = validator
        self.mongo = mongo

    def haversine_km(self,lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate the great-circle distance in km between two points on Earth."""
        EARTH_RADIUS_KM = 6371.0

        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        a = (
            math.sin(delta_lat / 2) ** 2
            + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return EARTH_RADIUS_KM * c
    
    def handel_intel(self,val:dict):
        if not self.mongo.get_doc(entity_id = val['entity_id'],collection='intel'):
            doc = self.validator.validate(data=val,topic="intel")
            self.mongo.save_doc(doc=doc.model_dump(),collection='intel')
        
        else:
            old_doc = self.mongo.get_doc(entity_id = val['entity_id'],collection='intel')
            old_lat , old_lon = old_doc["reported_lat"] , old_doc["reported_lon"]
            lat , lon = val["reported_lat"] , val["reported_lon"]
            val["distance_from_last_point"] = self.haversine_km(lat1=old_lat, lon1=old_lon, lat2=lat, lon2=lon)
            self.mongo.replace(doc=val,entity_id=val['entity_id'],collection='intel')

        self.thier_logger(level="info", message=f"manager - handel intel msg", extra_info=val)
    


    def handel_attack(self,val):
        if not self.mongo.get_doc(entity_id = val['entity_id'],collection='attack'):
            self.mongo.update_doc(updated_filed={'status':'attacked'},entity_id=val['entity_id'],collection='intel')
        self.mongo.save_doc(doc=val,collection='attack')

        self.thier_logger(level="info", message=f"manager - handel attack msg", extra_info=val)

    def handel_damage(self,val:dict):
        status = val["result"]
        self.mongo.update_doc(self,updated_filed={'status':status},entity_id=val['entity_id'],collection='intel')
        self.mongo.save_doc(doc=val,collection='damage')

        self.thier_logger(level="info", message=f"manager - handel damage msg", extra_info=val)

    def handel_event(self,topic,val=None,error=None):
        if error:                                               #if the consumer rais json error means the data is currapt
            self.producer.produce_error(msg={"topic":topic,"error":error})
        
        elif e :=isinstance(self.validator.validate(data=val,topic=topic),str): 
            self.producer.produce_error(msg={"topic":topic,"error":e})
            self.thier_logger(level="error", message=f"menager - validation error", extra_info=val)
        
        elif val.get("status",None) == "destroyed":             
            self.producer.produce_error(msg={"topic":topic,"error":f"{val['"entity_id"']} is allready destroyed"})
            self.thier_logger(level="error", message=f"menager - terget allready destroyed error", extra_info=val)
        
        else:
            if topic == 'intel':
                self.handel_intel(val=val)
            elif topic == "attack":
                self.handel_attack(val=val)
            else:
                self.handel_damage(val=val)
        
    def run(self):
        self.consumer.run(callback=self.handel_event)

a = {"a":1}
