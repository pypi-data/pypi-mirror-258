
import logging as _logging
import py_pkg_logging as _ppl

_log_config = _ppl.LogConfig(name = "color_wizard", log_file="color_wizard.log")

_logger = _logging.getLogger(f'color_wizard.{__name__}')
_logger.info(f"Logs for color_wizard will be saved to: {_log_config.log_fpath}")
_logger.debug(f"Importing from local install location: {__file__}")
