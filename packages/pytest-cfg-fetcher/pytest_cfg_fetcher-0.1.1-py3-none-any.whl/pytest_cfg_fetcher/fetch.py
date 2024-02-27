"""
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

"""
import inspect, json, os

def fetch_config(test):
    """
    Fetch config for a particular test, or return None.
    Args:
    - test: name of test, corresponds to key in _test-config/config.json
    Returns:
    - dict object, config opts for test
    """
    def _caller_path():
        """
        gets path of the file that calle fetch_config.
        """
        for frame in inspect.stack():
            if 'fetch_config' in frame.code_context[0]:
                return os.path.dirname(frame.filename)
    try:
        test_path = _caller_path()
        with open(f"{test_path}/_test-config/config.json", 'r') as j:
            d = json.load(j)
            config = d[test]
            config['test_out_dir'] = d['test_out_dir']
        return config
    except:
        return None


"""
Usage:
```

from pytest_cfg_fetcher.fetch import fetch_config
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
```
"""
