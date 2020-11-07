import abc
from multiprocessing import Pipe

class BasePipe(object, metaclass=abc.ABCMeta):
    # Abstract class for pipes
    @abc.abstractmethod
    def receive(self):
        raise NotImplementedError('users must define receive to use this base class')
    @abc.abstractclassmethod
    def send(self,message):
        raise NotImplementedError('users must define send to use this base class')


class Pipes(BasePipe):
    def __init__(self):
        self.Inqueue,self.Outqueue = Pipe(duplex=False)
    def receive(self):
        return self.Inqueue.recv()
    def send(self,Message):
        self.Outqueue.send(Message)
        self.Outqueue.close()