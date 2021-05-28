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

from typing import Any
from .configurationType import ConfigurationType
from ibm_appconfiguration.core.internal import Logger


class Property:

    def __init__(self, property_list=dict):
        """
        @type property_list: dict
        """
        self.__name = property_list.get('name', '')
        self.__property_id = property_list.get('property_id', '')
        self.__segment_rules = property_list.get('segment_rules', list())
        self.__property_data = property_list
        self.__type = ConfigurationType(property_list.get('type') if property_list.get('type') is not None else ConfigurationType.NUMERIC)
        self.__value = property_list.get('value', object)

    def get_property_name(self) -> str:
        return self.__name

    def get_value(self) -> str:
        return self.__value

    def get_property_id(self) -> str:
        return self.__property_id

    def get_property_data_type(self) -> ConfigurationType:
        return self.__type

    def get_segment_rules(self) -> list:
        return self.__segment_rules

    def get_current_value(self, entity_id: str, entity_attributes: dict = dict()) -> Any:

        if not entity_id or entity_id == "":
            Logger.error("A valid entity id should be passed for this method.")
            return None
        from ibm_appconfiguration.configurations.configuration_handler import ConfigurationHandler
        configuration_handler = ConfigurationHandler.get_instance()
        return configuration_handler.property_evaluation(property_obj=self, entity_id=entity_id,
                                                         entity_attributes=entity_attributes)

