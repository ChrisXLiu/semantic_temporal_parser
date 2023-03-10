from abc import ABCMeta, abstractmethod


class IStrategy:
    __metaclass__ = ABCMeta

    # Runs some or all provided parsers on the given input
    # `today` and `utterance`. Returns a final decision based on some
    # aggregation logic.
    # See `IParser` for more information.
    @abstractmethod
    def run(self, today, utterance, parsers) -> str | None:
        raise NotImplementedError
