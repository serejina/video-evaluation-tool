"""
Module to represent custom exceptions
"""


class VideoCaptureException(Exception):
    """Raised when cv::VideoCapture encounters errors, e.g. file can't be open
    """
    pass


class ConfigError(Exception):
    """Raised when configuration parameters are not found or incorrect, e.g. videos are not defined in the configuration file
    """
    pass


