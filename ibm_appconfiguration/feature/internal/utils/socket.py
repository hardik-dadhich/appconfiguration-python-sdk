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

import websocket
import ssl

try:
    import thread
except ImportError:
    import _thread as thread


class Socket(object):

    def __init__(self, url, headers, callback):
        self.__callback = callback
        self.ws_client = websocket.WebSocketApp(
            url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            header=headers
        )
        self.ws_client.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def on_message(self, message):
        if message == 'test message':
            return
        self.__callback(message=message)

    def on_error(self, error):
        self.__callback(error_state=error)
        self.ws_client.close()

    def on_close(self):
        self.__callback(closed_state='Closed the web_socket')

    def on_open(self):
        self.__callback(open_state='Opened the web_socket')

    def cancel(self):
        self.ws_client.close()
