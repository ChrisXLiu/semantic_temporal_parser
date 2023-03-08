import openai
import os
import re
from os.path import join, dirname
from dotenv import load_dotenv


class SpellingCorrecter:
    def __init__(self):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def correct(self, utterance):
        spell_correction_prompt = """
Try correcting the spelling of these phrases about date and time:
Input: 'Teuesdey oif Nexx weak att 9 pm'
Output: 'Tuesday of Next week at 9 pm'

Input: 'Frday at nooon'
Output: 'Friday at noon'

Input: 'Monday 3 pm'
Output: 'Monday 3 pm'

Input: '{}'
Output: ?
""".format(utterance)
        spell_correction_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            messages=[{"role": "system", "content": spell_correction_prompt}],
            max_tokens=50)
        raw_spell_corrected_message = spell_correction_response.choices[0].message.content.strip(
        )
        spell_correction_matched = re.search(
            "(?:Output:\s*)?'([^']+?)'", raw_spell_corrected_message)
        if spell_correction_matched is not None and len(spell_correction_matched.groups()) == 1:
            return spell_correction_matched.group(1)

        return utterance
