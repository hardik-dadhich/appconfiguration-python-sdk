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


def remove_null_values(dictionary: dict) -> dict:
    """Create a new dictionary without keys mapped to null values.

    Args:
        dictionary: The dictionary potentially containing keys mapped to values of None.

    Returns:
        A dict with no keys mapped to None.
    """
    if isinstance(dictionary, dict):
        return {k: v for (k, v) in dictionary.items() if v is not None}
    return dictionary
