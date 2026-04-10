class AppError(Exception):
    """Base application exception."""


class AuthError(AppError):
    """Base auth-related exception."""


class UserAlreadyExistsError(AuthError):
<<<<<<< HEAD
    """Raised when user with same email or login already exists."""
=======
    """Raised when user with same email or username already exists."""
>>>>>>> e9df211 (initial commit)


class InvalidCredentialsError(AuthError):
    """Raised when credentials are invalid."""


class TokenInvalidError(AuthError):
    """Raised when token is invalid or expired."""


class NotFoundError(AppError):
    """Raised when entity is not found."""


class PermissionDeniedError(AppError):
    """Raised when user has no permission for action."""
<<<<<<< HEAD


class ConflictError(AppError):
    """Raised when operation conflicts with existing state."""


class BadRequestError(AppError):
    """Raised when request data is semantically invalid."""
=======
>>>>>>> e9df211 (initial commit)
