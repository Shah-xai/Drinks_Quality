from drinks_quality import logger
from drinks_quality.utils.common import read_yaml, create_directories
from drinks_quality.entity.config_entity import DataIngestionConfig
from drinks_quality.constants import *

class Configuration:
    def __init__(self, config_file_path = CONFIG_FILE_PATH):
        self.config_info = read_yaml(config_file_path)
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
    
