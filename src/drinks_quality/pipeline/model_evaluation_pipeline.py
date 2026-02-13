from drinks_quality import logger
from drinks_quality.config.configuration import Configuration
from drinks_quality.components.model_evaluation import ModelEvaluation

class ModelEvaluationPipeline:
    def __init__(self, config: Configuration):
        self.config = config

    def run_pipeline(self):
        logger.info("Starting model evaluation pipeline.")
        model_evaluation_config = self.config.get_model_evaluation_config()
        model_evaluation = ModelEvaluation(model_evaluation_config)
        model_evaluation.evaluate_model()
        logger.info("Model evaluation pipeline completed.")
    
if __name__ == "__main__":
    config = Configuration()
    pipeline = ModelEvaluationPipeline(config)
    pipeline.run_pipeline()