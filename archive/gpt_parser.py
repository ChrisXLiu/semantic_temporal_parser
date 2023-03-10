import openai
import os
import re
from os.path import join, dirname
from dotenv import load_dotenv
from iparser import IParser


class GptParser(IParser):
    def __init__(self, spelling_correcter=None):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.spelling_correcter = spelling_correcter

    def parse(self, today, utterance):
        if self.spelling_correcter is not None:
            utterance = self.spelling_correcter.correct(utterance)

        semantic_parsing_prompt = """
Follow my examples and give me an answer.

Assuming reference date = '2023-02-24'
'Tomorrow at 11am' -> '2023-02-25 11:00'
'This coming Tuesday at 9pm' -> '2023-02-28 21:00'
'Next Tuesday at 9pm' -> '2023-02-28 21:00'
'Teuesdey oif Nexx weak att 9 pm' -> '2023-02-28 21:00'

Reference date = '{}'
'{}' -> ?
""".format(today, utterance)
        semantic_parsing_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            messages=[{"role": "system", "content": semantic_parsing_prompt}],
            max_tokens=50)
        raw_semantic_parsing_message = semantic_parsing_response.choices[0].message.content.strip(
        )
        semantic_parsing_matched = re.search(
            "'(\d\d\d\d-\d\d-\d\d \d\d:\d\d)'", raw_semantic_parsing_message)
        if semantic_parsing_matched is not None and len(semantic_parsing_matched.groups()) == 1:
            return semantic_parsing_matched.group(1)

        # print("Unrecognized pattern")
        return None
