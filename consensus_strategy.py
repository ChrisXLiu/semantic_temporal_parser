from istrategy import IStrategy


class ConsensusStrategy(IStrategy):
    def run(self, today, utterance, parsers):
        candidates = set()
        for parser in parsers:
            ret = parser.parse(today, utterance)
            if ret is not None:
                candidates.add(ret)
        if len(candidates) == 1:
            return list(candidates)[0]
        return None
