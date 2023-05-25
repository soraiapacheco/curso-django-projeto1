Running only the functional test 
pytest 'functional_test' -rP

Disconsidering functional test and running others tests 
pytest -m "not functional_test" -rP