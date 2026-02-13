from drinks_quality import logger
from drinks_quality.entity.config_entity import ModelEvaluationConfig
from drinks_quality.utils.common import save_json, load_bin
from sklearn.metrics import classification_report, roc_auc_score
from pathlib import Path
import pandas as pd
class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def evaluate_model(self):
        # Placeholder for model evaluation logic
        logger.info(f"Evaluating model from {self.config.model_file} using data from {self.config.data_file}")
        # Load the model
        model = load_bin(Path(self.config.model_file))
        # Load the test data
        data = pd.read_csv(self.config.data_file)
        X_test = data.drop(self.config.target_column, axis=1)  # Assuming target_column is the label column
        y_test = data[self.config.target_column]
        # Make predictions
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None
        # Calculate metrics
        report = classification_report(y_test, y_pred, output_dict=True)
        if y_prob is not None:
            roc_auc = roc_auc_score(y_test, y_prob)
            report['roc_auc'] = roc_auc
        # Save metrics to a JSON file
        metrics_path = Path(f"{self.config.root_dir}/{self.config.metrics_file_name}")
        save_json(metrics_path, report)
        logger.info(f"Metrics saved to {metrics_path}")