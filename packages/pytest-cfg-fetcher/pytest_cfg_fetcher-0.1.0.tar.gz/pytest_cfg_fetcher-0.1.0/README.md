# pytest-cfg-fetcher

Unit tests don't take arguments. Sometimes we like to pass an arg or two, e.g. you want to write test results to a file when running locally. This is a simple function to do that.

pytestconfig assumes you have a directory called `_test-config/` in the same directory as your unit tests, e.g. under `test/`. The `_test-config/` dir contains a `config.json` file/

`_test-config/config.json` contians minimally:

    {
        "test_out_path": <path>
    }

which is a local path where you might want to write output for tests.

The `fetch_config()` function takes a single argument, which should be the name of the test that calls it -- the return value is a dict object containing the test_out_path and whatever else you want to pass into your unit tests.

    {
        "test_out_path": "test/_test-result",
        "my_test" {
            "my_test_bool_opt": true,
            "my_test_str_opt": "stringalingting"
        }
    }

## Installation

	pip install pytest-cfg-fetcher

## Usage
```python
# mytest.py
from pytest-cfg-fetcher.fetch import fetch_config
import unittest

class Test(unittest.TestCase):

    def test_import(self):
        config = fetch_config("my_test")
        ...
        testy stuf
        ...
        test_result = "results of test"
        if config and config['my_test_bool_opt']:
            with open(f"{config['test_out_path']}/{config['my_test_str_opt']}.txt", "w+") as out:
                out.write(test_result)

if __name__ == '__main__':
    unittest.main()
