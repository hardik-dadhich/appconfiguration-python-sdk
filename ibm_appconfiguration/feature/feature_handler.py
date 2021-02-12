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

from typing import Dict, List, Optional, Any
from .models import Feature
from .models import SegmentRules
from .models import Segment
from ibm_appconfiguration.core.internal import Logger
from ibm_appconfiguration.core import BaseRequest
from .internal.utils.file_manager import FileManager
from .internal.utils.metering import Metering
from .internal.utils.socket import Socket
from .internal.utils.url_builder import URLBuilder
from threading import Timer
from ibm_appconfiguration.feature.internal.common import constants

try:
    import thread
except ImportError:
    import _thread as thread


class FeatureHandler:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if FeatureHandler.__instance is None:
            return FeatureHandler()
        return FeatureHandler.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self.__retry_count = 3
        if FeatureHandler.__instance is not None:
            raise Exception("FeatureHandler " + constants.SINGLETON_EXCEPTION)
        else:
            self.__collection_id = ''
            self.__apikey = ''
            self.__guid = ''
            self.__region = ''
            self.__is_initialized = False
            self.__is_initialized_feature = False
            self.__features_update_listener = None
            self.__feature_map = dict()
            self.__segment_map = dict()
            self.__live_feature_update_enabled = True
            FeatureHandler.__instance = self
            self.__retry_count = 3
            self.__retry_interval = 600000
            self.__feature_file = None
            self.__on_socket_retry = False
            self.__override_server_host = None
            self.__socket = None

    def init(self, apikey: str,
             guid: str,
             region: str,
             override_server_host=str):

        self.__apikey = apikey
        self.__guid = guid
        self.__region = region
        self.__override_server_host = override_server_host

        self.__feature_map = dict()
        self.__segment_map = dict()
        Metering.get_instance().set_metering_url(URLBuilder.get_metering_url(), self.__apikey)

    def set_collection_id(self, collection_id: str):

        self.__collection_id = collection_id
        URLBuilder.init_with_collection_id(collection_id=collection_id,
                                           guid=self.__guid,
                                           region=self.__region,
                                           override_server_host=self.__override_server_host)
        self.__is_initialized = True

    def fetch_features_from_file(self, live_feature_update_enabled: Optional[bool] = True,
                                 feature_file: Optional[str] = None):
        self.__live_feature_update_enabled = live_feature_update_enabled
        self.__feature_file = feature_file

    def load_data(self):
        if not self.__is_initialized:
            Logger.error(constants.FEATURE_HANDLER_INIT_ERROR)
            return
        if self.__feature_file:
            self.__get_file_data(self.__feature_file)
        self.__load_features()
        if self.__live_feature_update_enabled:
            thread.start_new_thread(self.__fetch_features_data, ())
        else:
            if self.__socket:
                self.__socket.cancel()

    def register_features_update_listener(self, listener):
        if callable(listener):
            if self.__is_initialized:
                self.__features_update_listener = listener
            else:
                Logger.error(constants.FEATURE_HANDLER_INIT_ERROR)
        else:
            Logger.error(constants.FEATURE_HANDLER_METHOD_ERROR)

    def get_features(self) -> Dict[str, Feature]:
        return self.__feature_map

    def get_feature(self, feature_id: str):
        if feature_id in self.__feature_map:
            return self.__feature_map.get(feature_id)
        else:
            self.__load_features()
            if feature_id in self.__feature_map:
                return self.__feature_map.get(feature_id)
            else:
                Logger.error(constants.FEATURE_INVALID + feature_id)
                return None

    def __fetch_features_data(self):
        if self.__is_initialized:
            self.__fetch_from_api()
            self.__start_web_socket()

    def __start_web_socket(self):
        headers = {
            'Authorization': self.__apikey
        }
        if self.__socket:
            self.__socket.cancel()
        self.__socket = Socket(
            url=URLBuilder.get_web_socket_url(),
            headers=headers,
            callback=self.__on_web_socket_callback
        )

    def __get_file_data(self, file_path: str):
        data = FileManager.read_files(file_path=file_path)
        if data is not None:
            self.__write_to_file(json=data)

    def __load_features(self):
        all_feature: dict = FileManager.read_files()
        if all_feature:
            if 'features' in all_feature:
                self.__feature_map = dict()
                try:
                    all_feature_list: List = all_feature.get('features')
                    for i in range(0, len(all_feature_list)):
                        feature: dict = all_feature_list[i]
                        feature_obj = Feature(feature)
                        self.__feature_map[feature_obj.get_feature_id()] = feature_obj
                except Exception as err:
                    Logger.debug(err)

            if 'segments' in all_feature:
                self.__segment_map = dict()
                try:
                    segment_list: List = all_feature.get('segments')
                    for i in range(0, len(segment_list)):
                        segment: dict = segment_list[i]
                        segment_obj = Segment(segment)
                        self.__segment_map[segment_obj.get_segment_id()] = segment_obj
                except Exception as err:
                    Logger.debug(err)

    def record_valuation(self, feature_id):
        Metering.get_instance().add_metering(
            guid=self.__guid,
            feature_id=feature_id,
            collection_id=self.__collection_id
        )

    def feature_evaluation(self, feature: Feature, identity_attributes: dict = dict()) -> Any:

        if len(identity_attributes) <= 0:
            return feature.get_enabled_value()

        rules_map = self.__parse_rules(feature.get_segment_rules())

        for i in range(1, len(rules_map) + 1):
            segment_rule = rules_map[i]
            if not (segment_rule is None):
                for level in range(0, len(segment_rule.get_rules())):
                    try:
                        rule: dict = segment_rule.get_rules()[level]
                        segments: List = rule.get('segments')
                        for inner_level in range(0, len(segments)):
                            segment_key = segments[inner_level]
                            if self.__evaluate_segment(segment_key, identity_attributes):
                                if segment_rule.get_value() == "$default":
                                    return feature.get_enabled_value()
                                else:
                                    return segment_rule.get_value()

                    except Exception as err:
                        Logger.debug(err)

        return feature.get_enabled_value()

    def __evaluate_segment(self, segment_key: str, identity_attributes: dict) -> bool:
        if segment_key in self.__segment_map:
            segment: Segment = self.__segment_map[segment_key]
            return segment.evaluate_rule(identity_attributes)
        return False

    def __parse_rules(self, segment_rules: List) -> dict:
        rule_map = dict()
        for i in range(0, len(segment_rules)):
            try:
                rules = segment_rules[i]
                rules_obj = SegmentRules(rules)
                rule_map[rules_obj.get_order()] = rules_obj
            except Exception as err:
                Logger.debug(err)
        return rule_map

    def __write_server_file(self, json: dict):
        if self.__live_feature_update_enabled:
            self.__write_to_file(json)

    def __write_to_file(self, json: dict):
        FileManager.store_files(json)
        self.__load_features()
        if self.__features_update_listener and callable(self.__features_update_listener):
            self.__features_update_listener()

    def __fetch_from_api(self):
        if self.__is_initialized:
            self.__retry_count -= 1
            config_url = URLBuilder.get_config_url()
            service = BaseRequest()
            header = {
                'Authorization': self.__apikey,
                'Content-Type': 'application/json'
            }

            request = service.prepare_request(
                method='GET',
                url=config_url,
                headers=header
            )

            response = service.send(request)
            status_code = response.get_status_code()

            if 200 <= status_code <= 299:
                response_data = response.get_result()
                try:
                    response_data = dict(response_data)
                    if response_data:
                        self.__write_server_file(response_data)
                except:
                    if response_data:
                        self.__write_server_file(response_data)
            else:
                if self.__retry_count > 0:
                    self.__fetch_from_api()
                else:
                    self.__retry_count = 3
                    Logger.error(constants.FEATURE_API_ERROR)
                    Timer(self.__retry_interval, lambda: self.__fetch_from_api()).start()
        else:
            Logger.debug(constants.FEATURE_HANDLER_INIT_ERROR)

    def __on_web_socket_callback(self, message=None, error_state=None, closed_state=None, open_state=None):
        if message:
            self.__fetch_from_api()
            Logger.debug(f'Received message from socket {message}')
        elif error_state:
            Logger.debug(f'Received error from socket {error_state}')
        elif closed_state:
            Logger.debug(f'Received close connection from socket')
            self.__on_socket_retry = True
            Timer(self.__retry_interval, lambda: self.__start_web_socket()).start()
        elif open_state:
            if self.__on_socket_retry:
                self.__on_socket_retry = False
                self.__fetch_from_api()
            Logger.debug(f'Received opened connection from socket')
        else:
            Logger.debug('Unknown Error inside the socket connection')
