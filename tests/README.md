# Run for Code coverage 

1. pip install coverage
2. coverage run --source=./ibm_appconfiguration/ -m unittest discover -s tests
3. coverage report -m
4. coverage html

Results will be available in `htmlcov` folder