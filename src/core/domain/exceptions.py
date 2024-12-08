class AlreadyExistsException(Exception):
    pass


class DoesNotExistException(Exception):
    pass


class UserAlreadyExistsException(AlreadyExistsException):
    pass


class UserDoesNotExistsException(DoesNotExistException):
    pass


class ResponseAlreadyExistsException(AlreadyExistsException):
    pass


class ResponseDoesNotExistException(DoesNotExistException):
    pass


class MatchDoesNotExistException(DoesNotExistException):
    pass
