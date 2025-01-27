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
import os
import time
import responses
from ibm_appconfiguration import Property, Feature
from ibm_appconfiguration.configurations.configuration_handler import ConfigurationHandler
from ibm_appconfiguration.configurations.internal.utils.metering import Metering
from ibm_appconfiguration.configurations.internal.utils.url_builder import URLBuilder


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.responses = responses.RequestsMock()
        self.responses.start()
        self.addCleanup(self.responses.stop)
        self.addCleanup(self.responses.reset)
        self.sut = ConfigurationHandler.get_instance()
        self.sut.load_data()
        self.sut.init("apikey", "guid", "region", None)
        FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user.json')
        self.sut.set_context("collectionId", "environmentId", FILE, False)
        self.sut.load_data()
        time.sleep(2.5)

    def tearDown(self):
        self.sut = None

    def test_load_from_web(self):
        Metering.get_instance().set_repeat_calls(False)
        URLBuilder.set_auth_type(False)
        mock_response = '''
            {
                "features": [
                    {
                        "name": "featurestring",
                        "feature_id": "featurestring",
                        "type": "STRING",
                        "enabled_value": "Hello",
                        "disabled_value": "Hi",
                        "segment_rules": [],
                        "enabled": true
                    }
                ],
                "properties": [
                    {
                        "name": "numericproperty",
                        "property_id": "numericproperty",
                        "tags": "",
                        "type": "NUMERIC",
                        "value": 30,
                        "segment_rules": [],
                        "created_time": "2021-05-23T08:00:56Z",
                        "updated_time": "2021-05-23T08:00:56Z"
                    }
                ],
                "segments": []
            }
        '''
        url = 'https://cloud.ibm.com/apprapp/feature/v1/instances/guid/collections/collection_id/config?environment_id=environment_id'
        self.responses.add(responses.GET,
                           url,
                           body=mock_response,
                           content_type='application/json',
                           status=200)
        self.sut.init("apikey", "guid", "region", "https://cloud.ibm.com")
        self.sut.set_context("collection_id", "environment_id", None, True)
        self.sut.load_data()
        features = self.sut.get_features()
        self.assertEqual(len(features), 1)

    def test_evaluate_property(self):
        property_json = {
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
        property_obj = Property(property_json)
        value = self.sut.property_evaluation(property_obj, "id1", {"email": "test.dev@tester.com"})
        self.assertEqual(value, 81)

        value = self.sut.property_evaluation(property_obj, "id1", {"email": "test@f.com"})
        self.assertEqual(value, 10)

        value = self.sut.property_evaluation(property_obj, "id1", {})
        self.assertEqual(value, 10)

    def test_evaluate_feature(self):
        feature_json = {
            "name": "defaultFeature",
            "feature_id": "defaultfeature",
            "type": "STRING",
            "enabled_value": "hello",
            "disabled_value": "Bye",
            "segment_rules": [
                {
                    "rules": [
                        {
                            "segments": [
                                "kg92d3wa"
                            ]
                        }
                    ],
                    "value": "Welcome",
                    "order": 1
                }
            ],
            "segment_exists": True,
            "enabled": True
        }
        feature_obj = Feature(feature_json)
        value = self.sut.feature_evaluation(feature_obj, "id1", {"email": "test.dev@tester.com"})
        self.assertEqual(value, "Welcome")

        value = self.sut.feature_evaluation(feature_obj, "id1", {"email": "test@tester.com"})
        self.assertEqual(value, "hello")

        value = self.sut.feature_evaluation(feature_obj, "id1", {})
        self.assertEqual(value, "hello")

    def test_get_methods(self):
        feature = self.sut.get_feature("defaultfeature")
        self.assertEqual(feature.get_feature_id(), "defaultfeature")

        features = self.sut.get_features()
        self.assertEqual(len(features), 3)

        property_obj = self.sut.get_property("numericproperty")
        self.assertEqual(property_obj.get_property_id(), "numericproperty")

        properties = self.sut.get_properties()
        self.assertEqual(len(properties), 1)


if __name__ == '__main__':
    unittest.main()
