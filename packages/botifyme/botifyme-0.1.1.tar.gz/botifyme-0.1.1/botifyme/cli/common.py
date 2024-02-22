import os
import importlib
import inspect
from loguru import logger
from pathlib import Path
from slugify import slugify
from dotenv import load_dotenv
from botifyme.utils.tools import get_function_details, get_class_details

CONFIG_DIR = Path.home() / ".botifyme"
CONFIG_FILE = CONFIG_DIR / "config.yaml"


def init_cli():
    load_dotenv()


def configure_logging(verbose: bool):
    logger.remove()  # Remove the default handler
    if verbose:
        level = "INFO"
    else:
        level = "WARNING"
    logger.add(lambda msg: print(msg, end=""), level=level)


def load_tools_from_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            module_path = os.path.join(directory, filename)

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    # Check if the class has the 'tool' decorator
                    # This requires a way to identify if the decorator is applied.
                    # One approach could be checking for a custom attribute set by the decorator.
                    if hasattr(obj, "your_custom_attribute_set_by_tool_decorator"):
                        # Instantiate the class or register it as needed
                        instance = obj()
                        print(f"Loaded tool: {name}")

