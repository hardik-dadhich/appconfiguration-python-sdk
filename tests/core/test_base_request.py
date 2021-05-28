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

import unittest
from unittest.mock import patch
from ibm_appconfiguration.core.base_request import BaseRequest
import ibm_appconfiguration.core.base_request as target


def mocked_base_requests(*args, **kwargs):
    class MockBaseResponse:
        def __init__(self, json_data, status_code):
            self.text = json_data
            self.status_code = status_code
            self.headers = dict()

        def json(self):
            return self.json_data

    if kwargs['url'] == 'http://python.test.sdk.com/test.json':
        return MockBaseResponse({"key1": "value1"}, 200)
    return MockBaseResponse(None, 404)


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.patcher = patch('ibm_appconfiguration.core.base_request.requests')
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_base_request(self):
        service = BaseRequest()
        header = {
            'Authorization': "apikey",
            'Content-Type': 'application/json'
        }
        target.requests.request.side_effect = mocked_base_requests

        request = service.prepare_request(
            method='GET',
            url='http://python.test.sdk.com/test.json',
            headers=header
        )

        response = service.send(request)
        status_code = response.get_status_code()
        self.assertEqual(status_code, 200)

        request = service.prepare_request(
            method='GET',
            url='http://python.test.sdk.com/testnone.json',
            headers=header
        )

        response = service.send(request)
        status_code = response.get_status_code()
        self.assertEqual(status_code, 404)


if __name__ == '__main__':
    unittest.main()
