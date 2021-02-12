# IBM Cloud App Configuration Python server SDK

IBM Cloud App Configuration SDK is used to perform feature evaluation based on the configuration on IBM Cloud App Configuration service.

## Table of Contents

  - [Overview](#overview)
  - [Installation](#installation)
  - [Import the SDK](#import-the-sdk)
  - [Initialize SDK](#initialize-sdk)
  - [License](#license)

## Overview

IBM Cloud App Configuration is a centralized feature management and configuration service on [IBM Cloud](https://www.cloud.ibm.com) for use with web and mobile applications, microservices, and distributed environments.

Instrument your applications with App Configuration Python SDK, and use the App Configuration dashboard or API to define features flags, organized into collections and targeted to segments. Change feature flag states in the cloud to activate or deactivate features in your application or environment, often without re-starting.

## Installation

To install, use `pip` or `easy_install`:
  
```sh
pip install --upgrade ibm-appconfiguration-python-sdk
```
or

```sh
 easy_install --upgrade ibm-appconfiguration-python-sdk
```
## Import the SDK

```py
from ibm_appconfiguration import AppConfiguration, Feature, FeatureType
```
## Initialize SDK

```py
app_config = AppConfiguration.get_instance()
app_config.init(region=AppConfiguration.REGION_US_SOUTH,
               guid='GUID',
               apikey='APIKEY')

## Initialize feature 
app_config.set_collection_id(collection_id='collection_id') 

## set the file or offline feature
app_config.fetch_features_from_file(feature_file='custom/userJson.json', # Add this field if liveFeatureUpdateEnabled false or get features when the device is offline during the first app load.
                                    live_feature_update_enabled=True) # This is for live update from server.

```

- region : Region name where the service instance is created. Eg: `AppConfiguration.REGION_US_SOUTH`
- guid : GUID of the App Configuration service. Get it from the service credentials section of the dashboard
- apikey : ApiKey of the App Configuration service. Get it from the service credentials section of the dashboard
* collection_id : Id of the collection created in App Configuration service instance.
* feature_file : Path to the JSON file which contains feature details and segment details.
* live_feature_update_enabled : Set this value to false if the new feature values shouldn't be fetched from the server. Make sure to provide a proper JSON file in the feature_file path. By default, this value is enabled.

## Set listener for feature data changes

```py
def features_update(self):
    print('Get your Feature value NOW')

app_config.register_features_update_listener(features_update)

```

## Get single feature

```py
feature = app_config.get_feature('feature_id')
```

## Get all features 

```py
features_dictionary = app_config.get_features()
```

## Evaluate a feature

You can use the feature.get_current_value(identity_id, identity_attributes) method to evaluate the value of the feature flag. 

You should pass an unique identity_id as the parameter to perform the feature flag evaluation. If the feature flag is configured with segments in the App Configuration service, you can set the attributes values as a dictionary.

```py

identity_attributes = {
    'city': 'Bangalore',
    'country': 'India'
}
feature_value = feature.get_current_value(identity_id='identity_id', identity_attributes=identity_attributes)
```

## Fetch latest data 

```py
app_config.fetch_feature_data()
```

## Enable debugger

```py
app_config.enable_debug(True)
```

## License

This project is released under the Apache 2.0 license. The license's full text can be found in [LICENSE](https://github.com/IBM/appconfiguration-python-client-sdk/blob/master/LICENSE)
