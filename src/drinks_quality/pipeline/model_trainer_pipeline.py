from drinks_quality import logger
from drinks_quality.config.configuration import Configuration
from drinks_quality.components.model_trainer import ModelTrainer

class ModelTrainerPipeline:
    def __init__(self):
        self.config = Configuration()
    
    def run_pipeline(self):
        logger.info("Starting Model Trainer Pipeline")
        model_trainer_config = self.config.get_model_trainer_config()
        model_trainer = ModelTrainer(config=model_trainer_config)
        model_trainer.train_model()
        logger.info("Model Trainer Pipeline completed successfully")
if __name__ == "__main__":
    pipeline = ModelTrainerPipeline()
    pipeline.run_pipeline()