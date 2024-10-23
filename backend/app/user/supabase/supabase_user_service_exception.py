from dataclasses import dataclass

from app.user import UserServiceException


@dataclass(frozen=True)
class SupabaseUserServiceException(UserServiceException):
    message: str

    @property
    def message(self) -> str:
        return str(self.message)
