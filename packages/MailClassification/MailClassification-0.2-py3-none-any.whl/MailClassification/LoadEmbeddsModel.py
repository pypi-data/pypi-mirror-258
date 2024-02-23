import os
import logging
import zipfile
import requests
from sentence_transformers import SentenceTransformer


logging.basicConfig(level=logging.INFO) 



class LoadEmbeddsModel:
    Embedding_Model_Url = "https://d2olrrfwjazc7n.cloudfront.net/website/assets/entity_extraction_model/classification/Embedding_Model.zip"
    BASE_DIR = os.getcwd()
    local_zip_file_path = os.path.join(BASE_DIR, 'Embedding_Model.zip')
    extract_to = BASE_DIR
    modelInstance = None

    @classmethod
    def get_model_instance(cls):
        if cls.modelInstance is None:
            cls.modelInstance = cls.load_model()
        return cls.modelInstance
    
       
    @classmethod
    def load_model(cls):
        try:
            logging.info("Checking Model File")
            if os.path.exists(cls.local_zip_file_path) and os.path.exists(os.path.join(cls.extract_to, 'Embedding_Model')):
                logging.info("Loading Pretrained Model")
                model = SentenceTransformer(os.path.join(cls.extract_to, 'Embedding_Model'))
                logging.info("Model has been loaded")
                return model
            
            elif os.path.exists(cls.local_zip_file_path):
                logging.info("Unzipping File to: %s", cls.extract_to)
                with zipfile.ZipFile(cls.local_zip_file_path, 'r') as zip_ref:
                            os.makedirs(cls.extract_to, exist_ok=True)
                            zip_ref.extractall(cls.extract_to)
                            logging.info("Zip file extracted to %s", cls.extract_to)

                model = SentenceTransformer(cls.extract_to, 'Embedding_Model')

                logging.info("Model has been loaded")
                return model

            else:
                try:
                    logging.info("Downloading Model File")
                    response = requests.get(cls.Embedding_Model_Url)

                    if response.status_code == 200:
                        logging.info("Response Code: %s", response.status_code)

                        with open(cls.local_zip_file_path, 'wb') as file:
                            file.write(response.content)

                        logging.info("File downloaded to %s", cls.local_zip_file_path)
                        logging.info("Unzipping File to: %s", cls.extract_to)

                        with zipfile.ZipFile(cls.local_zip_file_path, 'r') as zip_ref:
                            os.makedirs(cls.extract_to, exist_ok=True)
                            zip_ref.extractall(cls.extract_to)
                            logging.info("Zip file extracted to %s", cls.extract_to)

                        model = SentenceTransformer(os.path.join(cls.extract_to, 'Embedding_Model'))

                        logging.info("Model has been loaded")
                        return model
                    else:
                        logging.error("Failed to download the file")
                        return None
                except Exception as e:
                    logging.error("Error %s", e)
                    return None
        except Exception as e:
            logging.error("Error %s", e)
            return None
