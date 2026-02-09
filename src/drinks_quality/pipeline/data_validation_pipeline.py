from drinks_quality.config.configuration import Configuration
from drinks_quality.components.data_validation import DataValidation
from drinks_quality import logger

class DataValidationPipeline:
    def __init__(self, config: Configuration):
        self.config = config

    def start_data_validation(self):
        data_validation_config = self.config.get_data_validation_config()
        logger.info(f"Data Validation Config: {data_validation_config}")
        data_validation = DataValidation(config=data_validation_config)
        validation_result = data_validation.run_validation()
        if validation_result:
            logger.info("Data validation completed successfully.")
        else:
            logger.error("Data validation failed.")

if __name__ == "__main__":
    config = Configuration()
    data_validation_pipeline = DataValidationPipeline(config=config)
    data_validation_pipeline.start_data_validation()