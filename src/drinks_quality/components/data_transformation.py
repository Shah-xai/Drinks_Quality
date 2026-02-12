from pathlib import Path
from drinks_quality.config.configuration import Configuration
from drinks_quality.utils.common import save_bin
from drinks_quality import logger
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer

import pandas as pd
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline


class DataTransformation:
    def __init__(self, config: Configuration):
        self.config = config
    def run_transformation(self):
        data_transformation_config = self.config
        logger.info(f"Running data transformation for config: {data_transformation_config}")
        df = pd.read_csv(data_transformation_config.data_file)
        logger.info(f"Data loaded with shape: {df.shape}")
        train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
        logger.info(f"Train set shape: {train_set.shape}, Test set shape: {test_set.shape}")
        target_col = data_transformation_config.target_column
        X_train = train_set.drop(columns=[target_col])
        y_train = train_set[target_col].reset_index(drop=True)

        X_test = test_set.drop(columns=[target_col])
        y_test = test_set[target_col].reset_index(drop=True)

        numeric_features = X_train.select_dtypes(include=["int64", "float64"]).columns.tolist()
        logger.info(f"Numeric features: {numeric_features}")

    # preprocess
        numeric_transformer = make_pipeline(KNNImputer(), StandardScaler())
        preprocessor = make_column_transformer(
        (numeric_transformer, numeric_features),
        remainder="drop"
    )

# transform
        X_train_t = preprocessor.fit_transform(X_train[numeric_features])
        X_test_t = preprocessor.transform(X_test[numeric_features])

    # back to DataFrame (keep feature names)
        X_train_t_df = pd.DataFrame(X_train_t, columns=numeric_features)
        X_test_t_df = pd.DataFrame(X_test_t, columns=numeric_features)

# add target back
        train_final = pd.concat([X_train_t_df, y_train.rename(target_col)], axis=1)
        test_final = pd.concat([X_test_t_df, y_test.rename(target_col)], axis=1)

    # save
        train_final.to_csv("artifacts/data_transformation/train_transformed.csv", index=False)
        test_final.to_csv("artifacts/data_transformation/test_transformed.csv", index=False)
        save_bin(preprocessor, Path("artifacts/data_transformation/preprocessor.joblib"))

        logger.info("Data transformation completed and saved.")