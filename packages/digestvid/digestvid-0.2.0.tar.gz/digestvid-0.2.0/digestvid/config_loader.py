import os
import yaml
from pathlib import Path

def get_config_path():
    """Returns the path to the config.yaml file."""
    return Path.home() / '.DigestVid' / 'config.yaml'

def load_config():
    """Loads the entire configuration from the config file."""
    config_path = get_config_path()
    if config_path.exists():
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML configuration: {e}")
            return {}
    return {}

# Use a single function to load the entire configuration and then access parts of it.
_config_cache = None  # Cache the configuration to avoid multiple file reads.

def get_config():
    """Gets the entire configuration, caching it to avoid repeated file access."""
    global _config_cache
    if _config_cache is None:
        _config_cache = load_config()
    return _config_cache

def load_api_key():
    """Loads the OpenAI API key, preferring the environment variable if set."""
    return os.getenv('OPENAI_API_KEY', get_config().get('openai_api_key'))

def load_llm_config():
    """Loads the LLM configuration from the config file."""
    return get_config().get('llm_config', {})
