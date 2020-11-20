"""
Message module docstring.
"""
import abc


class Message(object, metaclass=abc.ABCMeta):
    """
    Message class docstring.
    """
    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError(
            """users must
    define __str__ to use this base class"""
        )
