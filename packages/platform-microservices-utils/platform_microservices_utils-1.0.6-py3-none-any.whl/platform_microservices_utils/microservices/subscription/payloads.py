# Python Imports

# Django Imports

# Third-Party Imports

# Project-Specific Imports

# Relative Import


class IncreaseUsageCountPayload:
    """Class representing a payload for increasing usage count."""

    def __init__(self, username, tenant_identifier, endpoint_id):
        self.username = username
        self.tenant_identifier = tenant_identifier
        self.endpoint_id = endpoint_id

    def get_payload(self):
        """Return a dictionary representation of the payload."""
        return vars(self)
