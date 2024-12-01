class AlreadyExistsException(Exception):
    pass


class DoesNotExistException(Exception):
    pass


class UserAlreadyExistsException(AlreadyExistsException):
    pass


class UserDoesNotExistsException(DoesNotExistException):
    pass
