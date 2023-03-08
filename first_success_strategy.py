from istrategy import IStrategy


class FirstSuccessStrategy(IStrategy):
    def run(self, today, utterance, parsers):
        for parser in parsers:
            ret = parser.parse(today, utterance)
            if ret is not None:
                return ret
        return None
