import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


class Plotter:
    @staticmethod
    def visualize_nulls(df_info):
        plt.figure(figsize=(10, 6))
        plt.title('NULL Values in DataFrame')
        plt.imshow(df_info.df.isnull(), cmap='viridis', aspect='auto')
        plt.xlabel('Columns')
        plt.ylabel('Rows')
        plt.show()


    @staticmethod
    def visualize_after_imputation(df_before, df_after, columns_imputed):
        # Creates a mask for NULL values before and after imputation
        null_mask_before = df_before.isnull()
        null_mask_after = df_after.isnull()

        # Creates a figure with subplots for visual comparison
        fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

        # Plots NULL values before imputation
        sns.heatmap(null_mask_before, cmap='viridis', cbar=False, ax=axes[0])
        axes[0].set_title('NULL Values Before Imputation')

        # Plots NULL values after imputation
        sns.heatmap(null_mask_after, cmap='viridis', cbar=False, ax=axes[1])
        axes[1].set_title('NULL Values After Imputation')

        # Highlights columns that were imputed
        for col in columns_imputed:
            try:
                # If col is an index
                col_index = df_before.columns.get_loc(col)
            except KeyError:
                # If col is a column name
                col_index = df_before.columns.get_loc(df_before.columns[df_before.columns == col].item())

            for ax in axes:
                ax.axvline(x=col_index, color='red', linestyle='--', linewidth=2)
                ax.set_xticks(range(len(df_before.columns)))
                ax.set_xticklabels(df_before.columns, rotation=45, ha='right')

        plt.tight_layout()
        plt.show()


    @staticmethod
    def visualize_distribution_numeric(df, exclude_columns=None):
        if exclude_columns is None:
            exclude_columns = []

        numeric_columns = df.select_dtypes(include=['float', 'int']).columns
        numeric_columns = [col for col in numeric_columns if col not in exclude_columns]

        for col in numeric_columns:
            try:
                # Trys to convert the column to numeric, and skip if unsuccessful
                numeric_col = pd.to_numeric(df[col], errors='coerce')
                if numeric_col.notnull().all():
                    plt.figure(figsize=(10, 6))
                    sns.histplot(numeric_col, kde=True, color='skyblue', bins=30)
                    plt.title(f'Distribution of {col}')
                    plt.xlabel(col)
                    plt.ylabel('Frequency')
                    plt.show()
            except ValueError:
                pass


# class DataFrameTransform:
class DataFrameTransform:
    @staticmethod
    def drop_columns_with_nulls(df, threshold=0.3):
        # Drops columns with NULL values exceeding the threshold
        null_percentages = df.isnull().mean()
        columns_to_drop = null_percentages[null_percentages >= threshold].index
        df = df.drop(columns=columns_to_drop)
        return df

    @staticmethod
    def impute_nulls(df):
        """
        Impute NULL values in numerical columns of DataFrame based on specified strategies for specific columns.

        Parameters:
        - df: pandas DataFrame

        Returns:
        - df: pandas DataFrame with NULL values imputed
        """
        # Identifies columns with numerical data (integers or floats)
        numeric_columns = df.select_dtypes(include=['int', 'float', 'period[M]']).columns

        # Columns to impute with median
        median_columns = [col for col in numeric_columns if col in df.columns]

        # Columns to impute with mean
        mean_columns = [col for col in numeric_columns if col not in median_columns]

        # Imputes NULL values based on specified strategies for columns
        df[median_columns] = df[median_columns].fillna(df[median_columns].median())
        df[mean_columns] = df[mean_columns].fillna(df[mean_columns].mean())

        return df


    @staticmethod
    def reduce_skewness_log(df, columns):
        """
        Apply logarithmic transformation to specified columns to reduce skewness.

        Parameters:
        - df: pandas DataFrame
        - columns: List of column names to transform

        Returns:
        - df_transformed: pandas DataFrame with transformed columns
        """
        df_transformed = df.copy()

        # Apply logarithmic transformation to specified columns
        for col in columns:
            if col in df.columns and df[col].min() > 0:
                df_transformed[col] = np.log1p(df[col])

        return df_transformed


    @staticmethod
    def remove_outliers_zscore(df, threshold=3):
        """
        Remove outliers from numeric columns using z-scores.

        Parameters:
        - df: pandas DataFrame
        - threshold: Z-score threshold for outlier removal (default is 3)

        Returns:
        - df_outliers_removed: pandas DataFrame with outliers removed
        """
        df_outliers_removed = df.copy()

        # Selects numeric columns (integers and floats)
        numeric_columns = df.select_dtypes(include=['int', 'float']).columns

        for col in numeric_columns:
            # Calculates z-scores for the column
            z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())

            # Identifies rows where z-score exceeds the threshold
            outliers_mask = z_scores > threshold

            # Removes outliers by replacing with NaN
            df_outliers_removed.loc[outliers_mask, col] = np.nan

        # Drops rows with NaN values after outlier removal
        df_outliers_removed = df_outliers_removed.dropna()

        return df_outliers_removed
