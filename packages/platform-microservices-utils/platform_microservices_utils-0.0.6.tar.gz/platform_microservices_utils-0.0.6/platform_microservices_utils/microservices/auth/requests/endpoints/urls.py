# Python Imports

# Django Imports

# Third-Party Imports

# Project-Specific Imports

# Relative Import
from .core import AuthEndpointUrl
from .endpoints import AuthPassEndpoint





class AuthPassUrl(AuthEndpointUrl):
    """Class for constructing URLs related to the authentication microservice."""

    @classmethod
    def get_auth_pass_url(cls):
        """Get the URL for authenticating user passwords."""
        return cls.get_url(AuthPassEndpoint)


class ValidateTokenUrl(AuthEndpointUrl):
    """Class for constructing URLs related to token validation in the authentication microservice."""

    # @classmethod
    # def get_validate_token_url(cls):
    #     """Get the URL for token validation."""
    #     return cls.get_url(ValidateTokenEndpoint)
    @classmethod
    def get_validate_token_url(cls):
        """Get the URL for token validation."""
        return "http://127.0.0.1:8000/auth/verify-token/"


class HasPermUrl(AuthEndpointUrl):
    """Class for constructing URLs related to permission validation in the authentication microservice."""

    # @classmethod
    # def get_has_perm_url(cls):
    #     """Get the URL for validating a token."""
    #     return cls.get_url(HasPermEndpoint)

    @classmethod
    def get_has_perm_url(cls):
        """Get the URL for token validation."""
        return "http://127.0.0.1:8000/authorisation/has-perm"
