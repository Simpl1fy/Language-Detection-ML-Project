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

        except:
            pass