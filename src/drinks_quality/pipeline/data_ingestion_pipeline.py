from drinks_quality.config.configuration import Configuration
from drinks_quality.components.data_ingestion import DataIngestion
from drinks_quality import logger

class DataIngestionPipeline:
    def __init__(self, config: Configuration):
        self.config = config

    def start_data_ingestion(self):
        data_ingestion_config = self.config.get_data_ingestion_config()
        logger.info(f"Data Ingestion Config: {data_ingestion_config}")
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_data()
        logger.info("Data download completed.")

if __name__ == "__main__":
    config = Configuration()
    data_ingestion_pipeline = DataIngestionPipeline(config=config)
    data_ingestion_pipeline.start_data_ingestion()