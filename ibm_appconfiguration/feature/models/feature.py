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
from typing import Any
from ibm_appconfiguration.core.internal import Logger


class FeatureType(enum.Enum):
    NUMERIC = 'NUMERIC'
    STRING = 'STRING'
    BOOLEAN = 'BOOLEAN'


class Feature:

    def __init__(self, feature_list=dict):
        """
        @type feature_list: dict
        """
        self.__enabled = feature_list.get('isEnabled', False)
        self.__name = feature_list.get('name', '')
        self.__feature_id = feature_list.get('feature_id', '')
        self.__segment_rules = feature_list.get('segment_rules', list())
        self.__segment_exists = feature_list.get('segment_exists', False)
        self.__feature_data = feature_list
        self.__type = FeatureType(feature_list.get('type'))
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

    def get_feature_data_type(self) -> FeatureType:
        return self.__type

    def is_enabled(self) -> bool:
        return self.__enabled

    def get_segment_rules(self) -> list:
        return self.__segment_rules

    def get_current_value(self, identity_id: str, identity_attributes: dict = dict()) -> Any:

        if not identity_id or identity_id == "":
            Logger.error("A valid id should be passed for this method.")
            return None
        from ibm_appconfiguration.feature.feature_handler import FeatureHandler
        feature_handler = FeatureHandler.get_instance()

        feature_handler.record_valuation(self.__feature_id)

        if self.__enabled:
            if self.__segment_exists and len(self.__segment_rules) > 0:
                return feature_handler.feature_evaluation(self, identity_attributes)

            else:
                return self.__enabled_value
        else:
            return self.__disabled_value

