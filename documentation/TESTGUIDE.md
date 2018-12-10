# Running tests in Foundations

Each module within Foundations ([foundations_sdk](../foundations_sdk), [foundations_contrib](../foundations_contrib), [foundations_internal](../foundations_contrib), [foundations_rest_api](../foundations_rest_api) and [foundations_ui](../foundations_ui)) has their own set of unit tests and integration tests.

To run these tests, first build Foundations. In the foundations [root directory](../), run

```
./build.sh
```


To run unit and integration tests, navigate to the desired module source folder (ie. `foundations_<module_name>/ src`)  and run:

For **unit** tests
```
python -m unittest test
```

For **integration** tests
```
python -m unittest integration
```


_If you make changes to code outside the module you're running tests in (ie. if you're running tests in `foundations_sdk` and just changed a file in `foundations_contrib` that `foundations_sdk` uses), you'll have to rebuild before running tests again._


To run **acceptance** tests for `foundations_sdk`, `foundations_contrib`, and `foundations_internal`, navigate to the [foundations/testing](../testing) folder and run
```
python -m unittest acceptance
```

_If you make changes to code in any of the `foundations_sdk`, `foundations_contrib`, or `foundations_internal` modules, rebuild before running the acceptance tests again._


To run **acceptance** tests for `foundations_rest_api`, go to the [`foundations/foundations_rest_api/src`](../foundations/foundations_rest_api/src) folder and run:
```
python -m unittest acceptance
```


