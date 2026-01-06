import os
import sys
from src.ML_Project.execption import CustomException
from src.ML_Project.loggers import logging
import pandas as pd
from src.ML_Project.utils import read_sql_data
from dataclasses import dataclass
from sklearn.model_selection import train_test_split


@dataclass
class DataIngestionConfig:
    traindata_path:str = os.path.join('artifacts', 'train.csv')
    testdata_path:str = os.path.join('artifacts', 'test.csv')
    rawdata_path:str = os.path.join('artifacts', 'raw.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config= DataIngestionConfig()

    def initiate_data_ingestion(self):
        try:
            df=read_sql_data()
            logging.info('Reading comp from MySql')

            os.makedirs(os.path.dirname(self.ingestion_config.traindata_path),exist_ok=True)

            df.to_csv(self.ingestion_config.rawdata_path,index=False,header=True)
            train_set,test_set = train_test_split(df,test_size=0.2, random_state=42)
            train_set.to_csv(self.ingestion_config.traindata_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.testdata_path,index=False,header=True)

            logging.info("Data ingestion is completed")

            return(
                self.ingestion_config.traindata_path,
                self.ingestion_config.testdata_path,

            ) 





        except Exception as e:
            raise CustomException(e,sys)
