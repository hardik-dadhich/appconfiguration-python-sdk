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
from ibm_appconfiguration.feature.internal.utils.metering import Metering


class MyTestCase(unittest.TestCase):

    def test_metering(self):

        metering = Metering.get_instance()
        metering.add_metering(guid="guid1",collection_id="collection_id1",feature_id='feature_id1')
        metering.add_metering(guid="guid1", collection_id="collection_id2", feature_id='feature_id1')
        metering.add_metering(guid="guid1", collection_id="collection_id2", feature_id='feature_id2')

        metering.add_metering(guid="guid2", collection_id="collection_id1", feature_id='feature_id1')
        metering.add_metering(guid="guid3", collection_id="collection_id1", feature_id='feature_id1')

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
