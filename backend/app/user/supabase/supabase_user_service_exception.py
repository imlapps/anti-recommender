from app.user import UserServiceException


class SupabaseUserServiceException(UserServiceException):
    def __init__(self, message: str) -> None:
        self.__message = message

    @property
    def message(self) -> str:
        return str(self.__message)
