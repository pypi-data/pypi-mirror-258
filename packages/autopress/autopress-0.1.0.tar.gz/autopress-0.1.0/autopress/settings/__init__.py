import os
import logging

from dotenv import load_dotenv

import logging
logger = logging.getLogger()

def load_env():
    # Load comments from .env file
    env_path = os.path.join(os.path.dirname(__file__), ".env")  # change .env.public to something else

    if os.path.exists(env_path):
        logger.info(f"✅ Loading secrets at {env_path}")
        load_dotenv(env_path, verbose=True)

def write_env_file(data: dict, name: str) -> str:
    """Create a .env file with the given data.

    Args:
        data (dict): A dictionary with the environment variables.
        name (str): The name of the .env file to create. (.env.local, .env.dev, .env.prod, etc.)

    Returns:
        str: The path to the created .env file.
    """
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), name))
    with open(dotenv_path, "w") as f:
        for key, value in data.items():
            f.write(f"{key}={value}\n")
    return dotenv_path
        
def getenv(key: str, default=None):
    """Use this function to get environment variables.
    It is a wrapper around os.getenv that returns the default value
     if the variable is not set.
    It is useful for boolean variables that are converted 
    from strings to booleans (e.g. "True" -> True).

    Example usage:
    ```python
    import photonml.settings as settings
    val = settings.getenv("DEBUG", False)
    ```

    """
    value = os.getenv(key, default)
    if value == "True":
        return True
    elif value == "False":
        return False
    elif value == "None":
        return None
    else:
        return value
