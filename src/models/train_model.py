from typing import Tuple

import numpy as np
import pandas as pd
from category_encoders import TargetEncoder
from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer


def create_pipeline() -> Pipeline:
    """
    Create a pipeline for numeric data preprocessing.

    Returns:
        numeric_transformer (Pipeline): A pipeline object that includes the following steps:
            - imputer: An imputer object that replaces missing values with the mean.
            - log_transformer: A transformer object that applies the natural logarithm transformation to the data.

    """
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('log_transformer', FunctionTransformer(np.log1p, validate=True))
    ])

    return numeric_transformer


def apply_log1p_transformation(data, numeric_transformer: BaseEstimator) -> np.ndarray:
    """
    Apply a log1p transformation to the given data using the specified numeric transformer.

    Parameters:
        data (array-like): The input data to apply the transformation to.
        numeric_transformer (object): The numeric transformer object used to apply the transformation.

    Returns:
        array-like: The transformed data after applying the log1p transformation.
    """
    transformed_data = numeric_transformer.transform(data)  # type: ignore
    return transformed_data


def apply_target_encoder(data: pd.DataFrame, target_column: str) -> pd.DataFrame:
    """
    Apply Target Encoding to categorical data using the specified target column.

    Parameters:
        data (pd.DataFrame): The input DataFrame containing categorical data.
        target_column (str): The name of the target column for encoding.

    Returns:
        pd.DataFrame: The DataFrame with target-encoded categorical columns.
    """
    encoder = TargetEncoder()
    encoded_data = encoder.fit_transform(data, target_column)
    return encoded_data


def split_data(df: pd.DataFrame, target_column: str = 'preco', random_state=42) -> tuple:
    """
    Split the input DataFrame into training and testing sets for machine learning.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing the dataset.
        target_column (str, optional): The name of the target column. Defaults to 'preco'.

    Returns:
        tuple: A tuple containing four DataFrames - X_treino, X_teste, y_treino, y_teste.
    """
    X = df.drop(target_column, axis=1)
    y = df[target_column]
    X_treino, X_teste, y_treino, y_teste = train_test_split(X, y,
                                                            test_size=0.3,  # noqa
                                                            random_state=random_state)  # noqa
    return X_treino, X_teste, y_treino, y_teste


def train_model(data: pd.DataFrame, X_treino: pd.DataFrame, y_treino: pd.Series) -> Tuple[np.ndarray, float, float, float]:
    """
    Train a machine learning model and evaluate its performance on the test set.

    Parameters:
        data (pd.DataFrame): The input DataFrame containing the dataset.
        X_treino (pd.DataFrame): The training feature data.
        y_treino (pd.Series): The training target data.

    Returns:
        Tuple[np.ndarray, float, float, float]: A tuple containing the predictions, Mean Absolute Error (MAE),
        Mean Squared Error (MSE), and R-squared (R2) scores.
    """
    optimized_rf = RandomForestRegressor(n_estimators=2, random_state=42,
                                         min_samples_split=2,
                                         min_samples_leaf=1, max_depth=2)

    optimized_rf.fit(X_treino, y_treino)
    X_treino, X_teste, y_treino, y_teste = split_data(data, random_state=42)
    predict_ = optimized_rf.predict(X_teste)

    mae = float(mean_absolute_error(y_teste, predict_))
    mse = float(mean_squared_error(y_teste, predict_))
    r2 = float(r2_score(y_teste, predict_))

    print('Resultado de métrica do modelo de machine learning:')
    print()
    print('=' * 30)
    print(f'Mean Absolute Error (MAE): {round(mae, 2)}')
    print('=' * 30)
    print(f'Mean Squared Error (MSE): {round(mse, 2)}')
    print('=' * 30)
    print(f'R-squared (R2): {round(r2 * 100, 2)}%')
    print('=' * 30)

    return predict_, mae, mse, r2
