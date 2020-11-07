import abc
class Pipe(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError('users must define __str__ to use this base class')
