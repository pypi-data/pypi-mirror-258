import re
from bs4 import BeautifulSoup
import spacy
from .WordReplacements import word_replacements
import logging
import base64

logging.basicConfig(level=logging.INFO) 


class NLPOBJ:
    _instance = None
    
    def __new__(cls,*args,**kwargs):
        if NLPOBJ._instance is None:
            spacy.cli.download("en_core_web_lg")
            
            NLPOBJ._instance = spacy.load("en_core_web_lg")
        return NLPOBJ._instance




class TextCleaner:
    irr_words = ["//n", "//r", "/n", "/r", "\n", '\r' , '\\r','\\n']
    stop_words = ['dear' , 'mr' , 'telix' , 'msg' , 'ref','fm','good','day' , 'woorim','sbm','sh','mm']
        
    @classmethod
    def clean_text(self, text):
        try:
            soup = BeautifulSoup(text, "html.parser")
            text = soup.get_text()
            text = text.lower()
            pattern = '|'.join(map(re.escape, self.irr_words))
            text = re.sub(pattern, ' ', text)
            content_before_disclaimer = re.search(r'(.+?)\bdisclaimer\b', text, re.DOTALL)
            if content_before_disclaimer:
                text = content_before_disclaimer.group(1).strip()
            # Replace 'm[./]v' with 'mv'
            text = re.sub(r'm[./]v', 'mv', text)
            return text
        except Exception as e:
            print("Cleaning text failed")
            return None
        
    @classmethod
    def clean(self , text):
        try:
            nlp = NLPOBJ()
            text = TextCleaner.clean_text(text)
            words_list = []
            doc = nlp(text)
            for token in doc:
                if token.is_alpha:
                    word_to_append = token.text.lower()
                    if word_to_append in word_replacements:
                        word_to_append = word_replacements[word_to_append]
                    if word_to_append not in self.stop_words and len(word_to_append)>1:
                        words_list.append(word_to_append)
                    
            replaced_text = ' '.join(words_list)
            return replaced_text
        except Exception as e:
            print("Cleaning Failed")
            return None
        

    def decode_into_text(self, text):
        try:
            decoded_bytes = base64.b64decode(text)
            decoded_text = decoded_bytes.decode('utf-8')
            return decoded_text
        except Exception as e:
            logging.error("Given input is not in base64 form")
                