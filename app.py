from src.ML_Project.loggers import logging
from src.ML_Project.execption import CustomException
import sys
from src.ML_Project.components.data_ingestion import DataIngestion
from src.ML_Project.components.data_ingestion import DataIngestionConfig
from src.ML_Project.components.data_transformation import DataTransformationConfig, DataTransformation




if __name__=="__main__":
    logging.info("The execution has started ")


    try:
        # data_ingestion_config=DataIngestionConfig()
        data_ingestion=DataIngestion()
        train_data_path,test_data_path=data_ingestion.initiate_data_ingestion()
        
        data_tranformation=DataTransformation()
        data_tranformation.initiate_data_tranformation(train_data_path,test_data_path)




    except Exception as e:
        logging.info('Custom exception')
        raise CustomException(e,sys)