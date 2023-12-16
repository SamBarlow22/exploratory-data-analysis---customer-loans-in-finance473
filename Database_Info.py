import pandas as pd

class DataFrameInfo:
    def __init__(self, df):
        self.df = df

    def describe_all_columns(self):
        return self.df.dtypes

    def extract_statistical_values(self):
        excluded_columns = ['id', 'member_id', 'grade', 'sub_grade', 'home_ownership',
                             'verification_status', 'issue_date', 'loan_status', 'payment_plan',
                             'purpose', 'earliest_credit_line', 'last_payment_date',
                             'next_payment_date', 'last_credit_pull_date', 'application_type']

        columns_to_process = [col for col in self.df.columns if col not in excluded_columns]

        return {
            'median': self.df[columns_to_process].median(),
            'std': self.df[columns_to_process].std(),
            'mean': self.df[columns_to_process].mean()
        }

    def count_distinct_values(self):
        excluded_columns = ['id', 'member_id', 'grade', 'sub_grade', 'home_ownership',
                             'verification_status', 'issue_date', 'loan_status', 'payment_plan',
                             'purpose', 'earliest_credit_line', 'last_payment_date',
                             'next_payment_date', 'last_credit_pull_date', 'application_type']

        return self.df.drop(excluded_columns, axis=1).nunique()

    def print_shape(self):
        return self.df.shape

    def count_null_values(self):
        return self.df.isnull().sum()

    def percentage_null_values(self):
        return (self.df.isnull().sum() / len(self.df)) * 100

    def identify_outliers(self, threshold=0.003):
        # Selects numeric columns only
        numeric_columns = self.df.select_dtypes(include=['number']).columns

        # Calculates IQR for each numeric column
        q1 = self.df[numeric_columns].quantile(0.25)
        q3 = self.df[numeric_columns].quantile(0.75)
        iqr = q3 - q1

        # Identifies outliers based on IQR
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        # Counts outliers for each numeric column
        outliers_count = ((self.df[numeric_columns] < lower_bound) | (self.df[numeric_columns] > upper_bound)).sum()

        # Calculates the percentage of outliers for each column
        percentage_outliers = outliers_count / len(self.df) * 100

        # Filters columns based on the specified threshold
        columns_above_threshold = percentage_outliers[percentage_outliers > threshold].index

        # Creates a DataFrame to display results
        outliers_info = pd.DataFrame({
            'Lower Bound': lower_bound,
            'Upper Bound': upper_bound,
            'Outliers Count': outliers_count,
            'Percentage Outliers': percentage_outliers
        })

        return outliers_info, len(columns_above_threshold)

