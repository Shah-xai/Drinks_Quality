import os
from pathlib import Path
from drinks_quality import logger
from drinks_quality.entity.config_entity import DataIngestionConfig 
from urllib import request
from drinks_quality.utils.common import get_size, load_bin 

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
    
    def download_data(self):
        logger.info(f"Downloading data from {self.config.source_URL} to {self.config.local_data_file}")
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url=self.config.source_URL,
                filename=self.config.local_data_file
            )
            logger.info(f"Downloaded file {filename} with info: \n{headers}")
  
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")