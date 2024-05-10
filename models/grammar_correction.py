from happytransformer import HappyTextToText, TTSettings
from transformers import pipeline
import spacy
class Grammer_Correction:
    def __init__(self, file):
        #spacy.cli.download("en_core_web_lg")
        self.happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
        self.fix_spelling = pipeline("text2text-generation",model="oliverguhr/spelling-correction-english-base")
        self.args = TTSettings(num_beams=5, min_length=1)
        self.nlp = spacy.load("en_core_web_lg")
        self.text = self.nlp(file.decode("utf-8"))

    def generate_crted_text(self, texts):
        re=[]
        for text in texts:
            result = self.happy_tt.generate_text(f"grammar:{text}", args=self.args)
            #print(self.fix_spelling(result.text,max_length=4028))
            re.append(self.fix_spelling(result.text,max_length=4028)[0]['generated_text'])
        return re

    def get_sentences(self):
        sentence = ""
        sentences = []
        for i in self.text:
            if i.is_sent_end:
                if(i.is_punct):
                    sentence += i.text
                else:
                    sentence = sentence + " " + i.text
                sentences.append(sentence)
                sentence = ""
            else:
                sentence = sentence + " " + i.text
        else:
            if sentence.strip() != '':
                sentences.append(sentence)
        return sentences

    def crt_the_grammer(self):
        corrected_sentences = self.generate_crted_text(self.get_sentences())
        return ''.join(corrected_sentences)

    def make_grammer_error_free(self):
        return self.crt_the_grammer()

