from abc import ABCMeta, abstractmethod


class IParser:
    __metaclass__ = ABCMeta

    # Parses a temporal utterance string relative to `today`.
    # `today` is assumed to be in the format of "YYYY-mm-dd".
    @abstractmethod
    def parse(self, today, utterance) -> str | None: raise NotImplementedError
