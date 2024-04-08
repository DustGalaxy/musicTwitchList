from fastapi import HTTPException, status


class MissingCode(Exception):
    def __init__(self):
        message = "Missing code"
        super().__init__(message)


class EmailConfirmException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Email not confirmed, please confirm email in Twitch to continue."
        )


class CredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={"Authenticate": "Bearer"}
        )
