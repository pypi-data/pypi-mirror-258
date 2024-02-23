from .LoadClassModel import LoadClassModel
from .LoadEmbeddsModel import LoadEmbeddsModel
from .TextCleaner import TextCleaner
import torch
import logging


logging.basicConfig(level=logging.INFO) 

class MailClassification:
    def __init__(self):
        self.classification_model = LoadClassModel.get_model_instance()
        self.embedding_model = LoadEmbeddsModel.get_model_instance()
        self.text_cleaner = TextCleaner()

    def predict(self, text):
        text = self.text_cleaner.decode_into_text(text) 
        cleaned_text = self.text_cleaner.clean(text)
        try:
            with torch.no_grad():
                embeddings = self.embedding_model.encode(cleaned_text)
                predictions = self.classification_model.predict(embeddings.reshape(1, -1),verbose = 0)
                return round(predictions[0][0])
        except Exception as e:
            logging.error("Error in predicting %s" , e)
