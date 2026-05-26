# Playwright QA Automation Framework - Enterprise Edition

## 📋 Overview

A professional, enterprise-grade QA automation framework built with Playwright, Python, and pytest. Designed for testing complex applications across multiple environments and server arrays.

**Version**: 2.0 (Enterprise Edition with Multi-Environment & Array Support)

---

## 🎯 Key Features

### ✨ Enterprise Configuration Management

- **Multi-Environment Support**: DEV, QA, STAGE, PROD
- **Array/Server Targeting**: Dynamic selection of 3-4 arrays per environment
- **Environment Variables**: Dynamic configuration via ENV and ARRAY variables
- **Realistic IP Simulation**: Private IP network infrastructure (192.168.1.x)

### 🚀 Advanced Automation Capabilities

- **Playwright Web Automation**: Async/await based browser automation
- **REST API Testing**: Built-in API client with comprehensive logging
- **Data-Driven Testing**: JSON-based test data management
- **Modular Architecture**: Page objects, utilities, flows for code reuse

### 📊 Enterprise-Grade Logging

- **Structured Logging**: Environment and array context in every log message
- **Test Lifecycle Tracking**: Automatic logging of test start, pass, fail, skip
- **File & Console Output**: Separate log files per test module
- **Colored & Formatted**: Professional log output for analysis

### 🏗️ Scalable Framework Design

- **100% Backward Compatible**: Existing tests work without modification
- **Gradual Enhancement**: Optional adoption of new features
- **Extensible Architecture**: Ready for Selenium, mobile testing, and more
- **Clean Code Standards**: DRY principle, modular design, proper documentation

---

## 📁 Project Structure

```
project_playwright/
├── config/                          # ⭐ Configuration Management
│   ├── __init__.py
│   ├── config.py                   # Basic config loader
│   ├── config_loader.py            # Environment-based loader
│   ├── array_config.py             # ⭐ NEW: Advanced array/server manager
│   ├── env.yaml                    # ⭐ Enhanced: Multi-env & array configs
│   ├── database.yaml               # Database configuration
│   └── CONFIG_MANAGEMENT.md        # ⭐ NEW: Complete config guide
│
├── core/                            # Core Framework Components
│   ├── api_client.py               # REST API client with logging
│   └── ...
│
├── pages/                           # Page Object Models
│   ├── home_page.py
│   ├── login_page.py
│   ├── cart_page.py
│   └── ...
│
├── tests/                           # Test Suites
│   ├── UI/                         # UI/Browser Tests
│   │   ├── test_case_01_register_user.py
│   │   ├── test_case_02_login_valid.py
│   │   └── ...
│   └── API/                        # API Tests
│       ├── nightly/
│       ├── regression/
│       └── ...
│
├── utils/                           # Reusable Utilities
│   ├── logger.py                   # ⭐ Enhanced: Context-aware logging
│   ├── api_client.py               # API request wrapper
│   ├── api_assertions.py           # API assertion helpers
│   ├── api_flows.py                # Reusable API workflows
│   ├── ecommerce_flows.py          # Business logic flows
│   ├── test_case_helpers.py        # Test execution helpers
│   └── ...
│
├── test_data/                       # Environment-Specific Test Data
│   ├── qa/
│   │   ├── api/
│   │   ├── registration/
│   │   └── ...
│   ├── stage/
│   ├── dev/
│   └── prod/
│
├── constants/                       # Framework Constants
│   ├── api_routes.py               # API endpoints
│   ├── messages.py                 # Expected messages
│   └── timeouts.py                 # Timeout values
│
├── conftest.py                      # ⭐ Enhanced: Array config fixtures
├── pytest.ini                       # Pytest configuration
├── requirements.txt                 # Python dependencies
│
├── INTEGRATION_GUIDE.md             # ⭐ NEW: Quick start guide
├── example_test_array_config.py     # ⭐ NEW: 8 working examples
│
└── logs/                            # Test execution logs (auto-generated)
```

---

## 🚀 Quick Start

### Installation

```bash
# Navigate to framework directory
cd project_playwright

# Activate virtual environment
source playwright/Scripts/activate  # Linux/Mac
playwright\Scripts\activate         # Windows PowerShell

# Install dependencies
pip install -r requirements.txt
```

### Running Tests

```bash
# Run with default QA environment
pytest tests/ -v

# Run with DEV environment (NEW)
ENV=dev pytest tests/ -v

# Run with specific array
ENV=qa ARRAY=array_02 pytest tests/ -v

# Run specific test file
pytest tests/UI/test_case_01_register_user.py -v

# Run with custom configuration
ENV=stage HEADLESS=true WINDOW_MODE=custom WINDOW_WIDTH=1920 WINDOW_HEIGHT=1080 pytest tests/ -v
```

---

## 🌍 Environment Configuration

### Supported Environments

| Environment | Purpose                 | Primary Array IP | Default Port |
| ----------- | ----------------------- | ---------------- | ------------ |
| **DEV**     | Development & Debugging | 192.168.1.10     | 8080         |
| **QA**      | Quality Assurance       | 192.168.1.10     | 443          |
| **STAGE**   | Pre-Production          | 192.168.1.10     | 443          |
| **PROD**    | Production              | 192.168.1.10     | 443          |

### Array/Server Configuration

Each environment has 3-4 configurable arrays:

- **array_01**: Primary array (192.168.1.10)
- **array_02**: Secondary array (192.168.1.11)
- **array_03**: Tertiary array (192.168.1.12) - QA/STAGE/PROD only

### Environment Variables

```bash
# Core Configuration
ENV=qa                      # Target environment (dev, qa, stage, prod)
ARRAY=array_01             # Target array (default, array_01, array_02, array_03)

# Browser Configuration
HEADLESS=true              # Run in headless mode
WINDOW_MODE=maximized      # Window mode (maximized, fullscreen, minimized, custom)
WINDOW_WIDTH=1920          # Custom window width
WINDOW_HEIGHT=1080         # Custom window height

# Logging
LOG_DIR=logs               # Log output directory
```

---

## 📝 Usage Examples

### Example 1: Traditional Test (100% Backward Compatible)

```python
import pytest
from pages.home_page import HomePage

@pytest.mark.asyncio
async def test_navigate_home(page, env):
    """Existing tests work exactly as before."""
    home_page = HomePage(page)
    base_url = env.get("base_url")
    await page.goto(base_url)
    assert await home_page.is_loaded()
```

### Example 2: Using Array Configuration (NEW)

```python
@pytest.mark.asyncio
async def test_with_array_config(array_config_manager):
    """New feature: Access array/server details."""
    mgr = array_config_manager

    # Get current array
    array = mgr.get_selected_array()
    print(f"Testing against: {array['name']} at {array['ip']}")

    # Get connection string
    conn_str = mgr.get_array_connection_string()
    # Output: "https://192.168.1.10:443"
```

### Example 3: Dynamic Array Switching (NEW)

```python
@pytest.mark.asyncio
async def test_multiple_arrays(array_config_manager):
    """Test against multiple arrays dynamically."""
    mgr = array_config_manager

    # Test array_01
    mgr.set_selected_array("array_01")
    result_1 = await run_test_scenario()

    # Test array_02
    mgr.set_selected_array("array_02")
    result_2 = await run_test_scenario()

    assert result_1 == result_2  # Validate consistency
```

### Example 4: API Testing with Array Config (NEW)

```python
@pytest.mark.asyncio
async def test_api_with_array(array_config_manager, api_client):
    """API testing with dynamic array targeting."""
    url = array_config_manager.get_array_url("/api/products")
    # Output: "https://192.168.1.10:443/api/products"

    response = await api_client.get("/api/products")
    assert response.http_status == 200
```

---

## 📚 Documentation

- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - Enterprise configuration integration guide
- **[config/CONFIG_MANAGEMENT.md](config/CONFIG_MANAGEMENT.md)** - Comprehensive configuration reference
- **[example_test_array_config.py](example_test_array_config.py)** - 8 working examples

---

## 🔧 Advanced Features

### Multi-Array Testing

```bash
# Run tests in parallel against multiple arrays
for ARRAY in array_01 array_02 array_03; do
    ENV=qa ARRAY=$ARRAY pytest tests/ -v
done
```

### Custom Test Data Per Environment

Test data automatically loaded from environment-specific directories:

```
test_data/
├── dev/
├── qa/         # Used when ENV=qa
├── stage/
└── prod/
```

### Environment-Specific Credentials

```python
async def test_login(array_config_manager):
    creds = array_config_manager.get_credentials()
    username = creds["username"]
    password = creds["password"]
    # Login with environment-specific credentials
```

### Structured Logging

All logs include context:

```
2024-05-24 10:15:30 | INFO     | QA     | [array_02]       | test_module | Test execution started
2024-05-24 10:15:32 | INFO     | QA     | [array_02]       | utils.api   | API REQUEST | method=GET | endpoint=/api/products
```

---

## 🛠️ Technology Stack

- **Language**: Python 3.11+
- **Automation**: Playwright (async)
- **Testing**: Pytest with async support
- **Logging**: Python logging module with custom formatting
- **Configuration**: YAML-based configuration management
- **Reporting**: Allure (optional), pytest default reports
- **CI/CD**: Jenkins compatible

---

## 📊 Features by Version

### Version 1.0

- Basic configuration system (QA, STAGE, PROD)
- Playwright UI automation
- REST API testing
- Data-driven testing
- Modular architecture

### Version 2.0 ⭐ (Current - Enterprise Edition)

- ✨ Multi-environment support (added DEV)
- ✨ Array/server configuration manager
- ✨ Dynamic array switching
- ✨ Enhanced structured logging
- ✨ Enterprise-grade documentation
- ✨ Example tests and integration guide
- ✨ 100% backward compatible

---

## 🎓 Best Practices

1. **Use Environment Variables**: Control execution via ENV and ARRAY variables
2. **Leverage Fixtures**: Use array_config_manager and array_info fixtures
3. **Structured Logging**: Always use logger for important test events
4. **Test Data Organization**: Organize test data by environment
5. **Modular Code**: Keep flows, utilities, and page objects separate
6. **Array Targeting**: Test against multiple arrays for failover validation

---

## 🐛 Troubleshooting

### Issue: "Environment 'x' not found"

```bash
# Verify environment is set correctly
echo $ENV  # or set ENV on command line
ENV=qa pytest tests/
```

### Issue: "Array key 'x' not found"

```bash
# Verify array exists in configuration
grep "array_" config/env.yaml
ARRAY=array_01 pytest tests/
```

### Issue: Tests not finding data

```bash
# Verify test data directory structure
ls test_data/qa/  # Check for environment directory
ls test_data/qa/api/  # Check for data file
```

---

## 📈 Scalability

This framework scales to:

- ✅ 100+ test cases
- ✅ 4+ environments
- ✅ 3-4 arrays per environment
- ✅ Parallel execution
- ✅ Selenium/Playwright/API hybrid testing
- ✅ Mobile testing (Appium)

---

## 📞 Support

- Check example tests: `example_test_array_config.py`
- Read config guide: `config/CONFIG_MANAGEMENT.md`
- Review integration guide: `INTEGRATION_GUIDE.md`

---

## 📄 License

Internal Use Only

---

## 🎉 Summary

**Playwright QA Automation Framework v2.0** brings enterprise-grade capabilities to your testing:

- ✅ Multi-environment support (DEV, QA, STAGE, PROD)
- ✅ Dynamic array/server targeting
- ✅ Structured enterprise logging
- ✅ 100% backward compatible
- ✅ Production-ready architecture
- ✅ Comprehensive documentation

Perfect for teams needing professional, scalable, enterprise-level test automation!
