#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import logging.config

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.const as CT


class Logger:
    """日志类"""
    LOGGER_QUANT = 'quant'
    LOGGER_WARN = 'warn'
    LOGGER_TRADE = 'trade'
    LOGGER_SMTP = 'smtp'

    __instance = None
    log_conf = CT.CONF_DIR + "logger.conf"

    def __init__(self):
        logging.config.fileConfig(CT.CONF_DIR + "logger.conf")

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            if not cls.__instance:
                # cls.__instance = super(Broker, cls).__new__(cls, *args, **kwargs)
                cls.__instance = super(Logger, cls).__new__(cls)
        return cls.__instance

    @staticmethod
    def get_instance():
        if Logger.__instance is None:
            Logger.__instance = Logger()
        return Logger.__instance

    @staticmethod
    def quant(message):
        """系统日志"""
        Logger.get_instance()
        logging.getLogger(Logger.LOGGER_QUANT).info(message)
        return 0

    @staticmethod
    def warn(message):
        """warning日志"""
        Logger.get_instance()
        logging.getLogger(Logger.LOGGER_WARN).warning(message)
        return 0

    @staticmethod
    def trade(message):
        """交易日志"""
        Logger.get_instance()
        logging.getLogger(Logger.LOGGER_TRADE).info(message)
        return 0

    @staticmethod
    def smtp(message):
        """邮件"""
        Logger.get_instance()
        logging.getLogger(Logger.LOGGER_SMTP).warning(message)
        return 0


def main(argv):
    Logger.quant('quant log test')
    #Logger.smtp('smtp log test')


if __name__ == "__main__":
    main(sys.argv)

