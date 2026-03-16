
class Menager():
    def __init__(self,my_logger,their_logger,producer,consumer,validator,mongo):
        self.logger = my_logger
        self.thier_logger = their_logger
        self.producer = producer
        self.consumer = consumer
        self.validator = validator
        self.mongo = mongo

    def handel_event(self,topic,val=None,error=None):
        
        if error:                                               #if the consumer rais json error means the data is currapt
            self.producer.produce_error(msg={"topic":topic,"error":error})

        elif a:= self.validator.validate(data=val,topic=topic): 
            self.producer.produce_error(msg={"topic":topic,"error":a})
        
        elif val.get("status",None) == "destroyed":               
            self.producer.produce_error(msg={"topic":topic,"error":f"{val['"entity_id"']} is allready destroyed"})
        
        else:

        
        