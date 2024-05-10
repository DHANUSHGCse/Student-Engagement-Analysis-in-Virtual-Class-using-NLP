from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

class originality_checker:
    def __init__(self, text):
        self.model = load_model(r'C:\Users\maste\finalyearproject\models\valid_notes_check_model.h5')
        self.text = text
    def perform_pad(self):
        length = 10129
        encoded_vector = self.perform_onehot()
        padded_vector = pad_sequences([encoded_vector], maxlen=length, padding='post')
        return padded_vector
    def perform_onehot(self):
        vocab_size = 393537
        return one_hot(str(self.text), vocab_size)  # Ensure 'text' is converted to string

    def compute_model(self):
        padded_string = self.perform_pad()
        score = self.model.predict(np.array(padded_string))
        return score[0][0]

