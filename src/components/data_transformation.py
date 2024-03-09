import sys
import os

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer

from src.logger import logging
from src.exception import CustomException
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocesor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transfomation_config_obj=DataTransformationConfig()
    
    def get_data_transformation_object(self):
        '''
            This function is responsible for data transformation
        '''

        try:
            input_column = ['Text']
            output_column = ['Language']

            # Creating pipeline for input column
            input_pipeline = Pipeline(
                steps=[
                    ("count vectorizer", CountVectorizer())
                ]
            )

            # Pipeline for output
            output_pipeline = Pipeline(
                steps=[
                    "label encoder", LabelEncoder()
                ]
            )

            logging.info(f"Input Features: {input_column}")
            logging.info(f"Output Features: {output_column}")

            # Creating a preprocessor to transform both input and output columns
            preprocessor = ColumnTransformer(
                [
                    ("input_pipeline", input_pipeline, input_column)
                    ("output_pipeline", output_pipeline, output_column)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)


        # Creating a function for initiating data transformation
    def initiate_data_transformation(self, train_path, test_path):

        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Reading the training and testing csv into a dataframe")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj=self.get_data_transformation_object()

            target_column_name = "Language"
            input_column_name = "Text"

            logging.info("Applying the preprocessor object to training and testing dataset")

            train_arr = preprocessing_obj.fit_transform(train_df)
            test_arr = preprocessing_obj.fit_transform(test_df)

            logging.info("Saving the preprocessing object")
            save_object(
                file_path = self.data_transfomation_config_obj.preprocessor_obj_file_path
                obj = preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transfomation_config_obj.preprocessor_obj_file_path
            )
        except Exception as e:
            raise CustomException(e, sys)
            