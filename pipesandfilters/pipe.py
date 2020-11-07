import abc
from multiprocessing import Pipe
class BasePipe(object, metaclass=abc.ABCMeta):
    # Abstract class for pipes
    def __init__(self,strategy):
        self.strategy = strategy
    @abc.abstractmethod
    def receive(self):
        raise NotImplementedError('users must define receive to use this base class')
    @abc.abstractclassmethod
    def send(self,message):
        raise NotImplementedError('users must define send to use this base class')


class Pipes(BasePipe):
	def __init__(self,strategy):
		self.Inqueue,self.Outqueue = Pipe()
		self.Strategy = strategy
	def receive():
        return self.Inqueue.recv()
	def send(Message):
		Message = self.Strategy.getMessage(Messages)
		self.Outqueue.send(self.Messages)
