import os

class Config():
    def __init__(self):
        self.BOOT_STRP_SERVERS = os.getenv("BOOT_STRP_SERVERS","http://localhost:9092")
        self.ELASTIC_HOST = os.getenv("ELASTIC_HOST","")
        self.TOPICS = os.getenv("TOPICS")

        