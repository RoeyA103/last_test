import logging

class Logger():
    def __init__(self, app_name: str):
        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:  
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)

            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            ch.setFormatter(formatter)

            self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger