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

import tkinter as tk
from ibm_appconfiguration import AppConfiguration, Feature, FeatureType
import config


class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.currentColl = config.COLLECTION
        self.currentmode = True
        self.__haData = False
        self.title("App Configuration sample")
        self.label_text = tk.StringVar()
        self.label_text.set('Get your Feature value after data is loaded')

        self.label = tk.Label(self, textvar=self.label_text)
        self.label.pack(fill=tk.BOTH, expand=1, padx=100, pady=30)

        hello_button = tk.Button(self, text="Get String Feature", command=lambda: self.fetch_feature('featurestring'))
        hello_button.pack(side=tk.LEFT, padx=(10, 20), pady=(0, 20))

        numberic_button = tk.Button(self, text="Get Numeric Feature",
                                    command=lambda: self.fetch_feature('featurenumeric'))
        numberic_button.pack(side=tk.LEFT, padx=(10, 20), pady=(0, 20))

        bool_button = tk.Button(self, text="Get Boolean Feature", command=lambda: self.fetch_feature('featurebool'))
        bool_button.pack(side=tk.LEFT, padx=(10, 20), pady=(0, 20))

        change_button = tk.Button(self, text="Change CollectionId", command=lambda: self.change_collection())
        change_button.pack(side=tk.LEFT, padx=(10, 20), pady=(0, 20))

        change_Offline = tk.Button(self, text="Change Offline mode", command=lambda: self.change_mode())
        change_Offline.pack(side=tk.RIGHT, padx=(10, 20), pady=(0, 20))

        self.initialize_app(collectionId=self.currentColl)

    def change_mode(self):
        if self.currentmode:
            self.currentmode = False
        else:
            self.currentmode = True

        self.initialize_app(collectionId=self.currentColl, isOnLine=self.currentmode)

    def change_collection(self):
        if self.currentColl == config.COLLECTION:
            self.currentColl = config.COLLECTION1
        else:
            self.currentColl = config.COLLECTION
        self.initialize_app(collectionId=self.currentColl, isOnLine=self.currentmode)

    def fetch_feature(self, feature_id: str):
        if self.__haData:
            self.label.configure(background="red")
            app_config = AppConfiguration.get_instance()
            feature = app_config.get_feature(feature_id)
            try:
                if feature:

                    identity = {
                        'city': 'Bangalore',
                        'country': 'India'
                    }
                    if feature.get_feature_data_type() == FeatureType.STRING:
                        val = feature.get_current_value("pvQr45", identity)
                        self.label_text.set(F"Your feature value is {val}")
                        self.configure(background="yellow")
                    elif feature.get_feature_data_type() == FeatureType.BOOLEAN:
                        val = feature.feature.get_current_value("pvQr45", identity)
                        self.label_text.set(F"Your feature value is {val}")
                        self.configure(background="green")
                    elif feature.get_feature_data_type() == FeatureType.NUMERIC:
                        val = feature.feature.get_current_value("pvQr45", identity)
                        self.label_text.set(F"Your feature value is {val}")
                        self.configure(background="black")
                else:
                    print("No feature")
            except Exception as err:
                print(err)

        else:
            self.label_text.set("Not loaded")
            self.label.configure(background="red")

    def response(self):
        self.__haData = True
        self.label_text.set('Get your Feature value NOW')

    def initialize_app(self, collectionId=str, isOnLine: bool = True):
        app_config = AppConfiguration.get_instance()
        app_config.init(region=AppConfiguration.REGION_US_SOUTH,
                        guid=config.GUID,
                        apikey=config.APIKEY)
        app_config.set_collection_id(collectionId)
        app_config.fetch_features_from_file(feature_file=config.FILE, live_feature_update_enabled=isOnLine)

        app_config.register_features_update_listener(self.response)


if __name__ == "__main__":
    window = Window()
    window.mainloop()
