import re

import numpy as np
import pandas as pd


def clean_and_extract_data(df: pd.DataFrame, df_2: pd.DataFrame) -> pd.DataFrame:  # noqa
    """
    Cleans and extracts data from a DataFrame.

    Parameters:
    - df: The input DataFrame containing the data.
    - df_2: Another DataFrame to be merged with `df`.

    Returns:
    - df: The cleaned and extracted DataFrame.
    """
    def remove_motor_ano_nome(texto: str) -> str:
        """
        Removes motor, year, name, and additional patterns from the given text.

        Args:
            texto (str): The text from which to remove the patterns.

        Returns:
            str: The text with the patterns removed.
        """
        motor = r'\d+\.\d+'
        ano = r'\b\d{4}\b'
        nome = r'\(.+\)'
        padroes_adicionais = r'\s?2p|\s?4p|\s?2P|\s?4P|\s?8V|\s?12v|\s?12V|\s?16V|\s?20V'  # noqa

        texto = re.sub(motor, '', texto)
        texto = re.sub(ano, '', texto)
        texto = re.sub(nome, '', texto)
        texto = re.sub(padroes_adicionais, '', texto)

        return texto.strip()

    cilindrada = {}
    for i in range(10, 41):
        valor = f'{i / 10:.1f}'
        cilindrada[valor] = int(i * 100)

    def extract_cilindrada(modelo: str) -> str:
        """
        Extracts the cilindrada from the given modelo.

        Parameters:
            modelo (str): The modelo string from which to extract the cilindrada.

        Returns:
            str: The extracted cilindrada.

        """
        for key in cilindrada.keys():
            if key in modelo:
                return key
        return ''

    df = df.merge(df_2[['municipio', 'longitude', 'latitude']],
                  left_on='cidade', right_on='municipio', how='inner')
    df.rename(columns={'longitude_copia': 'longitude',
                       'latitude_copia': 'latitude'}, inplace=True)
    df.drop(['municipio', 'longitude', 'latitude'], axis=1, inplace=True)
    df = df.sample(frac=1).reset_index(drop=True)
    df['preco'] = df['preco'].str.replace("R$", "")
    df.dropna(inplace=True)
    df['preco'] = df['preco'].str.replace('R$', '').str.replace(
        '.', '').str.replace(',', '.').astype(float)
    df['km'] = df['km'].apply(lambda x: np.nan if x == 'N/D' else float(x))
    df = df.drop('câmbio automático', axis=1)
    df.rename(columns={
              'distribuição eletrônica de frenagem,': 'distribuição eletrônica de frenagem'}, inplace=True)
    df['motor'] = df['modelo'].apply(extract_cilindrada).map(cilindrada)
    df['modelo'] = df['modelo'].apply(remove_motor_ano_nome)

    return df
