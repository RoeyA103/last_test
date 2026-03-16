import logging

class Logger():
    def __init__(self,app_name):
        self.logger = None
        self.app_name= app_name

        self._create_logger

    def _create_logger(self):
        logger = logging.getLogger(self.app_name)
        logger.setLevel(logging.DEBUG)
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        f = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        sh.setFormatter(f)
        logger.addHandler(sh)

        self.logger = logger

    def get_logger(self):
        return self.logger