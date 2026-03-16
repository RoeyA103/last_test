from kafka import KafkaProducer
import json

class Producer():
    def __init__(self,my_logger,their_logger,boot_strap_servers:str,topic:str):
        self.logger = my_logger
        self.their_logger = their_logger
        self.boot_strap_servers = boot_strap_servers
        self.topic = topic
        self.producer = self._get_producer

    def _get_producer(self):
        try:
            producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: v if isinstance(v, bytes) else json.dumps(v).encode("utf-8")
            )

            self.logger.info("Producer - Connected to Kafka")
            return producer
        except Exception as e:
            self.logger.error(f"Producer - error in connecting to Kafka:{e}")

    def produce_error(self,msg):
        try:
            self.producer.send(self.topic, value=msg)
            self.producer.flush()

        except Exception as e:
            self.logger.info(f"Producer - could not sent msg:{e}")
            self.their_logger(level="error", message=f"Producer - could not sent msg:{e}", extra_info={"msg":msg})


        