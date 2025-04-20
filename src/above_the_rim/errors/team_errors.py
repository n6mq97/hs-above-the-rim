
class InvalidTeamShortError(ValueError):
    """Raised when the provided team short code is invalid."""
    pass

class TeamNotFoundError(ValueError):
    """Raised when the provided team short code not found in database."""
    pass

class TeamAlreadyExistsError(ValueError):
    """Raised when the provided team short code already exists in database."""
    pass