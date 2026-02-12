import os
import yaml
from anyio import Path
from drinks_quality.config.configuration import Configuration
from drinks_quality.components.data_transformation import DataTransformation
from drinks_quality import logger

class DataTransformationPipeline:
    def __init__(self, config: Configuration):
        self.config = config
    def run_pipeline(self):
        try:
            with open(Path("artifacts\\data_validation\\report.yaml"), "r") as f:
                report = yaml.safe_load(f)
                if report["status"] == "Failed":
                    logger.error("Data validation failed. Check the report for details.")
                    return
                else:
                    data_transformation_config = self.config.get_data_transformation_config()
                    logger.info(f"Running data transformation pipeline for config: {data_transformation_config}")
                    data_transformation = DataTransformation(data_transformation_config)
                    data_transformation.run_transformation()
        except Exception as e:
            logger.error(f"Error reading data validation report: {e}")
            return
        
if __name__ == "__main__":
    config = Configuration()
    data_transformation_pipeline = DataTransformationPipeline(config=config)
    data_transformation_pipeline.run_pipeline()