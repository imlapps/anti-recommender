from abc import abstractmethod


class UserServiceException(BaseException):

    @abstractmethod
    @property
    def message(self) -> str:
        pass
