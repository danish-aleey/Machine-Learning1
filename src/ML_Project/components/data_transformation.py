import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.ML_Project.execption import CustomException
from src.ML_Project.loggers import logging
import os
from src .ML_Project.utils import save_object



@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    
    def get_data_transformer_obj(self):
        # this function is responsible for data transformation

        try:
            numerical_columns=['writing_score','reading_score']
            categorical_columns=[
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course',
            ]
            num_pipline =Pipeline(steps=[
                ("imputre",SimpleImputer(strategy='median')),
                ("scalar", StandardScaler())
            ])
            cat_pipline=Pipeline(steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scalar",StandardScaler(with_mean=False))
            ])

            logging.info(f"Numerical Columns:{numerical_columns}")  
            logging.info(f"Categorical Columns:{categorical_columns}") 

            preprocessor=ColumnTransformer(
                [
                    ("num_pipline",num_pipline,numerical_columns),
                    ("cat_pipline",cat_pipline,categorical_columns)
                ]
            )
            return preprocessor
  
        
        except Exception as e:
            raise CustomException(e,sys)
        
    
    def initiate_data_tranformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Reading the train test file")
            preprocessing_obj=self.get_data_transformer_obj()

            target_column_name="math_score"
            numerical_columns=['writing_score','reading_score']

            #divide the train dataset to independet and dependent dataset

            input_features_train_df=train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df=train_df[target_column_name]

            #divide the test dataset to independent and dependent dataset
            input_features_test_df=test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info("Applying preprocessor on training and testing dataset")

            input_feature_train_arry=preprocessing_obj.fit_transform(input_features_train_df)
            input_feature_test_arry=preprocessing_obj.transform(input_features_test_df)

            train_arr = np.c_[
                input_feature_train_arry, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arry, np.array(target_feature_test_df)]

            logging.info(f"Saved Preprocessing object")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )









        except Exception as e:
            raise CustomException(e,sys)