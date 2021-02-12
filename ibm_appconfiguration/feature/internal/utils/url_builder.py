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

from .validators import Validators


class URLBuilder:
    __baseurl = ".apprapp.cloud.ibm.com"
    __wsurl = "/wsfeature"
    __path = "/feature/v1/instances/"
    __service = "/apprapp"
    __http_type = "https://"
    __web_socket_type = "wss://"
    __events = "/events/v1/instances/"
    __config = "config"
    __override_server_host = ''
    __region = ''
    __guid = ''

    re_write_domain = None

    @classmethod
    def init_with_collection_id(cls, collection_id='', region='', guid='', override_server_host=''):
        if Validators.validate_string(collection_id):
            cls.__override_server_host = override_server_host
            cls.__region = region
            cls.__guid = guid
            cls.__web_socket_base = cls.__web_socket_type
            if Validators.validate_string(cls.__override_server_host):
                cls.__http_base = ""
                cls.__http_base += cls.__override_server_host
                cls.__web_socket_base += cls.__override_server_host
                cls.re_write_domain = cls.__override_server_host
            else:
                cls.__http_base = cls.__http_type
                cls.__http_base += region
                cls.__http_base += cls.__baseurl
                cls.__web_socket_base += region
                cls.__web_socket_base += cls.__baseurl
                cls.re_write_domain = ""

        cls.__http_base += '{0}{1}{2}/collections/{3}/{4}'.format(cls.__service,
                                                                  cls.__path,
                                                                  guid,
                                                                  collection_id,
                                                                  cls.__config)

        cls.__web_socket_base += "{0}{1}?instance_id={2}&collection_id={3}".format(cls.__service,
                                                                                   cls.__wsurl,
                                                                                   guid,
                                                                                   collection_id)

    @classmethod
    def get_config_url(cls) -> str:
        return cls.__http_base

    @classmethod
    def get_web_socket_url(cls) -> str:
        return cls.__web_socket_base

    @classmethod
    def get_metering_url(cls) -> str:
        base = cls.__http_type + cls.__region + cls.__baseurl + cls.__service
        if Validators.validate_string(cls.re_write_domain):
            base = cls.__override_server_host + cls.__service
        return '{0}{1}'.format(base, cls.__events)
