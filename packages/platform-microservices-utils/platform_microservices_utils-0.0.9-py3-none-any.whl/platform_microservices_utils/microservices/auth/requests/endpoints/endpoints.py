# Python Imports

# Django Imports

# Third-Party Imports

# Project-Specific Imports

# Relative Import
from .core import BaseEndpoint



class AuthPassEndpoint(BaseEndpoint):
    """Class for managing authentication endpoints."""

    def get_endpoint(self):
        """Get the authentication endpoint."""
        return self.endpoint_config.auth_pass

class ValidateTokenEndpoint(BaseEndpoint):
    """Class for managing token validation endpoints."""

    def get_endpoint(self):
        """Get the token validation endpoint."""
        return self.endpoint_config.validate_token

class HasPermEndpoint(BaseEndpoint):
    """Class for managing endpoints related to permission validation."""

    def get_endpoint(self):
        """Get the permission validation endpoint."""
        return self.endpoint_config.has_perm
