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


class Feature:

    def __init__(self, feature_list=dict):
        """
        @type feature_list: dict
        """
        self.__enabled = feature_list.get('enabled', False)
        self.__name = feature_list.get('name', '')
        self.__feature_id = feature_list.get('feature_id', '')
        self.__segment_rules = feature_list.get('segment_rules', list())
        self.__feature_data = feature_list
        self.__type = ConfigurationType(feature_list.get('type') if feature_list.get('type') is not None else ConfigurationType.NUMERIC)
        self.__disabled_value = feature_list.get('disabled_value', object)
        self.__enabled_value = feature_list.get('enabled_value', object)

    def get_feature_name(self) -> str:
        return self.__name

    def get_disabled_value(self) -> str:
        return self.__disabled_value

    def get_enabled_value(self) -> str:
        return self.__enabled_value

    def get_feature_id(self) -> str:
        return self.__feature_id

    def get_feature_data_type(self) -> ConfigurationType:
        return self.__type

    def is_enabled(self) -> bool:
        return self.__enabled

    def get_segment_rules(self) -> list:
        return self.__segment_rules

    def get_current_value(self, entity_id: str, entity_attributes: dict = dict()) -> Any:
        if not entity_id or entity_id == "":
            Logger.error("A valid entity id should be passed for this method.")
            return None
        from ibm_appconfiguration.configurations.configuration_handler import ConfigurationHandler
        feature_handler = ConfigurationHandler.get_instance()
        return feature_handler.feature_evaluation(feature=self, entity_id=entity_id, entity_attributes=entity_attributes)
