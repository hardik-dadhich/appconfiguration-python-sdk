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

import requests
from threading import Timer


class Connectivity:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Connectivity.__instance is None:
            return Connectivity()
        return Connectivity.__instance;

    def __init__(self):
        if Connectivity.__instance is not None:
            print("Connectivity class must be initialized using the get_instance() method")
        else:
            self.__listeners = list()
            Connectivity.__instance = self

    def add_connectivity_listener(self, listener):
        if callable(listener) and not self.__listeners.__contains__(listener):
            self.__listeners.append(listener)

    def check_connection(self):
        self.__check_network()
        Timer(30, lambda: self.check_connection()).start()

    def __check_network(self):
        url = 'https://cloud.ibm.com'
        try:
            _ = requests.head(url, timeout=3)
            for listener in self.__listeners:
                listener(True)
        except:
            for listener in self.__listeners:
                listener(False)
