import spacy
class plagarism_check:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")

    def tokenize_and_clean(self, text):
        tokens = self.nlp(text.lower())
        clean_tokens = []
        for token in tokens:
            if not token.is_stop and not token.is_punct and not token.is_space:
                clean_tokens.append(token.lemma_)
        return clean_tokens

    def generate_vectorized_data(self, text1, text2):
        word2vec = dict()
        no = 0
        for i in text1:
            if i not in word2vec.keys():
                word2vec[i] = no
                no += 1
        for i in text2:
            if i not in word2vec.keys():
                word2vec[i] = no
                no += 1
        return word2vec

    def convert_data_to_vectors(self, text1, text2):
        vector_representation = self.generate_vectorized_data(text1, text2)
        vdata1 = [vector_representation[i] for i in text1]
        vdata2 = [vector_representation[i] for i in text2]
        return (vdata1, vdata2)

    def generate_counter(self, vdata1, vdata2):
        counter1 = dict()
        counter2 = dict()
        for i in vdata1:
            if i in counter1.keys():
                counter1[i] += 1
            else:
                counter1[i] = 1
        for i in vdata2:
            if i in counter2.keys():
                counter2[i] += 1
            else:
                counter2[i] = 1
        return (counter1, counter2)

    def extract_similar(self, counter1, counter2):
        similarity_extraction = 0
        for i in counter1:
            if i in counter2.keys():
                similarity_extraction += min(counter1[i], counter2[i])
        return similarity_extraction

    def calculate_common_score(self, text1, text2):
        text1_tokens = self.tokenize_and_clean(text1)
        text2_tokens = self.tokenize_and_clean(text2)
        counter1, counter2 = self.generate_counter(text1_tokens, text2_tokens)
        common_score = self.extract_similar(counter1, counter2)
        total_tokens = max(len(text1_tokens), len(text2_tokens))
        similarity_score = (common_score / total_tokens) * 100
        return similarity_score