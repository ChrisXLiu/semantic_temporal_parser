from iparser import IParser
import spacy


class SpacyParser(IParser):
    def parse_temporal_expression(self, text):
        doc = SpacyParser.nlp(text)
        temporal_entities = []
        for ent in doc.ents:
            if ent.label_ == "DATE" or ent.label_ == "TIME":
                temporal_entities.append(ent.text)
        return temporal_entities

    def parse(self, today, utterance):
        entities = self.parse_temporal_expression(utterance)
        return ",".join(entities)


SpacyParser.nlp = spacy.load("en_core_web_sm")
