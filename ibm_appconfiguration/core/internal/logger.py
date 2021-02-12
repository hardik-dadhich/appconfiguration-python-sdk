# (C) Copyright IBM Corp. 2021.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.


import enum
import logging
import sys


class Logger:
    __is_debug = False

    def setup_custom_logger(name: str):
        formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        handler = logging.FileHandler('log.txt', mode='w')
        handler.setFormatter(formatter)
        screen_handler = logging.StreamHandler(stream=sys.stdout)
        screen_handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        logger.addHandler(screen_handler)
        return logger

    __AppLogger = setup_custom_logger("app_rapp_logger")

    class LoggerColors:
        INFO = '\033[99m'
        ERROR = '\033[91m'
        SUCCESS = '\033[92m'
        WARNING = '\033[93m'
        DEBUG = '\033[99m'
        END = '\033[0m'

    class LEVEL(enum.Enum):
        SUCCESS = 'SUCCESS'
        ERROR = 'ERROR'
        WARN = 'WARNING'
        INFO = 'INFO'
        DEBUG = 'DEBUG'

    @classmethod
    def set_debug(cls, value: bool):
        cls.__is_debug = value

    @classmethod
    def is_debug(cls):
        return cls.__is_debug

    @classmethod
    def info(cls, message):
        message = str(message)
        cls.__AppLogger.info(cls.LoggerColors.INFO + message + cls.LoggerColors.END)

    @classmethod
    def error(cls, message):
        message = str(message)
        cls.__AppLogger.error(cls.LoggerColors.ERROR + message + cls.LoggerColors.END)

    @classmethod
    def warning(cls, message):
        message = str(message)
        if cls.__is_debug:
            cls.__AppLogger.warning(cls.LoggerColors.WARNING + message + cls.LoggerColors.END)

    @classmethod
    def success(cls, message):
        message = str(message)
        if cls.__is_debug:
            cls.__AppLogger.info(cls.LoggerColors.SUCCESS + message + cls.LoggerColors.END)

    @classmethod
    def debug(cls, message):
        message = str(message)
        if cls.__is_debug:
            cls.__AppLogger.debug(cls.LoggerColors.DEBUG + message + cls.LoggerColors.END)
