

class BadRequestException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)

class NotFoundException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)

class NotAllowedException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)


class DeleteFailureException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)


class ConflictException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)

