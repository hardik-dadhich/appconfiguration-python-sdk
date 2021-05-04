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

from .validators import Validators
from ..common import config_constants


class URLBuilder:
    __wsurl = "/wsfeature"
    __path = "/feature/v1/instances/"
    __service = "/apprapp"
    __events = "/events/v1/instances/"
    __config = "config"
    __override_server_host = ''
    __region = ''
    __http_base = ''
    __web_socket_base = ''

    @classmethod
    def init_with_collection_id(cls, collection_id='', region='', guid='', environment_id='', override_server_host=''):
        if Validators.validate_string(collection_id) \
                and Validators.validate_string(region)\
                and Validators.validate_string(guid)\
                and Validators.validate_string(environment_id):
            cls.__override_server_host = override_server_host
            cls.__region = region
            cls.__web_socket_base = config_constants.DEFAULT_WSS_TYPE
            cls.__http_base = config_constants.DEFAULT_HTTP_TYPE
            if Validators.validate_string(cls.__override_server_host):
                cls.__http_base = cls.__override_server_host
                cls.__web_socket_base += (cls.__override_server_host.replace("https://", "").replace("http://", ""))
            else:
                cls.__http_base += region
                cls.__http_base += config_constants.DEFAULT_BASE_URL
                cls.__web_socket_base += region
                cls.__web_socket_base += config_constants.DEFAULT_BASE_URL

        cls.__http_base += '{0}{1}{2}/collections/{3}/{4}?environment_id={5}'.format(cls.__service,
                                                                                     cls.__path,
                                                                                     guid,
                                                                                     collection_id,
                                                                                     cls.__config,
                                                                                     environment_id)

        cls.__web_socket_base += "{0}{1}?instance_id={2}&collection_id={3}&environment_id={4}".format(cls.__service,
                                                                                                      cls.__wsurl,
                                                                                                      guid,
                                                                                                      collection_id,
                                                                                                      environment_id)

    @classmethod
    def get_config_url(cls) -> str:
        return cls.__http_base

    @classmethod
    def get_web_socket_url(cls) -> str:
        return cls.__web_socket_base

    @classmethod
    def get_metering_url(cls) -> str:
        base = config_constants.DEFAULT_HTTP_TYPE + cls.__region + config_constants.DEFAULT_BASE_URL + cls.__service
        if Validators.validate_string(cls.__override_server_host):
            base = cls.__override_server_host + cls.__service
        return '{0}{1}'.format(base, cls.__events)
