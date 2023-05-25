Running only the functional test 
pytest 'functional_test' -rP

Disconsidering functional test and running others tests 
pytest -m "not functional_test" -rP

Running only one test by name of test, for example:
pytest -k "test_recipe_home_without_recipes_not_found_message" -rP