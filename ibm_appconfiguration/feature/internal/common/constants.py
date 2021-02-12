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


REGION_ERROR = "Provide a valid region in App Configuration init"
GUID_ERROR = "Provide a valid guid in App Configuration init"
APIKEY_ERROR = "Provide a valid apiKey in App Configuration init"
COLLECTION_ID_VALUE_ERROR = "Provide a valid collection_id in App Configuration set_collection_id method"
COLLECTION_ID_ERROR = "Invalid action in App Configuration. This action can be performed only after a successful " \
                      "initialization. Please check the initialization section for errors. "
COLLECTION_SUB_ERROR = "Invalid action in App Configuration. This action can be performed only after a successful " \
                       "initialization and set collection_id value operation. Please check the initialization and " \
                       "set_collection_id sections for errors. "
FEATURE_FILE_NOT_FOUND_ERROR = "feature_file parameter should be provided while live_feature_update_enabled is false " \
                               "during initialization "
FEATURE_HANDLER_INIT_ERROR = 'Invalid action in FeatureHandler. This action can be performed only after a successful ' \
                             'initialization. Please check the initialization section for errors. '
FEATURE_HANDLER_METHOD_ERROR = "Invalid action in FeatureHandler. Should be a method/function"
FEATURE_API_ERROR = "Invalid configuration. Verify the collectionId, apikey, guid and region."
SINGLETON_EXCEPTION = "class must be initialized using the get_instance() method."
FEATURE_INVALID = "Invalid feature_id - "
