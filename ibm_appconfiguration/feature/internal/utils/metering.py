#  IBM Confidential OCO Source Materials
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

from threading import Lock, Timer
from datetime import datetime
from ibm_appconfiguration.core import BaseRequest
from ..common import constants


class Metering:
    __send_interval = 600000
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Metering.__instance is None:
            return Metering()
        return Metering.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Metering.__instance is not None:
            raise Exception("Metering " + constants.SINGLETON_EXCEPTION)
        else:
            self.__metering_url = None
            self.__apikey = None
            self.__lock = Lock()
            self.__metering_data = dict()
            Metering.__instance = self
            self.__send_metering()

    def set_metering_url(self, url: str, apikey):
        self.__metering_url = url
        self.__apikey = apikey

    def add_metering(self, guid: str, collection_id: str, feature_id: str):
        self.__lock.acquire()
        try:
            time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            feature_json = {
                'count': 1,
                'evaluation_time': time
            }

            if guid in self.__metering_data:
                if collection_id in self.__metering_data[guid]:
                    if feature_id in self.__metering_data[guid][collection_id]:
                        self.__metering_data[guid][collection_id][feature_id]['evaluation_time'] = time
                        count = self.__metering_data[guid][collection_id][feature_id]['count']
                        self.__metering_data[guid][collection_id][feature_id]['count'] = count + 1
                    else:
                        self.__metering_data[guid][collection_id][feature_id] = feature_json
                else:
                    self.__metering_data[guid][collection_id] = {
                        feature_id: feature_json
                    }
            else:
                self.__metering_data[guid] = {
                    collection_id: {
                        feature_id: feature_json
                    }
                }
        finally:
            self.__lock.release()

    def __send_to_server(self, guid, data):
        service = BaseRequest()
        header = {
            'Authorization': self.__apikey,
            'Content-Type': 'application/json'
        }

        request = service.prepare_request(
            method='POST',
            url="{0}{1}/usage".format(self.__metering_url, guid),
            headers=header,
            data=data
        )
        service.send(request)

    def __send_metering(self):

        Timer(self.__send_interval, lambda: self.__send_metering()).start()
        self.__lock.acquire()
        try:
            send_metering_data = self.__metering_data
            self.__metering_data = dict()
        finally:
            self.__lock.release()

        if len(send_metering_data) <= 0:
            return

        result = dict()
        for kk, ee in send_metering_data.items():
            result[kk] = []
            for k1, e1 in ee.items():
                sub = {
                    'collection_id': k1,
                    'usages': []
                }
                for k2, e2 in e1.items():
                    feature_json = {
                        'feature_id': k2,
                        'evaluation_time': e2['evaluation_time'],
                        "count": e2['count']
                    }
                    sub['usages'].append(feature_json)
                result[kk].append(sub)
        for guid, values in result.items():
            for data in values:
                self.__send_to_server(guid=guid, data=data)
