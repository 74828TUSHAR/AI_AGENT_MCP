"""
===============================================================================
Enterprise Array/Server Configuration Manager
===============================================================================
Provides dynamic array/server targeting for multi-environment automation
Supports environment-based array selection and runtime switching

Usage:
    from config.array_config import ArrayConfigManager
    
    # Initialize with environment
    mgr = ArrayConfigManager(environment="qa")
    
    # Get default array for environment
    array = mgr.get_selected_array()
    print(f"Target Array: {array['name']}, IP: {array['ip']}")
    
    # Switch to different array
    mgr.set_selected_array("array_02")
    
    # Get all available arrays for environment
    arrays = mgr.get_available_arrays()
    
    # Get specific array by key
    specific = mgr.get_array("array_01")
===============================================================================
"""

import yaml
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from utils.logger import get_logger


class ArrayConfigManager:
    """
    Manages array/server configurations for multi-environment automation.
    Provides dynamic array selection, switching, and retrieval functionality.
    """

    def __init__(self, environment: str = None):
        """
        Initialize ArrayConfigManager with target environment.
        
        Args:
            environment: Target environment (dev, qa, stage, prod)
                        Defaults to ENV environment variable or 'qa'
        """
        self.logger = get_logger(self.__class__.__name__)
        self.environment = environment or os.getenv("ENV", "qa")
        self.config_path = Path(__file__).parent / "env.yaml"
        
        # Load configuration
        with open(self.config_path, "r", encoding="utf-8") as f:
            self._all_configs = yaml.safe_load(f)
        
        # Validate environment
        if self.environment not in self._all_configs:
            available = list(self._all_configs.keys())
            raise ValueError(
                f"Environment '{self.environment}' not found. "
                f"Available environments: {available}"
            )
        
        self._env_config = self._all_configs[self.environment]
        self._selected_array_key = "default"  # Default array selection
        
        self.logger.info(
            f"[ARRAY-CONFIG] Initialized for environment: {self.environment} | "
            f"Description: {self._env_config.get('description', 'N/A')}"
        )
    
    # =========================================================================
    # ARRAY SELECTION & RETRIEVAL METHODS
    # =========================================================================
    
    def get_selected_array(self) -> Dict[str, Any]:
        """
        Get currently selected array/server configuration.
        
        Returns:
            Dictionary containing array details (name, ip, port, protocol)
        """
        array = self._env_config["arrays"].get(self._selected_array_key)
        if not array:
            raise KeyError(
                f"Array key '{self._selected_array_key}' not found in "
                f"environment '{self.environment}'"
            )
        return array.copy()
    
    def set_selected_array(self, array_key: str) -> Dict[str, Any]:
        """
        Switch to different array/server for current environment.
        
        Args:
            array_key: Key of array to select (e.g., 'array_01', 'array_02')
        
        Returns:
            Dictionary containing selected array details
        
        Raises:
            KeyError: If array_key doesn't exist in current environment
        """
        if array_key not in self._env_config["arrays"]:
            available = list(self._env_config["arrays"].keys())
            raise KeyError(
                f"Array key '{array_key}' not found. "
                f"Available arrays: {available}"
            )
        
        self._selected_array_key = array_key
        selected = self.get_selected_array()
        
        self.logger.info(
            f"[ARRAY-SWITCH] Changed target array | "
            f"Environment: {self.environment} | "
            f"Array: {selected['name']} | "
            f"IP: {selected['ip']} | "
            f"Port: {selected['port']}"
        )
        
        return selected
    
    def get_array(self, array_key: str) -> Dict[str, Any]:
        """
        Get specific array configuration by key.
        
        Args:
            array_key: Array key identifier
        
        Returns:
            Dictionary containing array details
        """
        array = self._env_config["arrays"].get(array_key)
        if not array:
            available = list(self._env_config["arrays"].keys())
            raise KeyError(
                f"Array key '{array_key}' not found. "
                f"Available arrays: {available}"
            )
        return array.copy()
    
    def get_available_arrays(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all available arrays for current environment.
        
        Returns:
            Dictionary of all array configurations
        """
        return {
            key: value.copy() 
            for key, value in self._env_config["arrays"].items()
        }
    
    # =========================================================================
    # ARRAY CONNECTION STRING BUILDERS
    # =========================================================================
    
    def get_array_connection_string(self, array_key: str = None) -> str:
        """
        Build connection string for array/server.
        Format: protocol://ip:port
        
        Args:
            array_key: Optional array key. Defaults to selected array.
        
        Returns:
            Connection string (e.g., https://192.168.1.10:443)
        """
        array = self.get_array(array_key) if array_key else self.get_selected_array()
        return f"{array['protocol']}://{array['ip']}:{array['port']}"
    
    def get_array_url(self, endpoint: str = "", array_key: str = None) -> str:
        """
        Build full URL for array endpoint.
        
        Args:
            endpoint: API endpoint or path (e.g., '/api/products')
            array_key: Optional array key. Defaults to selected array.
        
        Returns:
            Full URL (e.g., https://192.168.1.10:443/api/products)
        """
        conn_string = self.get_array_connection_string(array_key)
        if endpoint.startswith("/"):
            return f"{conn_string}{endpoint}"
        return f"{conn_string}/{endpoint}" if endpoint else conn_string
    
    # =========================================================================
    # ENVIRONMENT & CONFIG ACCESSORS
    # =========================================================================
    
    def get_environment(self) -> str:
        """Get current environment name."""
        return self.environment
    
    def get_environment_config(self) -> Dict[str, Any]:
        """
        Get full environment configuration.
        
        Returns:
            Complete config for current environment
        """
        return self._env_config.copy()
    
    def get_base_url(self) -> str:
        """Get base URL for current environment."""
        return self._env_config.get("base_url", "")
    
    def get_api_base_url(self) -> str:
        """Get API base URL for current environment."""
        return self._env_config.get("api_base_url", self.get_base_url())
    
    def get_credentials(self) -> Dict[str, str]:
        """
        Get username and password for current environment.
        
        Returns:
            Dictionary with 'username' and 'password' keys
        """
        return {
            "username": self._env_config.get("username", ""),
            "password": self._env_config.get("password", "")
        }
    
    def get_window_config(self) -> Dict[str, Any]:
        """Get window/viewport configuration."""
        return self._env_config.get("window", {}).copy()
    
    # =========================================================================
    # ENVIRONMENT SUMMARY & LOGGING
    # =========================================================================
    
    def log_environment_info(self):
        """Log comprehensive environment and array configuration."""
        selected = self.get_selected_array()
        arrays = self.get_available_arrays()
        
        self.logger.info("=" * 75)
        self.logger.info("[ENV-SUMMARY] Automation Environment Configuration")
        self.logger.info("=" * 75)
        self.logger.info(f"Environment: {self.environment.upper()}")
        self.logger.info(f"Description: {self._env_config.get('description', 'N/A')}")
        self.logger.info(f"Base URL: {self.get_base_url()}")
        self.logger.info(f"API Base URL: {self.get_api_base_url()}")
        self.logger.info("-" * 75)
        self.logger.info(f"Selected Array: {selected['name']}")
        self.logger.info(f"Array IP: {selected['ip']}")
        self.logger.info(f"Array Port: {selected['port']}")
        self.logger.info(f"Protocol: {selected['protocol'].upper()}")
        self.logger.info(f"Connection String: {self.get_array_connection_string()}")
        self.logger.info("-" * 75)
        self.logger.info(f"Available Arrays ({len(arrays)}):")
        for key, array in arrays.items():
            is_selected = " [SELECTED]" if key == self._selected_array_key else ""
            self.logger.info(
                f"  • {array['name']} ({key}): {array['protocol']}://"
                f"{array['ip']}:{array['port']}{is_selected}"
            )
        self.logger.info("=" * 75)
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get dictionary summary of environment configuration.
        
        Returns:
            Dictionary with environment and array summary
        """
        selected = self.get_selected_array()
        return {
            "environment": self.environment,
            "description": self._env_config.get("description", ""),
            "base_url": self.get_base_url(),
            "api_base_url": self.get_api_base_url(),
            "selected_array": {
                "key": self._selected_array_key,
                "name": selected["name"],
                "ip": selected["ip"],
                "port": selected["port"],
                "protocol": selected["protocol"],
                "connection_string": self.get_array_connection_string()
            },
            "available_arrays": len(self._env_config["arrays"])
        }


# ============================================================================
# MODULE-LEVEL CONVENIENCE FUNCTIONS (Backward Compatibility)
# ============================================================================

# Global instance for backward compatibility
_global_array_manager: Optional[ArrayConfigManager] = None


def get_array_manager(environment: str = None) -> ArrayConfigManager:
    """
    Get or create global ArrayConfigManager instance.
    
    Args:
        environment: Optional environment override
    
    Returns:
        ArrayConfigManager instance
    """
    global _global_array_manager
    if _global_array_manager is None or (
        environment and environment != _global_array_manager.environment
    ):
        _global_array_manager = ArrayConfigManager(environment)
    return _global_array_manager


def reset_array_manager():
    """Reset global array manager instance."""
    global _global_array_manager
    _global_array_manager = None
