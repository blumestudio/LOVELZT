import logging

class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler("server.log")
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log(self, message, level=logging.INFO):
        if level == logging.DEBUG:
            self.logger.debug(message)
        elif level == logging.INFO:
            self.logger.info(message)
        elif level == logging.WARNING:
            self.logger.warning(message)
        elif level == logging.ERROR:
            self.logger.error(message)
        elif level == logging.CRITICAL:
            self.logger.critical(message)

    def log_info(self, message):
        self.log(message, logging.INFO)

    def log_warning(self, message):
        self.log(message, logging.WARNING)

    def log_error(self, message):
        self.log(message, logging.ERROR)

    def log_debug(self, message):
        self.log(message, logging.DEBUG)

    def log_critical(self, message):
        self.log(message, logging.CRITICAL)
