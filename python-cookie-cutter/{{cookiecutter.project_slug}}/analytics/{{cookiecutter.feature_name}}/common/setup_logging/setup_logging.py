import logging
from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['app'] = "{{cookiecutter.feature_name}}"
        log_record['filename'] = '{}:{}'.format(record.filename, record.lineno)
        log_record['function'] = record.funcName
        log_record['level'] = record.levelname


def initialise_logging(debug=False):
    """
    Initialise logging
    :param debug:
    :return:
    """

    logger = logging.getLogger()

    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG

    logger.setLevel(log_level)


def setup_loggers():
    #   If there is code calling logging.basicConfig() before the JSON logging
    #   setup code below, we will end up with every log event being printed twice: first as plain text, then as JSON.
    #   By attaching a handler to the root formatter first, we prevent logging.basicConfig() from doing anything, and log
    #   events are output only once, as JSON, as we require.
    logger = logging.getLogger()
    logHandler = logging.StreamHandler()
    formatter = CustomJsonFormatter('%(asctime)s %(message)s')
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)