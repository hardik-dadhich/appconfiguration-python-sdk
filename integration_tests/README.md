

## Requirement 
 
 Before running the commands, install the dev dependencies using the
 
 ```py
    pip install -r requirements-dev.txt
 ```
 
 # Run the Integration test

To run the integration test, you will need the appropriate service instance
   
   1. Go to the IBM Cloud Dashboard page. 
   2. Either click an existing App Configuration service instance or click Create resource > Developer Tools and create a service instance.
   3. Copy the guid and apikey from the Service credentials page.
   4. Create a new Environment or use the "dev".
   5. Create a collection named `appcompany` and copy the Id value.
   6. Add the above values to `.env` file.
   7. Follows the `user.json` file and create the given `Properties`, `Features` and `Segments`. Assign the correct values for each Feature and Property.
 
 Run the integration test with `python -m unittest discover -s integration_tests/`