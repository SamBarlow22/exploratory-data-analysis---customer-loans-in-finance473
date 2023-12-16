import pandas as pd

class ColumnConverter:

    @staticmethod
    def convert_term_column(column):
        """
        Convert 'term' column values to numeric.

        Parameters:
        - column: Pandas Series, 'term' column

        Returns:
        - Pandas Series with numeric values
        """
        return column.str.extract('(\d+)').astype(float)

    @staticmethod
    def convert_columns_to_numbers(df, term_column='term', employment_length_column='employment_length'):
        """
        Convert specified columns to numbers.

        Parameters:
        - df: DataFrame
        - term_column: str, name of the 'term' column
        - employment_length_column: str, name of the 'employment_length' column

        Returns:
        - DataFrame with converted columns
        """
        converter = ColumnConverter()

        # Converts 'term' column
        df[term_column] = converter.convert_term_column(df[term_column])

        # Converts 'employment_length' column
        df[employment_length_column] = df[employment_length_column].str.extract('(\d+)').astype(float)

        return df
