from confluent_kafka import Consumer
import json
class KafkaConsumer():
    def __init__(self,logger,boot_strap_servers,topics):
        self.logger = logger
        self.boot_strap_servers = boot_strap_servers
        self.topics = topics
        self.consumer = None

        self._get_consumer()

        self.logger.info("KafkaConsumer - created!")
    def _get_consumer(self):
        try:
            config = {"boot.strap.servers":self.boot_strap_servers,
                      "group.id":"main-tracker",
                      "auto.offset.reset":"earliest"}
            
            self.consumer = Consumer(config=config)

            self.consumer.subscribe([self.topics])

            self.logger.info("KafkaConsumer - soccessfuly connected")

        except Exception as e:
            self.logger.error(f"KafkaConsumer - error in logging to kafka: {e}")
            raise e
        
    def run(self,callback):
        counter = 0
        while True:
            try:
                msg = self.consumer.poll(1.0)

                if msg is None:
                    if counter % 5 == 0:
                        self.logger.debug("KafkaConsumer - no data")
                    counter +=1
                    continue
                    
                if msg.error():
                    self.logger.error(f"KafkaConsumer - {msg.error()}")
                    continue
                
            
                val = msg.value().decode('utf-8')

                data = json.loads(val)

                callback(data=data,topic=msg.topic())

                self.logger.debug(f"KafkaConsumer - msg:{data} successfuly transferd")

            except Exception as e:
                self.logger.error(f"KafkaConsumer - error in proseesing msg:{e}")


    