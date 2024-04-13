import logging

def logging_setup():
    root_logger = logging.getLogger()
    logger_level = logging.DEBUG if __debug__ else logging.INFO
    logger_format = "%(name)s %(asctime)s %(levelname)s %(message)s"
    logging.basicConfig(
        level=logger_level,
        format=logger_format
    )
    file_handler = logging.FileHandler("general.log", mode='w')
    formatter = logging.Formatter(logger_format)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    logging.getLogger("requests").setLevel(logging.WARNING)