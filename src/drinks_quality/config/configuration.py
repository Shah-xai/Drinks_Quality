from drinks_quality import logger
from drinks_quality.utils.common import read_yaml, create_directories
from drinks_quality.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from drinks_quality.constants import *

class Configuration:
    def __init__(self, config_file_path = CONFIG_FILE_PATH, 
                 schema_file_path = SCHEMA_FILE_PATH
                 ):
        self.config_info = read_yaml(config_file_path)
        self.schema_info = read_yaml(schema_file_path)
        logger.info(f"Configuration loaded from {config_file_path}")
        create_directories([self.config_info.get("artifact_root", "artifacts")])
    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        data_ingestion_info = self.config_info.get("data_ingestion", {})
        create_directories([data_ingestion_info.get("root_dir", "")])
        return DataIngestionConfig(
            root_dir=data_ingestion_info.get("root_dir", ""),
            source_URL=data_ingestion_info.get("source_URL", ""),
            local_data_file=data_ingestion_info.get("local_data_file", "")
        )
    def get_data_validation_config(self):
        data_validation_info = self.config_info.get("data_validation", {})
        create_directories([data_validation_info.get("root_dir", "")])
        return DataValidationConfig(
            root_dir=data_validation_info.get("root_dir", ""),
            data_file=data_validation_info.get("data_file", ""),
            report_file_path=data_validation_info.get("report_file_path", ""),
            schema=self.schema_info
        )
    def get_data_transformation_config(self):
        data_transformation_info = self.config_info.get("data_transformation", {})
        create_directories([data_transformation_info.get("root_dir", "")])
        return DataTransformationConfig(
            root_dir=data_transformation_info.get("root_dir", ""),
            data_file=data_transformation_info.get("data_file", ""),
            target_column=self.schema_info.get("target", {}).get("name", "")

        )
    
