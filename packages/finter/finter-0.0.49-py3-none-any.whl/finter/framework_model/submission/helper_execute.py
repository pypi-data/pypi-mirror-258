import importlib.util
import sys
from pathlib import Path

# Ensure your import path is correct for ModelConfig
from finter.framework_model.submission.config import ModelConfig
from finter.settings import logger


def load_and_run(start, end, file_path, model_type="alpha"):
    """
    Dynamically loads a class from a given file path, creates an instance,
    and executes its 'get' method with start and end parameters.

    :param file_path: Path to the .py file containing the class definition.
    :param start: Start date parameter for the 'get' method.
    :param end: End date parameter for the 'get' method.
    :param model_type: Type of the model to load, defaults to "alpha".
    :return: The result of the 'get' method if successful, None otherwise.
    """

    # Retrieve class name from the ModelConfig enum based on model_type
    class_name = ModelConfig[model_type].class_name

    # Use the file name (without extension) as the module name
    file_path = Path(file_path)
    module_name = file_path.stem

    # Add the directory containing the file to sys.path if not already included
    file_directory = file_path.parent
    if str(file_directory) not in sys.path:
        sys.path.append(str(file_directory))

    # Load the module
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        logger.error("Could not load the module.")
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        logger.error(f"Error loading module: {e}")
        return None

    # Import the class and create an instance
    try:
        Model = getattr(module, class_name)
        model_instance = Model()
    except AttributeError as e:
        logger.error(f"Error finding class {class_name} in the module: {e}")
        return None
    except Exception as e:
        logger.error(f"Error creating an instance of {class_name}: {e}")
        return None

    # Execute the 'get' method of the instance
    try:
        result = model_instance.get(start, end)
        logger.info(f"Model abs sum result: {result.abs().sum(axis=1).tail()}")
        return result
    except Exception as e:
        logger.error(f"Error executing the 'get' method: {e}")
        return None
