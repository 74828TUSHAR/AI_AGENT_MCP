"""
===============================================================================
Example Test: Enterprise Configuration & Array Management
===============================================================================
Demonstrates usage of the new array configuration system with environment
management, array switching, and structured logging.

Run with:
    # Default QA environment
    pytest example_test_array_config.py -v
    
    # DEV environment with array_02
    ENV=dev ARRAY=array_02 pytest example_test_array_config.py -v
    
    # STAGE environment
    ENV=stage pytest example_test_array_config.py -v
===============================================================================
"""

import pytest
from utils.logger import get_logger


# Get logger instance for this module
logger = get_logger(__name__)


class TestArrayConfigurationExample:
    """
    Example test class demonstrating array configuration management.
    """
    
    def test_environment_info(self, array_config_manager):
        """
        EXAMPLE 1: Get environment and array information.
        
        Demonstrates:
        - Accessing array configuration manager
        - Getting selected array details
        - Logging environment information
        """
        logger.info("=" * 75)
        logger.info("EXAMPLE 1: Environment & Array Information")
        logger.info("=" * 75)
        
        # Get current environment
        env = array_config_manager.get_environment()
        logger.info(f"Current Environment: {env.upper()}")
        
        # Get selected array
        array = array_config_manager.get_selected_array()
        logger.info(f"Selected Array: {array['name']}")
        logger.info(f"Array IP: {array['ip']}")
        logger.info(f"Array Port: {array['port']}")
        logger.info(f"Protocol: {array['protocol'].upper()}")
        
        # Log comprehensive environment info
        array_config_manager.log_environment_info()
        
        # Assertions
        assert env in ["dev", "qa", "stage", "prod"]
        assert "ip" in array
        assert "port" in array
        assert "protocol" in array
    
    def test_array_selection_and_switching(self, array_config_manager):
        """
        EXAMPLE 2: Array selection and dynamic switching.
        
        Demonstrates:
        - Getting available arrays
        - Switching between arrays
        - Accessing switched array details
        """
        logger.info("=" * 75)
        logger.info("EXAMPLE 2: Array Selection & Switching")
        logger.info("=" * 75)
        
        # Get all available arrays
        available = array_config_manager.get_available_arrays()
        logger.info(f"Available Arrays: {list(available.keys())}")
        
        # Get default array
        default = array_config_manager.get_selected_array()
        logger.info(f"Default Array: {default['name']} ({default['ip']})")
        
        # Switch to array_01 if available
        if "array_01" in available:
            switched = array_config_manager.set_selected_array("array_01")
            logger.info(f"Switched to: {switched['name']} ({switched['ip']})")
            
            # Verify switch
            current = array_config_manager.get_selected_array()
            assert current["name"] == switched["name"]
        
        # Demonstrate error handling
        try:
            array_config_manager.set_selected_array("nonexistent")
            assert False, "Should have raised KeyError"
        except KeyError as e:
            logger.info(f"Expected error for nonexistent array: {str(e)}")
    
    def test_connection_string_building(self, array_config_manager):
        """
        EXAMPLE 3: Building connection strings and URLs.
        
        Demonstrates:
        - Getting base connection string
        - Building full URLs with endpoints
        - Supporting different endpoint formats
        """
        logger.info("=" * 75)
        logger.info("EXAMPLE 3: Connection String Building")
        logger.info("=" * 75)
        
        # Get connection string
        conn_str = array_config_manager.get_array_connection_string()
        logger.info(f"Connection String: {conn_str}")
        assert "://" in conn_str
        assert "192.168" in conn_str
        
        # Build URLs with endpoints
        endpoints = [
            "/api/health",
            "api/products",
            "/api/users/123",
            "health"
        ]
        
        logger.info("Building URLs for various endpoints:")
        for endpoint in endpoints:
            url = array_config_manager.get_array_url(endpoint)
            logger.info(f"  • {endpoint:20s} -> {url}")
            assert conn_str in url
    
    def test_environment_credentials(self, array_config_manager):
        """
        EXAMPLE 4: Access environment-specific credentials.
        
        Demonstrates:
        - Getting username/password from config
        - Using credentials in test execution
        """
        logger.info("=" * 75)
        logger.info("EXAMPLE 4: Environment Credentials")
        logger.info("=" * 75)
        
        # Get credentials
        creds = array_config_manager.get_credentials()
        username = creds.get("username")
        password = creds.get("password")
        
        logger.info(f"Username: {username}")
        logger.info(f"Password: {'*' * len(password) if password else 'Not set'}")
        
        # Verify credentials exist
        assert username is not None
        assert password is not None
    
    def test_using_array_info_fixture(self, array_info):
        """
        EXAMPLE 5: Using array_info fixture directly.
        
        Demonstrates:
        - Alternative approach using array_info fixture
        - Accessing array details in test
        """
        logger.info("=" * 75)
        logger.info("EXAMPLE 5: Using array_info Fixture")
        logger.info("=" * 75)
        
        logger.info(f"Array Name: {array_info['name']}")
        logger.info(f"Array IP: {array_info['ip']}")
        logger.info(f"Array Port: {array_info['port']}")
        logger.info(f"Protocol: {array_info['protocol']}")
        
        # Verify array_info structure
        required_keys = {"name", "ip", "port", "protocol"}
        assert required_keys.issubset(array_info.keys())
    
    def test_configuration_summary(self, array_config_manager):
        """
        EXAMPLE 6: Get comprehensive configuration summary.
        
        Demonstrates:
        - Getting full configuration summary
        - Analyzing available arrays
        - Displaying environment details
        """
        logger.info("=" * 75)
        logger.info("EXAMPLE 6: Configuration Summary")
        logger.info("=" * 75)
        
        # Get summary
        summary = array_config_manager.get_summary()
        
        logger.info(f"Environment: {summary['environment'].upper()}")
        logger.info(f"Description: {summary['description']}")
        logger.info(f"Base URL: {summary['base_url']}")
        logger.info(f"API Base URL: {summary['api_base_url']}")
        logger.info(f"Selected Array: {summary['selected_array']['name']}")
        logger.info(f"Connection String: {summary['selected_array']['connection_string']}")
        logger.info(f"Available Arrays: {summary['available_arrays']}")
        
        # Verify summary structure
        assert summary["environment"] in ["dev", "qa", "stage", "prod"]
        assert "selected_array" in summary
        assert summary["available_arrays"] > 0
    
    @pytest.mark.asyncio
    async def test_with_browser_fixture(self, page, array_info):
        """
        EXAMPLE 7: Using array configuration with browser tests.
        
        Demonstrates:
        - Combining array config with Playwright page fixture
        - Using array info in UI tests
        """
        logger.info("=" * 75)
        logger.info("EXAMPLE 7: Array Config with Browser Tests")
        logger.info("=" * 75)
        
        logger.info(f"Testing with array: {array_info['name']} at {array_info['ip']}")
        
        # This is where you would navigate to your test URL
        # The page fixture is already configured with the environment's base_url
        
        logger.info("Browser is ready for testing")
        # Example: await page.goto("https://your-application.com")
        # Example: await page.click("button[type='submit']")
    
    @pytest.mark.asyncio
    async def test_with_api_fixture(self, api_client, array_config_manager):
        """
        EXAMPLE 8: Using array configuration with API tests.
        
        Demonstrates:
        - Combining array config with API client
        - Using connection strings for API calls
        """
        logger.info("=" * 75)
        logger.info("EXAMPLE 8: Array Config with API Tests")
        logger.info("=" * 75)
        
        # Get array info
        array = array_config_manager.get_selected_array()
        logger.info(f"Testing API against: {array['name']} ({array['ip']})")
        
        # Get API base URL
        api_url = array_config_manager.get_api_base_url()
        logger.info(f"API Base URL: {api_url}")
        
        logger.info("API client is ready for testing")
        # Example: result = await api_client.get("/api/products")


class TestMultiArrayExecution:
    """
    Example tests demonstrating multi-array execution patterns.
    """
    
    def test_iterate_all_arrays(self, array_config_manager):
        """
        Demonstrates iterating through all arrays in an environment.
        Useful for:
        - Array compatibility testing
        - Load distribution validation
        - Array failover testing
        """
        logger.info("=" * 75)
        logger.info("Testing Against All Available Arrays")
        logger.info("=" * 75)
        
        available_arrays = array_config_manager.get_available_arrays()
        
        for array_key, array_config in available_arrays.items():
            logger.info("-" * 75)
            logger.info(f"Testing against array: {array_key}")
            logger.info(f"  Name: {array_config['name']}")
            logger.info(f"  IP: {array_config['ip']}")
            logger.info(f"  Port: {array_config['port']}")
            
            # Simulate test execution
            connection_string = (
                f"{array_config['protocol']}://"
                f"{array_config['ip']}:{array_config['port']}"
            )
            logger.info(f"  Connection: {connection_string}")
            
            # Your test logic here
            assert array_config["ip"] is not None
            logger.info(f"✓ Array {array_key} validated successfully")


if __name__ == "__main__":
    """
    Run with: pytest example_test_array_config.py -v -s
    
    Use -s flag to see print output in console.
    """
    pytest.main([__file__, "-v", "-s"])
