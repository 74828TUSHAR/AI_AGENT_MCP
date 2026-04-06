# Test-Specific Logging System

## Overview

The framework now uses **test-specific logging** where each test file generates its own separate log file. This makes it easier to track logs for individual test modules.

## How It Works

### Log File Naming Convention

Each test file generates a corresponding log file with the pattern:

```
<test_file_name>_test.log
```

**Examples:**

- `test_login_authentication.py` → `logs/login_authentication_test.log`
- `test_registration.py` (future) → `logs/registration_test.log`
- `test_dashboard_flow.py` (future) → `logs/dashboard_flow_test.log`

### Append Mode

- **First Run**: If the log file doesn't exist, it will be **created** automatically
- **Subsequent Runs**: New logs will be **appended** to the existing file

## File Structure

```
project_playwright/
├── logs/
│   ├── login_authentication_test.log    # Created from test_login_authentication.py
│   ├── registration_test.log            # (Future) From test_registration.py
│   └── dashboard_flow_test.log          # (Future) From test_dashboard_flow.py
├── tests/
│   ├── test_login_authentication.py     # Login tests (2 methods)
│   ├── test_registration.py             # (Future)
│   └── test_dashboard_flow.py           # (Future)
└── conftest.py                          # pytest hook that configures test-specific logging
```

## Log Format

Each log entry includes:

- **Timestamp**: Date and time of the log entry
- **Log Level**: INFO, DEBUG, ERROR, etc.
- **Module Name**: Test module where the log was generated
- **Function Name**: Test function that generated the log
- **Line Number**: Line number in the test file where the log was triggered
- **Message**: The actual log message

**Example Log Line:**

```
2026-04-05 22:37:13 [    INFO] test_login_authentication - test_login_with_invalid_password:330 - Current URL: https://automationexercise.com/login
                                ↑                           ↑                                  ↑
                                Module Name              Function Name                   Line Number
```

## Usage Examples

### Running Login Tests

```bash
python -m pytest tests/test_login_authentication.py
```

**Output Log File:** `logs/login_authentication_test.log`

### Running Registration Tests (Future)

```bash
python -m pytest tests/test_registration.py
```

**Output Log File:** `logs/registration_test.log`

### Running All Tests

```bash
python -m pytest tests/
```

**Output Log Files:** Multiple test-specific log files in `logs/` directory

### Running Tests Multiple Times

```bash
# First run
python -m pytest tests/test_login_authentication.py
# Creates: logs/login_authentication_test.log

# Second run
python -m pytest tests/test_login_authentication.py
# Appends to: logs/login_authentication_test.log (doesn't overwrite)
```

## Configuration

The test-specific logging is configured in [conftest.py](conftest.py) using the `pytest_runtest_setup` hook:

```python
def pytest_runtest_setup(item):
    # Extracts test module name
    # Creates logs directory if it doesn't exist
    # Sets up file handler with APPEND mode (mode='a')
    # Configures formatter with timestamp, function name, and line number
```

## Log Console Output

In addition to file logging, the framework also displays INFO and above logs to the console during test execution for immediate visibility.

## Benefits

✅ **Organized**: Each test file has its own log file  
✅ **Non-Destructive**: Logs are appended, never overwritten  
✅ **Traceable**: Includes function name and line number for each entry  
✅ **Scalable**: Easy to add new test files - logging is automatic  
✅ **Secure**: Credentials are masked with asterisks (e.g., `*****************`)  
✅ **Detailed**: Includes timestamps and log levels for debugging

## File Growth

The log files grow with each test run. For large test suites, periodically archive or clear old logs:

```bash
# To clear a test log file (Windows PowerShell)
Remove-Item logs/login_authentication_test.log

# Logs will be recreated on next test run
python -m pytest tests/test_login_authentication.py
```

## Integration with CI/CD

For Jenkins or other CI/CD systems:

- Logs are saved in a predictable location: `logs/<test_name>_test.log`
- Use these logs for test result analysis and debugging
- Reference specific line numbers in error reports
- Each test run appends to the log, creating a historical record
