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


import fcntl
import json
import os
from ibm_appconfiguration.core.internal import Logger
from typing import Optional


class FileManager:
    file_name = "appconfiguration-features.json"

    @classmethod
    def store_files(cls, json_data=dict()) -> bool:

        this_dir, _ = os.path.split(__file__)
        cache_loc = os.path.join(this_dir, cls.file_name)
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

        cache_loc = ''
        if file_path is not None:
            cache_loc = file_path
        else:
            this_dir, _ = os.path.split(__file__)
            cache_loc = os.path.join(this_dir, cls.file_name)

        try:
            with open(cache_loc, 'r') as cache:
                fcntl.flock(cache, fcntl.LOCK_EX | fcntl.LOCK_NB)
                data = json.load(cache)
                fcntl.flock(cache, fcntl.LOCK_UN)
                return data
        except Exception as err:
            Logger.debug(err)
            return None
