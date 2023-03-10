from istrategy import IStrategy
from collections import defaultdict


class MajorityVoteStrategy(IStrategy):
    def run(self, today, utterance, parsers):
        candidates = defaultdict(int)
        non_null_vote_count = 0
        for parser in parsers:
            ret = parser.parse(today, utterance)
            if ret is not None:
                candidates[ret] += 1
                non_null_vote_count += 1
        if len(candidates) > 0 and \
                max(candidates.values()) > non_null_vote_count / 2:
            return max(candidates, key=candidates.get)
        return None
