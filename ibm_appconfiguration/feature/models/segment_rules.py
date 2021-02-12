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

class SegmentRules:
    """
       Attributes:
        segment_rules (dict): segment_rules JSON object that contains all the SegmentRules
   """

    def __init__(self, segment_rules=dict()):

        self.__order = segment_rules.get("order", 1)
        self.__value = segment_rules.get("value", object)
        self.__rules = segment_rules.get("rules", list())

    def get_order(self) -> int:
        return self.__order

    def get_rules(self) -> list:
        return self.__rules

    def get_value(self):
        return self.__value
