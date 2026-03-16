from kafka import KafkaConsumer
import json

class KafkaConsumerService():
    def __init__(self,my_logger,their_logger,boot_strap_servers:str,topics:list):
        self.logger = my_logger
        self.their_logger = their_logger
        self.boot_strap_servers = boot_strap_servers
        self.topics = topics
        self.consumer = None

        self._get_consumer()

        self.logger.info("KafkaConsumer - created!")
        self.their_logger(level="info", message="KafkaConsumer - created!", extra_info=None)
    def _get_consumer(self):
        try:
            self.consumer = KafkaConsumer(bootstrap_servers=[self.boot_strap_servers],group_id="main-tracker",
                         auto_offset_reset ="earliest",
                         max_poll_records=1)

            self.consumer.subscribe(self.topics)

            self.logger.info("KafkaConsumer - soccessfuly connected")
            self.their_logger(level="info", message="KafkaConsumer - soccessfuly connected", extra_info=None)


        except Exception as e:
            self.logger.error(f"KafkaConsumer - error in logging to kafka: {e}")
            self.their_logger(level="error", message=f"KafkaConsumer - error in logging to kafka: {e}", extra_info=None)

            raise e
        
    def run(self,callback):
        while True:
            try:
                msg = self.consumer.poll(max_records=1,timeout_ms=1.0)
                for partition in msg.values():
                    for message in partition:
                        try:
                            topic = message.topic
                            val = json.loads(message.value.decode('utf-8'))

                            self.logger.info(f"KafkaConsumer - got msg from :{topic}")
                            self.their_logger(level="info", message=f"KafkaConsumer - got msg from :{topic}",
                                               extra_info={"entity_id":val["entity_id"],"topic":topic})
                            
                            callback(topic=topic,val=val)

                        except json.decoder.JSONDecodeError as e:

                            callback(topic=topic,error=e)
                            self.logger.error(f"KafkaConsumer - json error on:{val}")
                            self.their_logger(level="error", message=f"KafkaConsumer - json error on:{val}", extra_info=None)

            except Exception as e:
                self.logger.error(f"menager - error in proseesing msg:{e}")
                self.their_logger(level="error", message=f"menager - error in proseesing msg:{e}", extra_info=None)



    