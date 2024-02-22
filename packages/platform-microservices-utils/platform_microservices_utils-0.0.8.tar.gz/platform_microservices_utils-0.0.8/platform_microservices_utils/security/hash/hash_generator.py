# Python Imports

# Django Imports

# Third-Party Imports

# Project-Specific Imports
from platform_microservices_utils.security.core.base import (
    KeyDerivationBase,
    KeyGenerationUtility,
)

# Relative Import


class KeyDerivation(KeyDerivationBase, KeyGenerationUtility):
    """
    Utility class for key derivation using PBKDF2.
    """

    @classmethod
    def generate_key(cls):
        """
        Derive a key using PBKDF2.
        """
        return cls.derive_key(
            secret_key=cls.get_secret_key(), request_id=cls.get_request_id()
        )
