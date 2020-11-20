import abc


class PipeStrategy(object, metaclass=abc.ABCMeta):
    """Abstract class for PipeStrategy

    Pipestrategy class defines the blueprint for implementing
    the differnt pipeStrategy
    by which user's can modify the order of the message before
    sending it to outgoinfFilter
    """

    @abc.abstractclassmethod
    def transformMessageQueue(self, messages):
        """
        Defines the how messages need to be transformed
        before sending it to outgoingFilter

        Parameters
        ----------
            messages: List
                Input queue got from incomingFilter
        Returns
        ------
            messages: List
                Processed message queue using user's logic
        """
        raise NotImplementedError(
            "transformMessageQueue should be defined in base clase"
        )


class FIFO(PipeStrategy):
    """First In First Out strategy

    It makes the first message from the incomingFilter
    to be processed first by the outgoingFilter
    and the last message from the incomingFilter to be
    processed last by the outgoinfFilter
    """

    def transformMessageQueue(self, messages):
        return messages


class LIFO(PipeStrategy):
    """Last in First Out strategy

    It makes the last message from the incomingFilter to be
    processed first by the outgoingFilter
    and the first message from the incomingFilter
    to be processed last by the outgoinfFilter
    """

    def transformMessageQueue(self, messages):
        return messages[::-1]
