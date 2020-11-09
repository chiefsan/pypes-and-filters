import abc

class PipeStrategy(object, metaclass=abc.ABCMeta):
    '''Abstract class for PipeStrategy
    Pipestrategy class defines the blueprint for implementing the differnt pipeStrategy 
    by which users can define how the message need to be transformed before sending to outgoingFilter.
    '''
    @abc.abstractclassmethod
    def transformMessageQueue(self,messages):
        '''
        Arguments:
            messages(List):Input queue got from incomingFilter
        Return:
            messages(List): Processed the incomingFilter message using user's logic
        '''
        raise NotImplementedError("transformMessageQueue should be defined in base clase")

class FIFO(PipeStrategy):
    '''First In First Out strategy
    It makes the message which is first received from the pipe through incomingFilter
    should be sent first to the outgoingFilter
    '''
    def transformMessageQueue(self,messages):
        return messages

class LIFO(PipeStrategy):
    '''Last in First Out strategy
    It makes the message which is first received from the pipe through incomingFilter
    should be sent last to the outgoingFilter    
    '''
    def transformMessageQueue(self,messages):
        return messages[::-1]