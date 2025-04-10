import logging
import logging.config
from pathlib import Path

import yaml


def setup_logging():
    # Determine the path to config.yml relative to the current directory
    config_path = Path(__file__).parent / "config" / "config.yml"

    # Load YAML configuration
    with open(config_path) as f_in:
        config = yaml.safe_load(f_in)

    # Apply logging configuration
    logging.config.dictConfig(config)


logger = logging.getLogger("media-market-gen")

logger_request = logging.getLogger("media-market-gen.request")

logger_test = logging.getLogger("media-market-gen.test")
