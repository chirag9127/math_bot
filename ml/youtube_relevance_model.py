import os
import pickle
os.environ['KERAS_BACKEND'] = 'theano'

from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

from helper_scripts.singleton import Singleton

MAX_SEQUENCE_LENGTH = 100


@Singleton
class YoutubeRelevanceModel:

    def __init__(self):
        self.tokenizer = pickle.load(
            open(os.path.dirname(__file__) + '/tokenizer.p', 'rb'))
        self.model = load_model(os.path.dirname(__file__) + '/best_model.h5')

    def predict(self, data):
        query_sequences = self.tokenizer.texts_to_sequences(data['query'])
        title_sequences = self.tokenizer.texts_to_sequences(data['title'])
        desc_sequences = self.tokenizer.texts_to_sequences(data['description'])
        query_data = pad_sequences(query_sequences, maxlen=MAX_SEQUENCE_LENGTH)
        title_data = pad_sequences(title_sequences, maxlen=MAX_SEQUENCE_LENGTH)
        desc_data = pad_sequences(desc_sequences, maxlen=MAX_SEQUENCE_LENGTH)
        preds = self.model.predict([query_data, title_data, desc_data])
        return preds

