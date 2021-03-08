from config import config

import json_log_formatter

import logging
import sys


class CustomisedJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message: str, extra: dict, record: logging.LogRecord) -> dict:
        extra['message'] = message

        # Include builtins
        extra['level'] = record.levelname
        extra['name'] = record.name

        if record.exc_info:
            extra['exc_info'] = self.formatException(record.exc_info)

        return extra


def setup_logging() -> None:
    # Clear all logging handlers to make way for custom
    logging.getLogger().handlers = []

    file_handler = logging.FileHandler(filename='tmp.log')
    file_handler.setFormatter(CustomisedJSONFormatter())
    file_handler.setLevel(logging.getLevelName(config["logging"]["file-level"]))

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_log_format = '[%(asctime)s] [%(levelname)s] {%(filename)s:%(lineno)d} %(message)s'
    formatter = logging.Formatter(stdout_log_format)
    stdout_handler.setFormatter(formatter)
    stdout_handler.setLevel(logging.getLevelName(config["logging"]["stdout-level"]))

    logging.getLogger().setLevel(logging.NOTSET)
    logging.getLogger().addHandler(file_handler)
    logging.getLogger().addHandler(stdout_handler)