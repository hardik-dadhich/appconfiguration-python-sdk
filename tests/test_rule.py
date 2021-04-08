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

from __future__ import absolute_import

import unittest
from ibm_appconfiguration.feature.models import Rule


class MyTestCase(unittest.TestCase):
    sut = None

    def set_up_ends_with(self):
        values = ['in.ibm.com']
        rules = {
            'values': values,
            'operator': 'endsWith',
            'attribute_name': 'email'
        }
        self.sut = Rule(rules)

    def set_up_email(self, value):
        values = [value]
        rules = {
            'values': values,
            'operator': 'is',
            'attribute_name': 'creditValues'
        }
        self.sut = Rule(rules)

    def test_test_rules(self):
        self.set_up_ends_with()
        self.assertEqual(self.sut.get_attributes(), 'email')
        self.assertEqual(self.sut.get_operator(), 'endsWith')
        self.assertEqual(len(self.sut.get_values()), 1)
        self.assertNotEqual(self.sut.get_values()[0], 'in.test.com')
        self.assertEqual(self.sut.get_values()[0], 'in.ibm.com')

    def test_evaluation_ends_with_string(self):
        self.set_up_ends_with()
        client_attributes = {
            'email': 'tester@in.ibm.com'
        }
        self.assertTrue(self.sut.evaluate_rule(client_attributes))
        client_attributes = {
            'email': 'tester@in.ibm.error'
        }
        self.assertFalse(self.sut.evaluate_rule(client_attributes))

    def test_evaluation_ends_with_different_values(self):
        self.set_up_email("123")
        client_attributes = {
            'creditValues': '123'
        }
        self.assertTrue(self.sut.evaluate_rule(client_attributes))

        client_attributes = {
            'creditValues': False
        }
        self.set_up_email(False)
        self.assertTrue(self.sut.evaluate_rule(client_attributes))

        client_attributes = {
            'creditValues': 123
        }
        self.set_up_email(123)
        self.assertTrue(self.sut.evaluate_rule(client_attributes))

        client_attributes = {
            'creditValues': False
        }
        self.set_up_email("123")
        self.assertFalse(self.sut.evaluate_rule(client_attributes))

        self.set_up_email(123)
        self.assertFalse(self.sut.evaluate_rule(client_attributes))

        client_attributes = {
            'creditValues': False
        }
        self.set_up_email("False")
        self.assertFalse(self.sut.evaluate_rule(client_attributes))

        self.set_up_email(False)
        self.assertTrue(self.sut.evaluate_rule(client_attributes))


if __name__ == '__main__':
    unittest.main()
