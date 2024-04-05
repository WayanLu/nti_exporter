import logging


def set_logger(working_directory: str) -> None:
    # Configure logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # Create file handler which logs messages to a file
    file_handler = logging.FileHandler(f'{working_directory}/nti_exporter.log', mode='a')
    file_handler.setLevel(logging.INFO)
    # Create console handler which logs messages to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
