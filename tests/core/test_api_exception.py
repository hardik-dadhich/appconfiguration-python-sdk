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
from ibm_appconfiguration.core.base_request import ApiException
from requests.models import Response


class MyTestCase(unittest.TestCase):

    def test_exception(self):

        response = Response()
        response.status_code = 404
        response._content = b'{ "message" : "Not Found" }'

        exception = ApiException(400, "Not Found", response)
        self.assertEqual(exception.__str__(), "Error: Not Found, Code: 400")
        self.assertEqual(ApiException._get_error_message(response), "Not Found")

        response._content = b'{ "error" : "Not Found" }'
        self.assertEqual(ApiException._get_error_message(response), "Not Found")

        response._content = b'{ "errorMessage" : "Not Found" }'
        self.assertEqual(ApiException._get_error_message(response), "Not Found")

        response._content = b'{ "text" : "Not Found" }'
        response.status_code = 401

        self.assertEqual(ApiException._get_error_message(response), "Unauthorized: Access is denied due to invalid credentials")

        response._content = b'{ "errors" : [{ "message" : "Not Found" }] }'
        self.assertEqual(ApiException._get_error_message(response), "Not Found")

        response._content = None
        self.assertEqual(ApiException._get_error_message(response), "Unknown error")


if __name__ == '__main__':
    unittest.main()
