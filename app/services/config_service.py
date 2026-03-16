import os

class Config():
    def __init__(self):
        self.BOOT_STRP_SERVERS = os.getenv("BOOT_STRP_SERVERS","localhost:9092")
        self.ELASTIC_HOST = os.getenv("ELASTIC_HOST","http://localhost:9200")
        self.TOPICS = ["intel","attack","damage"]
        self.PRODUCER_TOPIC = os.getenv("PRODUCER_TOPIC","intel_signals_dlq")
        self.MONGO_HOTS = os.getenv("MONGO_HOTS","mongodb://localhost:27017")
        self.MONGO_DB = os.getenv("MONGO_DB","intels")
        