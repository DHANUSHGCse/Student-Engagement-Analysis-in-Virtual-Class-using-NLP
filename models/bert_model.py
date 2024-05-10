from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize
model = SentenceTransformer('bert-base-nli-mean-tokens')
def read_and_tokenize_text(text):
    sentences = sent_tokenize(text)
    return sentences
def calculate_similarity_score(text1, text2):
    sentences_doc1 = read_and_tokenize_text(text1)
    sentences_doc2 = read_and_tokenize_text(text2)
    embeddings_doc1 = model.encode(sentences_doc1)
    embeddings_doc2 = model.encode(sentences_doc2)

    similarity_scores = cosine_similarity(embeddings_doc1, embeddings_doc2)

    return similarity_scores.mean()



