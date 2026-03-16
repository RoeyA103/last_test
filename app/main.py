from services.config_service import Config
from services.consumer import KafkaConsumerService
from services.producer import Producer
from services.logger_service import Logger
from services.mongo_service import MongoService
from services.thier_logger import log_event
from services.validator import Validator
from menager import Menager


def main():
    config = Config()
    logger = Logger(app_name="Digital Hunter")
    validator = Validator(my_logger=logger.get_logger(),
                                    their_logger=log_event)
    
    consumer = KafkaConsumerService(my_logger=logger.get_logger(),
                                    their_logger=log_event,
                                    boot_strap_servers=config.BOOT_STRP_SERVERS,
                                    topics=config.TOPICS)
    
    producer = Producer(my_logger=logger.get_logger(),
                                    their_logger=log_event,
                                    boot_strap_servers=config.BOOT_STRP_SERVERS,
                                    topic=config.PRODUCER_TOPIC)
    
    mongo = MongoService(my_logger=logger.get_logger(),
                                    their_logger=log_event,
                                    mongo_host=config.MONGO_HOTS,
                                    db=config.MONGO_DB)
    menager = Menager(my_logger=logger.get_logger(),
                                    their_logger=log_event,
                                    producer=producer,
                                    consumer=consumer,
                                    validator=validator,
                                    mongo=mongo)
    menager.run()

if __name__=="__main__":
    main()