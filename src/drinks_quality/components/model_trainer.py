import os
from drinks_quality.entity.config_entity import ModelTrainerConfig 
from drinks_quality.utils.common import save_bin 
from sklearn.svm import SVC
import pandas as pd

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train_model(self):
        # Placeholder for model training logic
        print(f"Training model with data from {self.config.data_file} and saving to {self.config.root_dir}")
        # Load the training data
        data = pd.read_csv(self.config.data_file)
        X = data.drop(self.config.target_column, axis=1)  # Assuming target_column is the label column
        y = data[self.config.target_column]
        model_params = self.config.class_weight, self.config.kernel
        model = SVC(class_weight=model_params[0], kernel=model_params[1])
        model.fit(X, y)
        # Save the model to the specified directory
        model_path = os.path.join(self.config.root_dir, self.config.model_name)
        # Here you would typically use joblib or pickle to save the model
        save_bin(model, model_path)
        print(f"Model saved to {model_path}")