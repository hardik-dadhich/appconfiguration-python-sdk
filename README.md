# IBM Cloud App Configuration Python server SDK

IBM Cloud App Configuration SDK is used to perform feature flag and property evaluation based on the configuration on IBM Cloud App Configuration service.

## Table of Contents

  - [Overview](#overview)
  - [Installation](#installation)
  - [Import the SDK](#import-the-sdk)
  - [Initialize SDK](#initialize-sdk)
  - [License](#license)

## Overview

IBM Cloud App Configuration is a centralized feature management and configuration service on [IBM Cloud](https://www.cloud.ibm.com) for use with web and mobile applications, microservices, and distributed environments.

Instrument your applications with App Configuration Python SDK, and use the App Configuration dashboard, CLI or API to define feature flags or properties, organized into collections and targeted to segments. Toggle feature flag states in the cloud to activate or deactivate features in your application or environment, when required. You can also manage the properties for distributed applications centrally.

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
from ibm_appconfiguration import AppConfiguration, Feature, Property, ConfigurationType
```
## Initialize SDK

```py
app_configuration_client = AppConfiguration.get_instance()
app_configuration_client.init(region='region',
               guid='guid',
               apikey='apikey')

## Initialize configurations 
app_configuration_client.set_context(collection_id='airlines-webapp',
                       environment_id='dev')

```

- region : Region name where the service instance is created. Use
  - `AppConfiguration.REGION_US_SOUTH` for Dallas
  - `AppConfiguration.REGION_EU_GB` for London
  - `AppConfiguration.REGION_AU_SYD` for Sydney
- guid : GUID of the App Configuration service. Get it from the service credentials section of the dashboard
- apikey : ApiKey of the App Configuration service. Get it from the service credentials section of the dashboard
- collection_id : Id of the collection created in App Configuration service instance.
- environment_id : Id of the environment created in App Configuration service instance.

### Work offline with local configuration file

SDK can work offline with a local configuration file and perform feature and property related operations.

```py
app_configuration_client.set_context(collection_id='airlines-webapp',
                       environment_id='dev',
                       configuration_file='saflights/flights.json',
                       live_config_update_enabled=False)
```
- configuration_file : Path to the JSON file which contains configuration details.
- live_config_update_enabled : Set this value to false if the new configuration values shouldn't be fetched from the server. Make sure to provide a proper JSON file in the configuration_file path. By default, this value is enabled.

### Permissions required by SDK
  Add the permission for `non-root` users for writing permission to use the cache and logs in AppConfiguration SDK.
  AppConfiguration cache location will be `./ibm_appconfiguration/configurations/internal/utils/appconfiguration.json`.
  The `logs.txt` file location will be the application root folder.

## Get single feature

```py
feature = app_configuration_client.get_feature('online-check-in') # feature can be null incase of an invalid feature id

if feature:
    print(f'Feature Name : {0}'.format(feature.get_feature_name()))
    print(f'Feature Id : {0}'.format(feature.get_feature_id()))
    print(f'Feature Type : {0}'.format(feature.get_feature_data_type()))
    print(f'Feature is enabled : {0}'.format(feature.is_enabled()))

```

## Get all features 

```py
features_dictionary = app_configuration_client.get_features()
```

## Evaluate a feature

Use the `feature.get_current_value(entity_id=entity_id, entity_attributes=entity_attributes)` method to evaluate the value of the feature flag. Pass an unique entityId as the parameter to perform the feature flag evaluation.

### Usage

  - If the feature flag is configured with segments in the AppConfiguration service, provide a json object as entityAttributes parameter to this method.

    ```py
    entity_id = "john_doe"
    entity_attributes = {
      'city': 'Bangalore',
      'country': 'India'
    }
    feature_value = feature.get_current_value(entity_id=entity_id,    entity_attributes=entity_attributes)
    ```

  - If the feature flag is not targeted to any segments and the feature flag is turned ON this method returns the feature enabled value. And when the feature flag is turned OFF this method returns the feature disabled value.

    ```py
    entity_id = "john_doe"
    feature_value = feature.get_current_value(entity_id=entity_id)
    ```

## Get single Property

```py
property = app_configuration_client.get_property('check-in-charges') # property can be null incase of an invalid property id
if property:
    print(f'Property Name : {0}'.format(property.get_property_name()))
    print(f'Property Id : {0}'.format(property.get_property_id()))
    print(f'Property Type : {0}'.format(property.get_property_data_type()))
```

## Get all Properties 

```py
properties_dictionary = app_configuration_client.get_properties()
```

## Evaluate a property

Use the `property.get_current_value(entity_id=entity_id, entity_attributes=entity_attributes)` method to evaluate the value of the property. Pass an unique entityId as the parameter to perform the property evaluation.

### Usage

- If the property is configured with segments in the App Configuration service, provide a json object as entityAttributes parameter to this method.
  
  ```py
  entity_id = "john_doe"
  entity_attributes = {
      'city': 'Bangalore',
      'country': 'India'
  }
  property_value = property.get_current_value(entity_id=entity_id, entity_attributes=entity_attributes)
  ```
- If the property is not targeted to any segments this method returns the property value.

  ```py
  entity_id = "john_doe"
  property_value = property.get_current_value(entity_id=entity_id)
  ```

## Set listener for the feature and property data changes

To listen to the data changes add the following code in the application.

```py
def configuration_update(self):
    print('Received updates on configurations')

app_configuration_client.register_configuration_update_listener(configuration_update)

```

## Fetch latest data

Fetch the latest configuration data. 

```py
app_configuration_client.fetch_configurations()
```

## Enable debugger (Optional)

Use this method to enable/disable the logging in SDK.
```py
app_configuration_client.enable_debug(True)
```

## Examples 

The [examples](https://github.com/IBM/appconfiguration-python-sdk/tree/master/examples) folder has the examples. 

## License

This project is released under the Apache 2.0 license. The license's full text can be found in [LICENSE](https://github.com/IBM/appconfiguration-python-sdk/blob/master/LICENSE)