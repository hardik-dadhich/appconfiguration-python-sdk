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
from ibm_appconfiguration.configurations.models import Property, ConfigurationType


class MyTestCase(unittest.TestCase):
    sut = None

    def test_empty_property(self):
        sut = Property(dict())
        self.assertEqual(sut.get_property_name(), "")
        self.assertEqual(sut.get_property_id(), "")
        self.assertEqual(len(sut.get_segment_rules()), 0)
        self.assertEqual(sut.get_property_data_type(), ConfigurationType.NUMERIC)
        self.assertIsNotNone(sut.get_value())

    def test_property(self):
        property = {
            "name": "numericProperty",
            "property_id": "numericproperty",
            "description": "testing prop",
            "value": 10,
            "type": "NUMERIC",
            "tags": "test",
            "segment_rules": [
                {
                    "rules": [
                        {
                            "segments": [
                                "keuyclvf"
                            ]
                        }
                    ],
                    "value": 81,
                    "order": 1
                }
            ],
            "collections": [{
                "collection_id": "appcrash"
            }]
        }

        sut = Property(property)
        self.assertEqual(sut.get_property_name(), "numericProperty")
        self.assertEqual(sut.get_property_id(), "numericproperty")
        self.assertEqual(sut.get_value(), 10)
        self.assertEqual(sut.get_property_data_type(), ConfigurationType.NUMERIC)
        value = sut.get_current_value("id1", {"email": "test.dev@tester.com"})
        self.assertEqual(value, 10)


if __name__ == '__main__':
    unittest.main()
