import pandas as pd

from src.features.clean_data import clean_and_extract_data
from src.features.config import CLEAN_WANT_DF, DADOS, LL_DF
from src.models.train_model import (apply_log1p_transformation,
                                    apply_target_encoder, create_pipeline,
                                    split_data, train_model)


def main() -> None:
    """
    Generates a comment for the given function body.

    This function takes no parameters and does not return anything. It reads two CSV files, CLEAN_WANT_DF and LL_DF, using the pandas read_csv function. It then calls the clean_and_extract_data function with the two dataframes as arguments and assigns the result to the variable resulting_df. The resulting_df dataframe is then saved to a CSV file named 'name_you_want.csv' using the to_csv method.

    The function then assigns the value of the DADOS variable to the data variable. It creates a numeric_transformer object using the create_pipeline function and applies it to the numeric columns of the data dataframe using the fit method of the numeric_transformer object. The result of the transformation is assigned to the transformed_data variable using the apply_log1p_transformation function.

    The function selects the categorical columns of the data dataframe using the select_dtypes method with the argument 'object' and assigns the result to the categoric_variable variable. It then selects the categorical data from the data dataframe using the categoric_variable variable and assigns the result to the categoric_data variable. The apply_target_encoder function is then called with the categoric_data and data['preco'] as arguments and the result is assigned to the encoded_data variable.

    The function concatenates the encoded_data dataframe and a dataframe created from the transformed_data array, using the columns of the numeric_data dataframe as column names. The result is assigned to the data dataframe.

    The function then calls the split_data function with the data dataframe as an argument and assigns the returned values to the variables X_treino, X_teste, y_treino, and y_teste.

    Finally, the function calls the train_model function with the data, X_treino, and y_treino as arguments and assigns the returned values to the variables predict_, mae, mse, and r2.

    This function is the main entry point of the program and is executed when the script is run.

    """
    df = pd.read_csv(CLEAN_WANT_DF, sep=';')

    df_2 = pd.read_csv(LL_DF, sep=';')

    resulting_df = clean_and_extract_data(df, df_2)

    resulting_df.to_csv('data/processed/name_you_want.csv', index=False)

    data = DADOS

    numeric_transformer = create_pipeline()
    numeric_data = data.select_dtypes(exclude=['object'])
    numeric_transformer.fit(numeric_data)

    transformed_data = apply_log1p_transformation(numeric_data,
                                                  numeric_transformer)

    categoric_variable = data.select_dtypes(include=['object']).columns
    categoric_data = data[categoric_variable]
    encoded_data = apply_target_encoder(
        categoric_data, data['preco'])  # type: ignore

    data = pd.concat([encoded_data, pd.DataFrame(transformed_data,
                                                 columns=numeric_data.columns)],
                     axis=1)

    X_treino, X_teste, y_treino, y_teste = split_data(data)

    predict_, mae, mse, r2 = train_model(data, X_treino, y_treino)


if __name__ == "__main__":
    main()
