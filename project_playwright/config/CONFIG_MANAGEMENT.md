# Enterprise Configuration Management System

## Overview

This document describes the enterprise-grade configuration management system for the Playwright QA Automation Framework. The system supports multiple environments (DEV, QA, STAGE, PROD) with dynamic array/server targeting.

---

## Architecture

### Components

1. **env.yaml** - Central configuration file containing all environment and array definitions
2. **config.py** - Basic configuration loader (backward compatible)
3. **config_loader.py** - Environment-based config loader (backward compatible)
4. **array_config.py** - Advanced array/server configuration manager (NEW)
5. **conftest.py** - Updated fixtures with array config integration
6. **logger.py** - Enhanced logging with context tracking

---

## Configuration Structure

### Environment Configuration

Each environment (dev, qa, stage, prod) includes:

```yaml
environment_name:
  description: "Environment Description"
  base_url: "https://example.com"
  api_base_url: "https://api.example.com"
  window:
    mode: "maximized" # maximized, fullscreen, minimized, custom
    width: 1280 # used only when mode = custom
    height: 720
  username: "user@example.com"
  password: "password"
  arrays: # Array/Server definitions
    default: { ... } # Default array when none specified
    array_01: { ... } # Additional arrays
    array_02: { ... }
```

### Array Configuration

Each array includes:

```yaml
array_key:
  name: "ARRAY-NAME" # Display name
  ip: "192.168.1.10" # Server IP address
  port: 8080 # Server port
  protocol: "http" # http or https
```

---

## Usage Guide

### 1. Basic Usage (Backward Compatible)

Existing tests continue to work without modification:

```python
@pytest.mark.asyncio
async def test_example(page, env, api_client):
    """
    Traditional fixture usage - fully compatible with existing tests.
    """
    base_url = env.get("base_url")
    await page.goto(base_url)
```

### 2. Using Array Configuration (New)

#### In Fixtures

```python
@pytest.fixture
def test_setup(array_config_manager, array_info):
    """
    Access array configuration in fixtures.
    """
    # Get selected array
    array = array_config_manager.get_selected_array()
    print(f"Testing against: {array['name']} at {array['ip']}")

    # Get connection string
    conn_str = array_config_manager.get_array_connection_string()
    # Output: "https://192.168.1.10:443"

    yield
```

#### In Test Functions

```python
@pytest.mark.asyncio
async def test_with_array(array_info, api_client):
    """
    Use array_info fixture to access array details.
    """
    array_ip = array_info["ip"]
    array_port = array_info["port"]
    array_name = array_info["name"]

    # Use in assertions or test logic
    assert array_info["protocol"] == "https"
```

### 3. Dynamic Array Switching

```python
@pytest.mark.asyncio
async def test_multiple_arrays(array_config_manager):
    """
    Switch between arrays during test execution.
    """
    # Get manager
    mgr = array_config_manager

    # Current array
    current = mgr.get_selected_array()
    print(f"Current: {current['name']}")

    # Switch to array_02
    mgr.set_selected_array("array_02")
    new_current = mgr.get_selected_array()
    print(f"Switched to: {new_current['name']}")

    # Get connection string for new array
    url = mgr.get_array_url("/api/health")
    # Output: "https://192.168.1.11:443/api/health"
```

### 4. Getting Available Arrays

```python
@pytest.mark.asyncio
async def test_array_iteration(array_config_manager):
    """
    Iterate through all available arrays for an environment.
    """
    mgr = array_config_manager

    # Get all arrays
    all_arrays = mgr.get_available_arrays()

    for array_key, array_config in all_arrays.items():
        print(f"{array_key}: {array_config['name']} at {array_config['ip']}")
```

---

## Environment Variables

### Core Environment Variables

| Variable        | Description          | Default     | Example                |
| --------------- | -------------------- | ----------- | ---------------------- |
| `ENV`           | Target environment   | `qa`        | `ENV=dev`, `ENV=stage` |
| `ARRAY`         | Target array key     | `default`   | `ARRAY=array_01`       |
| `HEADLESS`      | Run browser headless | `false`     | `HEADLESS=true`        |
| `WINDOW_MODE`   | Browser window mode  | `maximized` | `WINDOW_MODE=custom`   |
| `WINDOW_WIDTH`  | Custom window width  | `1280`      | `WINDOW_WIDTH=1920`    |
| `WINDOW_HEIGHT` | Custom window height | `720`       | `WINDOW_HEIGHT=1080`   |
| `LOG_DIR`       | Log output directory | `logs`      | `LOG_DIR=test_logs`    |

### Usage Examples

```bash
# Run tests against DEV with array_02
ENV=dev ARRAY=array_02 pytest tests/

# Run tests against STAGE with custom window size and headless
ENV=stage HEADLESS=true WINDOW_MODE=custom WINDOW_WIDTH=1920 WINDOW_HEIGHT=1080 pytest tests/

# Run tests against PROD with specific log directory
ENV=prod LOG_DIR=/var/logs/automation pytest tests/

# Run tests against QA (default)
pytest tests/
```

---

## Logging System

### Enhanced Logging Features

1. **Execution Context Tracking** - Environment, array, and test name are logged with each message
2. **Structured Output** - Consistent formatting for easy parsing and analysis
3. **File & Console Output** - Separate log files per test module with console mirror
4. **Test Lifecycle Logging** - Automatic logging of test start, pass, fail, skip

### Log Format

```
2024-05-24 10:15:30 | INFO     | DEV    | [array_01]       | test_module | Test execution started
2024-05-24 10:15:32 | INFO     | DEV    | [array_01]       | utils.logger | [ARRAY-CONFIG] Initialized for environment: dev
2024-05-24 10:15:33 | ERROR    | DEV    | [array_01]       | test_module | Test failed: AssertionError
```

### Using Logger in Tests

```python
from utils.logger import get_logger

logger = get_logger(__name__)

def test_with_logging():
    logger.info("Test execution started")
    logger.debug("Detailed debugging information")
    logger.warning("Warning message")
    logger.error("Error occurred")

    # Context is automatically added by conftest
    # Logs will show environment and array information
```

---

## Advanced Features

### 1. Array Connection Strings

```python
# Get base connection string
conn_str = mgr.get_array_connection_string()  # "https://192.168.1.10:443"

# Get full URL with endpoint
url = mgr.get_array_url("/api/products")     # "https://192.168.1.10:443/api/products"
url = mgr.get_array_url("health")            # "https://192.168.1.10:443/health"
```

### 2. Credentials Management

```python
creds = mgr.get_credentials()
username = creds["username"]
password = creds["password"]
```

### 3. Window Configuration

```python
window = mgr.get_window_config()
mode = window.get("mode")
width = window.get("width")
height = window.get("height")
```

### 4. Configuration Summary

```python
# Get full environment and array summary
summary = mgr.get_summary()
# Returns dict with environment, arrays, base URLs, selected array details

# Log comprehensive environment info
mgr.log_environment_info()
# Outputs detailed environment and array configuration to logs
```

---

## Array Specifications

### Available IP Addresses

The framework simulates realistic private IP network infrastructure:

| IP Address   | Use Case             | Environments               |
| ------------ | -------------------- | -------------------------- |
| 192.168.1.10 | Primary/Master Array | All (default)              |
| 192.168.1.11 | Secondary Array      | All (array_02)             |
| 192.168.1.12 | Tertiary Array       | QA, STAGE, PROD (array_03) |

### Port Configuration

| Port | Protocol | Use Case        |
| ---- | -------- | --------------- |
| 8080 | HTTP     | DEV environment |
| 443  | HTTPS    | QA, STAGE, PROD |

---

## Framework Scalability

### Supported Automation Tools

The configuration system is designed to support:

1. **Playwright** - Web UI automation (current)
2. **Selenium** - WebDriver-based automation
3. **API Testing** - REST/GraphQL API automation
4. **Mobile Testing** - Appium-based mobile testing

### Extensibility

To add new environments or arrays:

1. **Edit config/env.yaml**

   ```yaml
   new_env:
     description: "New Environment"
     base_url: "https://new.example.com"
     api_base_url: "https://api.new.example.com"
     # ... other config ...
     arrays:
       default:
         name: "NEW-ARRAY-01"
         ip: "192.168.x.x"
         port: 443
         protocol: "https"
   ```

2. **Set environment variable**

   ```bash
   ENV=new_env pytest tests/
   ```

3. **Access in tests**
   ```python
   async def test_new_env(array_config_manager):
       array = array_config_manager.get_selected_array()
   ```

---

## Best Practices

### 1. Environment Selection

- **DEV**: For local development and rapid iteration
- **QA**: For comprehensive quality assurance
- **STAGE**: For pre-production validation
- **PROD**: For production verification (use with caution)

### 2. Array Targeting

- Use `default` array for standard test execution
- Switch arrays for:
  - Load distribution testing
  - Array failover validation
  - Multi-array synchronization testing

### 3. Logging Usage

```python
logger.info("Starting user login flow")     # Expected flow
logger.warning("Retry attempt 2 of 3")      # Expected but noteworthy
logger.error("Critical failure occurred")   # Unexpected error
```

### 4. Configuration Reuse

Use the existing config module in API clients, page objects, and utilities:

```python
from config.array_config import get_array_manager

class ApiClient:
    def __init__(self):
        mgr = get_array_manager()
        self.base_url = mgr.get_api_base_url()
        self.array = mgr.get_selected_array()
```

---

## Troubleshooting

### Issue: "Environment 'x' not found"

**Solution**: Verify environment variable is set correctly

```bash
# List available environments
grep "^[a-z]:" config/env.yaml

# Set correct environment
ENV=qa pytest tests/
```

### Issue: "Array key 'x' not found"

**Solution**: Verify array name in configuration

```bash
# View arrays for environment
grep -A20 "arrays:" config/env.yaml | grep "^\s*[a-z]"

# Use correct array
ARRAY=array_01 pytest tests/
```

### Issue: Missing context in logs

**Solution**: Ensure conftest.py is in test root directory and fixtures are used

```python
# Correct
def test_example(array_config_manager, array_info):
    pass

# Incorrect (no fixtures, no context)
def test_example():
    pass
```

---

## Migration Guide

### From Old Config to New System

**Old Code** (still works):

```python
def test_example(env, api_client):
    base_url = env.get("base_url")
```

**New Code** (recommended):

```python
def test_example(array_config_manager, array_info):
    base_url = array_config_manager.get_base_url()
    array_ip = array_info["ip"]
```

**Gradual Migration**: Both old and new approaches work simultaneously, allowing incremental migration.

---

## API Reference

### ArrayConfigManager Class

#### Methods

```python
# Initialization
mgr = ArrayConfigManager(environment="qa")

# Array Selection
mgr.get_selected_array() -> Dict
mgr.set_selected_array(array_key) -> Dict
mgr.get_array(array_key) -> Dict
mgr.get_available_arrays() -> Dict

# URL Building
mgr.get_array_connection_string() -> str
mgr.get_array_url(endpoint, array_key) -> str

# Configuration Access
mgr.get_environment() -> str
mgr.get_environment_config() -> Dict
mgr.get_base_url() -> str
mgr.get_api_base_url() -> str
mgr.get_credentials() -> Dict
mgr.get_window_config() -> Dict

# Logging & Reporting
mgr.log_environment_info() -> None
mgr.get_summary() -> Dict
```

---

## Version History

| Version | Date       | Changes                                                      |
| ------- | ---------- | ------------------------------------------------------------ |
| 2.0     | 2024-05-24 | Added array configuration, DEV environment, enhanced logging |
| 1.0     | 2024-01-01 | Initial configuration system                                 |

---

## Support & Questions

For questions or issues with the configuration system, please refer to:

- Array configuration examples in test files
- conftest.py fixture definitions
- array_config.py inline documentation
