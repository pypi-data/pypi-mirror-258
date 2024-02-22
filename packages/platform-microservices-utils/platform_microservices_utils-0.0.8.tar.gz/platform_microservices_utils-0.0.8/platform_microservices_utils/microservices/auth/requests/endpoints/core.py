# Python Imports

# Django Imports

# Third-Party Imports
from platform_microservices_utils.ini_parser import endpoint_config
from platform_microservices_utils.url_builder import BuildUrl

# Project-Specific Imports

# Relative Import


class BaseEndpoint:
    """Base class for managing generic endpoints."""

    def __init__(self):
        """Initialize the BaseEndpoint instance."""
        self.endpoint_config = endpoint_config

    def get_endpoint(self):
        """Get the endpoint."""
        raise NotImplementedError("Subclasses must implement this method.")


class AuthEndpointUrl(BuildUrl):
    """Class for constructing URLs related to various authentication endpoints."""

    @classmethod
    def get_url(cls, endpoint_class):
        """Get the URL for the specified authentication endpoint class."""
        endpoint = endpoint_class().get_endpoint()
        return cls.construct_url(endpoint=endpoint)
