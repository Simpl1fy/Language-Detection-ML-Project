import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig


@dataclass
class DataIngestionConfig:
    train_data_path:str = os.path.join('artifact', 'train.csv')
    test_data_path:str = os.path.join('artifact', 'test.csv')
    raw_data_path:str = os.path.join('artifact', 'raw.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method")
        try:
            df = pd.read_csv('notebook\data\Language Detection.csv')
            logging.info("read csv file as dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            # Saving the raw file
            df.to_csv(self.ingestion_config.raw_data_path, header=True, index=False)

            # Splitting the data into training and testing
            logging.info("Initiated train test split")
            train_set, test_set = train_test_split(df, test_size=0.2)

            train_set.to_csv(self.ingestion_config.train_data_path,header=True, index=False)
            test_set.to_csv(self.ingestion_config.test_data_path, header=True, index=False)

            logging.info("Ingestion of Data is completed")

            return(

                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e, sys)

if __name__=="__main__":
    obj=DataIngestion()
    train_data, test_data=obj.initiate_data_ingestion()
    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_data, test_data)