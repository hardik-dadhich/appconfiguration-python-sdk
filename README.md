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
app_config = AppConfiguration.get_instance()
app_config.init(region=AppConfiguration.REGION_US_SOUTH,
               guid='GUID',
               apikey='APIKEY')

## Initialize configurations 
app_config.set_context(collection_id='collection_id',
                       environment_id='environment_id')

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
You can also work offline with local configuration file and perform feature and property related operations.

```py
app_config.set_context(collection_id='collection_id',
                       environment_id='environment_id',
                       configuration_file='custom/userJson.json',
                       live_config_update_enabled=True)
```
- configuration_file : Path to the JSON file which contains configuration details.
- live_config_update_enabled : Set this value to false if the new configuration values shouldn't be fetched from the server. Make sure to provide a proper JSON file in the configuration_file path. By default, this value is enabled.

## Get single feature

```py
feature = app_config.get_feature('feature_id')
if (feature) {
    print('Feature Name : {0}'.format(feature.get_feature_name()));
    print('Feature Id : {0}'.format(feature.get_feature_id()));
    print('Feature Type : {0}'.format(feature.get_feature_data_type()));
    print('Feature is enabled : {0}'.format(feature.is_enabled()));
}
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

## Get single Property

```py
property = app_config.get_property('property_id')
if (property) {
    print('Property Name : {0}'.format(property.get_property_name()));
    print('Property Id : {0}'.format(property.get_property_id()));
    print('Property Type : {0}'.format(property.get_property_data_type()));
}
```

## Get all Properties 

```py
properties_dictionary = app_config.get_properties()
```

## Evaluate a property

You can use the property.get_current_value(identity_id, identity_attributes) method to evaluate the value of the property. 

You should pass an unique identity_id as the parameter to perform the property evaluation. If the property is configured with segments in the App Configuration service, you can set the attributes values as a dictionary.

```py

identity_attributes = {
    'city': 'Bangalore',
    'country': 'India'
}
property_value = property.get_current_value(identity_id='identity_id', identity_attributes=identity_attributes)
```

## Set listener for the feature and property data changes

To listen to the data changes add the following code in your application.

```py
def configuration_update(self):
    print('Get your Feature/Property value now')

app_config.register_configuration_update_listener(configuration_update)

```

## Fetch latest data

```py
app_config.fetch_configurations()
```

## Enable debugger (Optional)

```py
app_config.enable_debug(True)
```

## License

This project is released under the Apache 2.0 license. The license's full text can be found in [LICENSE](https://github.com/IBM/appconfiguration-python-client-sdk/blob/master/LICENSE)
