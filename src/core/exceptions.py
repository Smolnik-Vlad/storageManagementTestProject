class CustomBaseException(Exception):
    def __init__(self):
        self.status_code = 500
        self.default_message = "Default error occurred."


class DatabaseConnectionException(CustomBaseException):
    def __init__(self):
        self.status_code = 503  # Internal Server Error
        self.default_message = "Database connection error. Please try again later."


class DatabaseException(CustomBaseException):
    def __init__(self):
        self.status_code = 500  # Internal Server Error
        self.default_message = "Database exception. Check restrictions"


class InvalidRequestDataException(CustomBaseException):
    def __init__(self):
        self.status_code = 400  # Bad Request
        self.default_message = "Invalid request data."
