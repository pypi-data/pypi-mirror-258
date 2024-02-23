class KomoException(BaseException):
    def __init__(self, message):
        super().__init__(message)


class NoSymbolsFoundInGenerator(KomoException):
    """Exception raised when no symbols in the SymbolGenerator shared instance.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="No symbols in the SymbolGenerator instance. "):
        self._message = message

        super().__init__(self._message)

    def __str__(self):
        return f'{self._message}'


class NoWhiteListedExchangesError(KomoException):
    """Exception raised when no whitelisted exchanges are on the returned list.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="No valid whitelisted exchanges were found. "):
        self._message = message

        super().__init__(self._message)

    def __str__(self):
        return f'{self._message} Please check that the AWS S3 bucket has the correct list. '


class EnvironmentVariableError(KomoException):
    """Exception raised when one or more env variables are not available.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, missing: list, message="Environment variable(s) missing. "):
        self._missing = missing
        self._message = message

        super().__init__(self._message)

    def __str__(self):
        return f'{self._message} -> {self._missing}'


class TradesCollectionExecutorIsNotRunning(KomoException):
    """Exception raised when trades are needed but not trades are being collected by the trades collection executor.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Trades collection executor is not running. "):
        self._message = message

        super().__init__(self._message)

    def __str__(self):
        return f'{self._message}'


class IncongruentEpochError(KomoException):
    """Exception raised when a task with an epoch X is required to act on a data object with of an epoch Y.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Incorrect epoch id on data object. "):
        self._message = message

        super().__init__(self._message)

    def __str__(self):
        return f'{self._message}'


class RatesServiceNotAvailableError(KomoException):
    """Exception raised when the app fails to reach or get a valid response from the rates service.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, exception_type: str):
        self._message = f"Rates services is either not available or not working properly. Error type - {exception_type}. "
        super().__init__(self._message)

    def __str__(self):
        return f'{self._message}'


class SymbolsServiceNotAvailableError(KomoException):
    """Exception raised when the app fails to reach or get a valid response from the symbols and groups service.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, exception_type: str):
        self._message = f"Symbols services is either not available or not working properly. Error type - {exception_type}. "
        super().__init__(self._message)

    def __str__(self):
        return f'{self._message}'

