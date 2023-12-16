import pandas as pd

class DataTransform:
    date_columns = ['issue_date', 'last_payment_date', 'next_payment_date', 'earliest_credit_line', 'last_credit_pull_date']

    def convert_columns_to_datetime(self, df):
        for column in DataTransform.date_columns:
            df[column] = pd.to_datetime(df[column], errors='coerce', format='%b-%Y')
            df[column] = df[column].dt.to_period('M')  # Extracts month and year only

        # Converts 'term' and 'employment_length' columns to numeric values
        df['term'] = df['term'].str.extract('(\d+)').astype(float)
        df['employment_length'] = df['employment_length'].str.extract('(\d+)').astype(float)

        return df
