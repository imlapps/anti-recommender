from app.auth import AuthException


class UserNotFoundAuthException(AuthException):
    """An exception encountered when user data cannot be obtained from an AuthService."""
