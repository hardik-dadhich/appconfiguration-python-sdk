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

"""
This module provides methods that perform the store and retrieve operations on the
file based cache of the SDK.
"""

import fcntl
import json
import os
from typing import Optional
from .logger import Logger


class FileManager:
    """FileManager to handle the cache"""

    @classmethod
    def store_files(cls, json_data: {}, file_path: Optional[str] = None) -> bool:
        """Store the file

        Args:
            json_data: Data to be stored.
            file_path: File path for the cache.
        """
        cache_loc = ''
        if file_path is not None:
            cache_loc = file_path
        else:
            cache_loc = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'appconfiguration.json')
        try:
            with open(cache_loc, 'w') as cache:
                fcntl.flock(cache, fcntl.LOCK_EX | fcntl.LOCK_NB)
                json.dump(json_data, cache)
                fcntl.flock(cache, fcntl.LOCK_UN)
                return True
        except Exception as err:
            Logger.debug(err)
            return False

    @classmethod
    def read_files(cls, file_path: Optional[str] = None) -> dict:
        """
        Read the data from the cache.

        Args:
            file_path: File path for the cache.
        Returns:
            Dictionary from the cache.
        """
        cache_loc = ''
        if file_path is not None:
            cache_loc = file_path
        else:
            cache_loc = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'appconfiguration.json')

        try:
            with open(cache_loc, 'r') as cache:
                fcntl.flock(cache, fcntl.LOCK_EX | fcntl.LOCK_NB)
                data = json.load(cache)
                fcntl.flock(cache, fcntl.LOCK_UN)
                return data
        except Exception as err:
            Logger.debug(err)
            return None
