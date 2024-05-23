# file_cloud_api_tests
The framework is designed to validate the following scenarios via file cloud API:

*Note*: Please update the `GUEST_USERNAME` and `GUEST_PASSWORD` details in `env\.env.secret` before proceed.

Refer this [swagger](https://fcapi.filecloud.com/?urls.primaryName=version%2023.1#/) for more details

## Install
1. Install the latest version of Python depending on the OS.
2. Clone this repository.
3. Create the virtual environment: `python -m venv venv`
4. Activate the virtual environment: `./venv/Scripts/Activate.ps1 ` in PowerShell.
5. Install the project dependencies by running `pip3 install -r requirements.txt`.

## About Framework

The following components and features are designed to perform as a robust framework:

### Env and Secrets
Separate `.env` files are maintained to keep credentials and commonly used variables.

### API_Classes
A single class entity to keep track of all endpoints.

### Pytest Fixture
Fixtures like `load_env`, `get_cookies`, and `get_common_data` support state dependency across multiple methods.

### Utilities
Supporting classes are designed for reading `json` and `.env` files.

### Hook
The Pytest hook `pytest_collection_modifyitems` is implemented to control the order of test case execution.

## List of Few Commands to Execute
1. `pytest -v -s` - By default, all tests are collected and the results will be printed in the console.
2. `pytest -k <keyword> -v` - Keyword can be a full or partial test method name.
3. `pytest --collect-only` - Only shows the list of all collected methods.
4. `pytest tests/ -v -s -m <mark>` - s stands for std.in, m stands for marker, v stands for more verbose.
5. `pytest tests/ --html=/reports/report.html` --self-contained-html - Generates an HTML report of the test results.

After successful execution, an HTML report will be generated.

By following this structure, the framework will help in organizing and executing API tests effectively while maintaining a clear and concise codebase.

