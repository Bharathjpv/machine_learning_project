import sys

from housingPrediction.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from housingPrediction.logger import logging
from housingPrediction.exception import HousingException
from housingPrediction.constant import *
from housingPrediction.util.util import read_yaml_file

class Configration:
    def __init__(self, config_file_path=CONFIG_FILE_PATH):
        try:
            self.config_info  = read_yaml_file(file_path=config_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = currentTime()
        except Exception as e:
            raise HousingException(e,sys) from e
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
                
            data_ingestion_artifact_dir=os.path.join(
                    artifact_dir,
                    DATA_INGESTION_ARTIFACT_DIR,
                    self.time_stamp
            )
            logging.info(f"Time stamp is {self.time_stamp}")  
            data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]

            dataset_download_url = data_ingestion_info[DATA_INGESTION_DOWNLOAD_URL_KEY]

            raw_data_dir = os.path.join(data_ingestion_artifact_dir,
                    data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY]
            )

            ingested_data_dir = os.path.join(
                    data_ingestion_artifact_dir,
                    data_ingestion_info[DATA_INGESTION_INGESTED_DIR_NAME_KEY]
            )
                    
            ingested_train_dir = os.path.join(
                    ingested_data_dir,
                    data_ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY]
            )
                    
            ingested_test_dir =os.path.join(
                    ingested_data_dir,
                    data_ingestion_info[DATA_INGESTION_TEST_DIR_KEY]
            )

            data_ingestion_config=DataIngestionConfig(
                    dataset_download_url=dataset_download_url,
                    raw_data_dir=raw_data_dir,
                    ingested_train_dir=ingested_train_dir,
                    ingested_test_dir=ingested_test_dir
            )

            logging.info(f"Data Ingestion config: {data_ingestion_config}")

            return data_ingestion_config

        except Exception as e:
            raise HousingException(e,sys) from e
    
    def get_training_pipeline_config(self) ->TrainingPipelineConfig:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR,
            training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
            training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
            )

            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f"Training pipleine config: {training_pipeline_config}")
            return training_pipeline_config
        except Exception as e:
            raise HousingException(e,sys) from e