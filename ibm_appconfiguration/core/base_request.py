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


import json as json_import
from http.cookiejar import CookieJar
from typing import Optional, Union
import requests
from .internal import ApiException
from .internal import remove_null_values
from .internal import BaseResponse
from .internal import Logger

import sys


class BaseRequest:

    def __init__(self):
        self.jar = CookieJar()
        Logger.debug("Initialised _BaseRequest")
        self.__python_version = 3

    def prepare_request(self,
                        method: str,
                        url: str,
                        headers: Optional[dict] = None,
                        data: Optional[Union[str, dict]] = None) -> dict:
        request = {
            'method': method,
            'url': url,
            'headers': headers
        }

        if sys.version_info >= (self.__python_version, 0) and isinstance(data, str):
            data = data.encode('utf-8')

        if data and isinstance(data, dict):
            data = remove_null_values(data)
            headers.update({'content-type': 'application/json'})
            data = json_import.dumps(data)
            request['data'] = data
        return request

    def send(self, request: requests.Request) -> BaseResponse:

        kwargs = dict({"timeout": 5})
        # kwargs['verify'] = False

        try:
            response = requests.request(**request, cookies=self.jar, **kwargs)

            if 200 <= response.status_code <= 299:
                if response.status_code == 204 or request['method'] == 'HEAD':
                    # There is no body content for a HEAD request or a 204 response
                    result = None
                elif not response.text:
                    result = None
                else:
                    try:
                        result = response.json()
                    except:
                        result = response
                return BaseResponse(result, response.headers,
                                    response.status_code)

            else:
                return BaseResponse(None, None, response.status_code)
                # raise ApiException(response.status_code, http_response=response)

        except requests.exceptions.SSLError:
            Logger.debug('requests.exceptions.SSLError')
            return BaseResponse(None, None,
                                400)
        except ApiException as err:
            Logger.debug(err.message)
            return BaseResponse(None, None,
                                400)
        except Exception as err:
            Logger.debug(f'Error in service API call {str(err)}')
            return BaseResponse(None, None,
                                400)
