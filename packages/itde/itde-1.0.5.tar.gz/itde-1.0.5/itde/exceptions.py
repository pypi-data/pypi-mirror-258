class ITDEBaseException(BaseException):
    """ """


class KeyNotFound(ITDEBaseException, KeyError):
    """ """


class EndpointNotFound(ITDEBaseException):
    """ """


class UnexpectedState(ITDEBaseException):
    """ """


class UnregisteredElement(ITDEBaseException):
    """ """


class UnregisteredShelfType(UnregisteredElement):
    """ """


class UnregisteredHeaderType(UnregisteredElement):
    """ """


class UnregisteredItemType(UnregisteredElement):
    """ """
