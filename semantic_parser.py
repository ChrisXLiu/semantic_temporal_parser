
from iparser import IParser
from regex_parser import RegexParser
from gpt_parser import GptParser
from spelling_correcter import SpellingCorrecter
from istrategy import IStrategy
from first_success_strategy import FirstSuccessStrategy
import datetime


def parse_utterance(today, utterance):
    parsers = [RegexParser(), GptParser(), GptParser(SpellingCorrecter())]
    strategy = FirstSuccessStrategy()
    return strategy.run(today, utterance, parsers)


def main():
    # In the real use cases, `today` should reflect client timezone instead of
    # server timezone.
    today = datetime.datetime.strftime(datetime.date.today(), "%Y-%m-%d")
    utterance = input("Type a temporal utterance: ")
    result = parse_utterance(today, utterance)
    if result is None:
        print("Sorry, I didn't get that.")
    else:
        print(result)


if __name__ == "__main__":
    main()
