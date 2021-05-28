# Copyright 2021 IBM All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .configurations.internal.utils.validators import Validators
from .configurations.models import Feature, ConfigurationType, Property
from .core.internal import Logger
from .configurations.internal.common import config_messages
from typing import Dict, Optional
from .configurations.configuration_handler import ConfigurationHandler

try:
    import thread
except ImportError:
    import _thread as thread


class AppConfiguration:
    __instance = None

    # regions
    REGION_US_SOUTH = "us-south"
    REGION_EU_GB = "eu-gb"
    REGION_AU_SYD = "au-syd"
    override_server_host = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if AppConfiguration.__instance is None:
            return AppConfiguration()
        return AppConfiguration.__instance

    def __init__(self):
        """ Virtually private constructor. """

        if AppConfiguration.__instance is not None:
            raise Exception("AppConfiguration " + config_messages.SINGLETON_EXCEPTION)
        else:
            self.__apikey = ''
            self.__region = ''
            self.__configuration_handler_instance = None
            self.__guid = ''
            self.__is_initialized = False
            self.__is_initialized_configuration = False
            self.__is_loading = False
            AppConfiguration.__instance = self

    def init(self, region: str, guid: str, apikey: str):

        if not Validators.validate_string(region):
            Logger.error(config_messages.REGION_ERROR)
            return
        if not Validators.validate_string(apikey):
            Logger.error(config_messages.APIKEY_ERROR)
            return
        if not Validators.validate_string(guid):
            Logger.error(config_messages.GUID_ERROR)
            return
        self.__apikey = apikey
        self.__region = region
        self.__guid = guid
        self.__is_initialized = True
        self.__is_loading = False
        self.__setup_configuration_handler()

    def get_region(self) -> str:
        return self.__region

    def get_guid(self) -> str:
        return self.__guid

    def get_apikey(self) -> str:
        return self.__apikey

    def set_context(self, collection_id: str, environment_id: str,
                    configuration_file: Optional[str] = None,
                    live_config_update_enabled: Optional[bool] = True):

        if not self.__is_initialized:
            Logger.error(config_messages.COLLECTION_INIT_ERROR)
            return

        if not Validators.validate_string(collection_id):
            Logger.error(config_messages.COLLECTION_ID_VALUE_ERROR)
            return

        if not Validators.validate_string(environment_id):
            Logger.error(config_messages.ENVIRONMENT_ID_VALUE_ERROR)
            return

        self.__is_initialized_configuration = True
        if not live_config_update_enabled and configuration_file is None:
            Logger.error(config_messages.CONFIGURATION_FILE_NOT_FOUND_ERROR)
            return

        self.__configuration_handler_instance.set_context(collection_id, environment_id, configuration_file,
                                                          live_config_update_enabled)
        self.__load_data_now()

    def fetch_configurations(self):
        if self.__is_initialized and self.__is_initialized_configuration:
            self.__load_data_now()
        else:
            Logger.error(config_messages.COLLECTION_INIT_ERROR)

    def __setup_configuration_handler(self):
        self.__configuration_handler_instance = ConfigurationHandler.get_instance()
        self.__configuration_handler_instance.init(apikey=self.__apikey,
                                                   guid=self.__guid,
                                                   region=self.__region,
                                                   override_server_host=self.override_server_host)

    def __load_data_now(self):
        if self.__is_loading:
            return
        self.__is_loading = True
        self.__configuration_handler_instance.load_data()
        self.__is_loading = False

    def register_configuration_update_listener(self, listener):
        if self.__is_initialized and self.__is_initialized_configuration:
            self.__configuration_handler_instance.register_configuration_update_listener(listener)
        else:
            Logger.error(config_messages.COLLECTION_INIT_ERROR)

    def get_feature(self, feature_id: str) -> Feature:
        if self.__is_initialized and self.__is_initialized_configuration:
            return self.__configuration_handler_instance.get_feature(feature_id)
        else:
            Logger.error(config_messages.COLLECTION_INIT_ERROR)
            return None

    def get_features(self) -> Dict[str, Feature]:
        if self.__is_initialized and self.__is_initialized_configuration:
            return self.__configuration_handler_instance.get_features()
        else:
            Logger.error(config_messages.COLLECTION_INIT_ERROR)
            return None

    def get_properties(self) -> Dict[str, Property]:
        if self.__is_initialized and self.__is_initialized_configuration:
            return self.__configuration_handler_instance.get_properties()
        else:
            Logger.error(config_messages.COLLECTION_INIT_ERROR)
            return None

    def get_property(self, property_id: str) -> Property:
        if self.__is_initialized and self.__is_initialized_configuration:
            return self.__configuration_handler_instance.get_property(property_id)
        else:
            Logger.error(config_messages.COLLECTION_INIT_ERROR)
            return None

    def enable_debug(self, enable: bool):
        Logger.set_debug(enable)
