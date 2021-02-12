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


import unittest
from ibm_appconfiguration import AppConfiguration

class MyTestCase(unittest.TestCase):
    def test_configuration(self):
        sut1 = AppConfiguration.get_instance()
        sut2 = AppConfiguration.get_instance()
        self.assertEqual(sut1, sut2)
        # self.assertFalse(sut1.getinitValues())
        # self.assertFalse(sut2.getinitValues())
        # sut2.init('re','rr','rr')
        # self.assertTrue(sut2.getinitValues())
        # self.assertTrue(sut1.getinitValues())

if __name__ == '__main__':
    unittest.main()
